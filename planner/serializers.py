"""DRF serializers for the Planner API.

Includes basic ModelSerializers for:
- TypeToDoList
- Task
- Reminder
- Tag
- Event
"""

from rest_framework import serializers
from .models import TypeToDoList, Task, Reminder, Tag, Event


class TypeToDoListSerializer(serializers.ModelSerializer):
    """Serialize/deserialize TypeToDoList objects for the API."""
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = TypeToDoList
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    """Serialize/deserialize Task objects for the API."""
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Task
        fields = "__all__"


class ReminderSerializer(serializers.ModelSerializer):
    """Serialize/deserialize Reminder objects for the API."""

    class Meta:
        model = Reminder
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    """Serialize/deserialize Tag objects for the API."""

    class Meta:
        model = Tag
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    """Serialize/deserialize Event objects for the API."""

    class Meta:
        model = Event
        fields = "__all__"