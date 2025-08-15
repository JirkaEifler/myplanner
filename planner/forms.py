from django import forms
from .models import Task, TypeToDoList


class TaskForm(forms.ModelForm):
    """Form to create or edit a Task. Limits "list" choices to the user's own lists."""

    def __init__(self, user, *args, **kwargs):
        """Filter the "list" field to lists owned by the current user (sorted by name)."""

        super().__init__(*args, **kwargs) # Voláme původní konstruktor rodičovské třídy ModelForm
        self.fields["list"].queryset = TypeToDoList.objects.filter(owner=user).order_by("name")

    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "is_completed", "list"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }


class TypeToDoListForm(forms.ModelForm):
    """Simple form for creating or editing a list type (name only)."""

    class Meta:
        model = TypeToDoList
        fields = ["name"]