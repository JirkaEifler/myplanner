"""Forms for the Planner Django application."""

from django import forms
from django.db import transaction
from django.db.models import Count
from .models import Task, TypeToDoList, Comment, Reminder, Tag, Event


class LenientModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    """Custom field allowing 'NEW__<name>' values in multi-select inputs."""

    def clean(self, value):
        if value is None:
            value = []
        kept = []
        for v in value:
            if isinstance(v, str) and v.startswith("NEW__"):
                continue
            kept.append(v)
        return super().clean(kept)


class TaskForm(forms.ModelForm):
    """Form for creating and editing tasks, with support for new and existing tags."""

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
        help_text="Comma-separated (e.g. Work, Family)",
        widget=forms.TextInput(
            attrs={"placeholder": "New tag…", "id": "id_new_tag_input"}
        ),
    )
    _new_tag_names = None

    def __init__(self, user, *args, **kwargs):
        """Initialize with the current user and filter lists/tags by ownership."""
        super().__init__(*args, **kwargs)
        self.fields["list"].queryset = TypeToDoList.objects.filter(owner=user).order_by("name")
        self.fields["due_date"].required = False
        self.fields["priority"].label = "Priority"
        self.fields["tags"].queryset = Tag.objects.all().order_by("name")
        if self.instance and self.instance.pk:
            self.fields["tags"].initial = self.instance.tags.all()

    def clean_tags(self):
        """Extract and remember new tag names from submitted data."""
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
        """Save the task, including new tags if provided."""
        task = super().save(commit=False)
        task.save()
        selected_tags = self.cleaned_data.get("tags") or []
        task.tags.set(selected_tags)
        new_names = list(self._new_tag_names or [])
        csv_raw = (self.cleaned_data.get("new_tags") or "").strip()
        if csv_raw:
            new_names += [s.strip() for s in csv_raw.split(",") if s.strip()]
        for name in new_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            task.tags.add(tag)
        if commit:
            task.save()
        return task

    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "is_completed", "list", "priority"]
        widgets = {"due_date": forms.DateInput(attrs={"type": "date"})}


class TypeToDoListForm(forms.ModelForm):
    """Form for creating and editing to-do lists."""

    class Meta:
        model = TypeToDoList
        fields = ["name"]


class CommentForm(forms.ModelForm):
    """Form for adding comments to tasks."""

    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {"body": forms.Textarea(attrs={"rows": 3, "placeholder": "Add a comment…"})}


class ReminderForm(forms.ModelForm):
    """Form for creating and editing reminders."""

    class Meta:
        model = Reminder
        fields = ["remind_at", "note"]
        widgets = {
            "remind_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "note": forms.TextInput(attrs={"placeholder": "Optional note…"}),
        }


class TaskFilterForm(forms.Form):
    """Form for filtering tasks by search text, list, tags, priority, and completion."""

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
        """Filter lists and tags to only those belonging to the user."""
        super().__init__(*args, **kwargs)
        self.fields["list"].queryset = TypeToDoList.objects.filter(owner=user).order_by("name")
        self.fields["tags"].queryset = Tag.objects.filter(tasks__owner=user).distinct().order_by("name")


class MyTagsBulkForm(forms.Form):
    """Form for selecting and deleting multiple tags."""

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="My tags",
        help_text="",
    )

    def __init__(self, user, *args, **kwargs):
        """Filter available tags to all existing tags."""
        super().__init__(*args, **kwargs)
        self.fields["tags"].queryset = Tag.objects.all().order_by("name")

    def delete_from_database(self):
        """Delete the selected tags from the database."""
        chosen = self.cleaned_data.get("tags")
        if not chosen:
            return 0
        deleted, _ = Tag.objects.filter(pk__in=[t.pk for t in chosen]).delete()
        return deleted


class EventForm(forms.ModelForm):
    """Form for creating and editing events tied to a task."""

    class Meta:
        model = Event
        fields = ["start_time", "end_time"]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
        labels = {
            "start_time": "Start",
            "end_time": "End",
        }

    def clean(self):
        """Run model-level validation while allowing empty fields in the form."""
        cleaned = super().clean()
        return cleaned