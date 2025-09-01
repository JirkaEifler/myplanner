"""Forms for the MyPlanner Django application.

Key guarantees:
- Users only see/select their own lists and tags.
- Newly created tags are owned by the current user.
- A user cannot attach someone else’s tags (server-side validation).
"""

from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Task, TypeToDoList, Comment, Reminder, Tag, Event


class LenientModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    """
    Custom M2M field that ignores special "NEW__<name>" placeholder values
    injected by the UI when users add brand-new tags inline.
    """

    def clean(self, value):
        if value is None:
            value = []
        keep = []
        for v in value:
            if isinstance(v, str) and v.startswith("NEW__"):
                # Let TaskForm handle creation later; skip these here.
                continue
            keep.append(v)
        return super().clean(keep)


class TaskForm(forms.ModelForm):
    """
    Create/edit Task with support for selecting existing tags
    and creating new ones inline. Lists/tags are restricted to the current user.
    """

    tags = LenientModelMultipleChoiceField(
        queryset=Tag.objects.none(),
        required=False,
        widget=forms.SelectMultiple(
            attrs={"size": 8, "class": "tags-multiselect", "id": "id_tags"}
        ),
        label="Tags",
        help_text="Hold Ctrl/Cmd to select multiple.",
    )
    new_tags = forms.CharField(
        required=False,
        label="New tags",
        help_text="Comma-separated (e.g. Work, Family).",
        widget=forms.TextInput(
            attrs={"placeholder": "New tag…", "id": "id_new_tag_input"}
        ),
    )

    _new_tag_names = None  # collected in clean_tags()
    _user = None           # set in __init__

    def __init__(self, user, *args, **kwargs):
        """
        Expect `user` and scope list/tag querysets to this user only.
        """
        super().__init__(*args, **kwargs)
        self._user = user

        # Lists owned by this user
        self.fields["list"].queryset = (
            TypeToDoList.objects.filter(owner=user).order_by("name")
        )

        # Tags owned by this user
        self.fields["tags"].queryset = (
            Tag.objects.filter(owner=user).order_by("name")
        )

        # Minor field tweaks
        self.fields["due_date"].required = False
        self.fields["priority"].label = "Priority"

        # Pre-fill tags when editing
        if self.instance and self.instance.pk:
            # Instance should already contain only the owner’s tags,
            # but initial is set for convenience.
            self.fields["tags"].initial = self.instance.tags.all()

    def clean(self):
        """
        Server-side safety: ensure selected tags belong to the current user.
        """
        cleaned = super().clean()
        tags = cleaned.get("tags") or []
        illegal = [t for t in tags if t.owner_id != getattr(self._user, "id", None)]
        if illegal:
            raise ValidationError("You cannot attach tags that you don’t own.")
        return cleaned

    def clean_tags(self):
        """
        Capture any "NEW__<name>" values submitted by the UI for later creation.
        """
        selected = self.cleaned_data.get("tags")
        raw_vals = self.data.getlist("tags")
        new_names = []
        for v in raw_vals:
            if isinstance(v, str) and v.startswith("NEW__"):
                name = v[5:].strip()
                if name:
                    new_names.append(name)
        self._new_tag_names = new_names
        return selected

    @transaction.atomic
    def save(self, commit=True):
        """
        Save the Task and handle tag assignment:
        - Attach existing (owner-scoped) tags.
        - Create any new tags as owned by the current user and attach them.
        """
        task = super().save(commit=False)

        # Ensure task owner is set if your view hasn’t already
        if not task.owner_id:
            task.owner = self._user

        task.save()

        # Existing selected tags (already validated in clean())
        selected_tags = self.cleaned_data.get("tags") or []
        task.tags.set(selected_tags)

        # Also parse comma-separated "new_tags" field
        new_names = list(self._new_tag_names or [])
        csv_raw = (self.cleaned_data.get("new_tags") or "").strip()
        if csv_raw:
            new_names += [s.strip() for s in csv_raw.split(",") if s.strip()]

        # Create/attach per-user tags
        for name in new_names:
            # Unique per (owner, lower(name)) is enforced in the model constraints
            tag, _ = Tag.objects.get_or_create(name=name, owner=self._user)
            task.tags.add(tag)

        if commit:
            task.save()
        return task

    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "is_completed", "list", "priority"]
        widgets = {"due_date": forms.DateInput(attrs={"type": "date"})}


class TypeToDoListForm(forms.ModelForm):
    """Create/edit a to-do list (name only)."""

    class Meta:
        model = TypeToDoList
        fields = ["name"]


class CommentForm(forms.ModelForm):
    """Create a comment on a task."""

    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {"body": forms.Textarea(attrs={"rows": 3, "placeholder": "Add a comment…"})}


class ReminderForm(forms.ModelForm):
    """Create/edit a reminder."""

    class Meta:
        model = Reminder
        fields = ["remind_at", "note"]
        widgets = {
            "remind_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "note": forms.TextInput(attrs={"placeholder": "Optional note…"}),
        }


class TaskFilterForm(forms.Form):
    """
    Filter tasks by search text, list, tags, priority, and completion.
    Lists and tags are strictly scoped to the current user.
    """

    q = forms.CharField(required=False, label="Search")
    list = forms.ModelChoiceField(
        queryset=TypeToDoList.objects.none(), required=False, label="List"
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={"size": 6}),
        label="Tags",
        help_text="Hold ⌘/Ctrl to select multiple.",
    )
    priority = forms.ChoiceField(
        choices=[("", "—")] + [(str(n), f"Priority {n}") for n in (1, 2, 3, 4)],
        required=False,
        label="Priority",
    )
    done = forms.ChoiceField(
        choices=[("", "—"), ("0", "Open"), ("1", "Completed")],
        required=False,
        label="Done",
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["list"].queryset = (
            TypeToDoList.objects.filter(owner=user).order_by("name")
        )
        # Only the user’s own tags (not “tags used by my tasks”)
        self.fields["tags"].queryset = Tag.objects.filter(owner=user).order_by("name")


class MyTagsBulkForm(forms.Form):
    """
    Settings: bulk delete of the current user's tags only.
    """

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="My tags",
        help_text="",
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = user
        self.fields["tags"].queryset = Tag.objects.filter(owner=user).order_by("name")

    def delete_from_database(self) -> int:
        """
        Delete selected tags, but only those owned by the current user.
        Returns the number of deleted rows.
        """
        chosen = list(self.cleaned_data.get("tags") or [])
        if not chosen:
            return 0
        ids = [t.id for t in chosen]
        deleted, _ = Tag.objects.filter(owner=self._user, id__in=ids).delete()
        return deleted


class EventForm(forms.ModelForm):
    """Create/edit a one-off calendar event tied to a task."""

    class Meta:
        model = Event
        fields = ["start_time", "end_time"]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
        labels = {"start_time": "Start", "end_time": "End"}

    def clean(self):
        """
        Defer to model-level clean() (e.g., validating end >= start)
        while allowing blank fields to be normalized first.
        """
        return super().clean()