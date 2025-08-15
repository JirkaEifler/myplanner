from rest_framework import serializers
from .models import TypeToDoList, Task, Reminder, Tag, Event


class TypeToDoListSerializer(serializers.ModelSerializer):
    """Convert TypeToDoList model to/from JSON for the API."""
    owner = serializers.ReadOnlyField(source="owner.username")  # show username instead of ID

    class Meta:
        model = TypeToDoList
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    """Convert Task model to/from JSON for the API."""
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Task
        fields = "__all__"


class ReminderSerializer(serializers.ModelSerializer):
    """Convert Reminder model to/from JSON for the API."""

    class Meta:
        model = Reminder
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    """Convert Tag model to/from JSON for the API."""

    class Meta:
        model = Tag
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    """Convert Event model to/from JSON for the API."""

    class Meta:
        model = Event
        fields = "__all__"