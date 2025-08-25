"""REST API views for the planner app.

This module exposes CRUD endpoints for:
- TypeToDoList
- Task
- Reminder
- Event
- Tag

Each list view returns data scoped to the current user; detail views only
operate on objects owned by the current user (directly or via the related task).
"""

from rest_framework import generics

from .models import TypeToDoList, Task, Reminder, Tag, Event
from .serializers import (
    TypeToDoListSerializer,
    TaskSerializer,
    ReminderSerializer,
    TagSerializer,
    EventSerializer,
)


# -------------------- TypeToDoList --------------------

class TypeToDoListListCreateView(generics.ListCreateAPIView):
    """List all list types for the current user or create a new one."""
    serializer_class = TypeToDoListSerializer

    def get_queryset(self):
        return TypeToDoList.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TypeToDoListDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a single list type owned by the user."""
    serializer_class = TypeToDoListSerializer

    def get_queryset(self):
        return TypeToDoList.objects.filter(owner=self.request.user)


# ------------------------- Task -------------------------

class TaskListCreateView(generics.ListCreateAPIView):
    """List all tasks for the current user or create a new task."""
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a single task owned by the user."""
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)


# ----------------------- Reminder -----------------------

class ReminderListCreateView(generics.ListCreateAPIView):
    """List all reminders for the user's tasks or create a new reminder."""
    serializer_class = ReminderSerializer

    def get_queryset(self):
        return Reminder.objects.filter(task__owner=self.request.user)


class ReminderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a single reminder for the user's task."""
    serializer_class = ReminderSerializer

    def get_queryset(self):
        return Reminder.objects.filter(task__owner=self.request.user)


# ------------------------- Event ------------------------

class EventListCreateView(generics.ListCreateAPIView):
    """List all events for the user's tasks or create a new event."""
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(task__owner=self.request.user)


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a single event for the user's task."""
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(task__owner=self.request.user)


# -------------------------- Tag -------------------------

class TagListCreateView(generics.ListCreateAPIView):
    """List all tags used across the user's tasks or create a new tag."""
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.filter(tasks__owner=self.request.user).distinct()


class TagDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a single tag used on the user's tasks."""
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.filter(tasks__owner=self.request.user).distinct()