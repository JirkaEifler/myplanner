# planner/forms.py
from django import forms
from .models import Task, TypeToDoList, Comment, Reminder, Tag


class TaskForm(forms.ModelForm):
    """Form for creating/editing a Task: user lists, optional due_date, priority, tags + CSV new tags."""

    # vlastní pole pro tagy (reverse M2M; Django je automaticky nevygeneruje)
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Tags",
        help_text="Optional tags for this task.",
    )

    # nové volitelné pole – čárkami oddělené názvy tagů k vytvoření
    new_tags = forms.CharField(
        required=False,
        label="New tags",
        help_text="Comma-separated (e.g. Work, Family)",
    )

    def __init__(self, user, *args, **kwargs):
        """Limit lists to current user; make due_date optional; preload tags on edit."""
        super().__init__(*args, **kwargs)

        # seznamy jen aktuálního uživatele
        self.fields["list"].queryset = (
            TypeToDoList.objects.filter(owner=user).order_by("name")
        )

        # datum je nepovinné
        self.fields["due_date"].required = False

        # hezčí label
        self.fields["priority"].label = "Priority"

        # checkboxy s tagy, seřazené
        self.fields["tags"].queryset = Tag.objects.all().order_by("name")

        # při editaci předvyplním stávající tagy
        if self.instance and self.instance.pk:
            self.fields["tags"].initial = self.instance.tags.all()

    def save(self, commit=True):
        """Save task, set selected tags, create CSV tags from new_tags."""
        # nejdřív uložím modelová pole
        task = super().save(commit=commit)

        # pokud se ukládalo s commit=False, zajistím pk pro M2M
        if not commit:
            task.save()

        # 1) vybrané tagy z checkboxů -> nahradit
        selected_tags = self.cleaned_data.get("tags")
        if selected_tags is not None:
            task.tags.set(selected_tags)  # přepíše vazby

        # 2) nové tagy z CSV -> vytvořit/načíst a přidat
        raw = (self.cleaned_data.get("new_tags") or "").strip()
        if raw:
            names = [n.strip() for n in raw.split(",") if n.strip()]
            for name in names:
                tag, _ = Tag.objects.get_or_create(name=name)
                task.tags.add(tag)

        return task

    class Meta:
        model = Task
        # jen skutečná modelová pole Tasku
        fields = ["title", "description", "due_date", "is_completed", "list", "priority"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
            # "priority": forms.RadioSelect(),  # volitelné
        }


class TypeToDoListForm(forms.ModelForm):
    """Form for creating/editing a To-Do list type (name only)."""
    class Meta:
        model = TypeToDoList
        fields = ["name"]


class CommentForm(forms.ModelForm):
    """Form for adding a comment to a task."""
    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(attrs={"rows": 3, "placeholder": "Add a comment…"}),
        }


class ReminderForm(forms.ModelForm):
    """Form for adding a reminder to a task."""
    class Meta:
        model = Reminder
        fields = ["remind_at"]
        widgets = {
            "remind_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }