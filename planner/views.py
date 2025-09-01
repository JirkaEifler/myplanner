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
    """
    API view to list and create user-specific tags.
    - GET: returns only the tags belonging to the authenticated user.
    - POST: creates a new tag owned by the authenticated user.
    """
    serializer_class = TagSerializer

    def get_queryset(self):
        """
        Return tags filtered by the current user, ordered by name.
        Ensures users only see their own tags.
        """
        return Tag.objects.filter(owner=self.request.user).order_by("name")

    def perform_create(self, serializer):
        """
        Save a new tag and automatically assign ownership
        to the authenticated user.
        """
        serializer.save(owner=self.request.user)


class TagDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific user tag.
    - Ensures that only the owner of the tag can access or modify it.
    """
    serializer_class = TagSerializer

    def get_queryset(self):
        """
        Return only the tags belonging to the authenticated user.
        Prevents unauthorized access to other users' tags.
        """
        return Tag.objects.filter(owner=self.request.user)