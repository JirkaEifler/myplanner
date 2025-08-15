from rest_framework import generics
from .models import TypeToDoList, Task, Reminder, Tag, Event
from .serializers import (
    TypeToDoListSerializer,
    TaskSerializer,
    ReminderSerializer,
    TagSerializer,
    EventSerializer
)

# TypeToDoList
class TypeToDoListListCreateView(generics.ListCreateAPIView):
    """List all to-do list types of the current user or create a new one."""
    serializer_class = TypeToDoListSerializer
    def get_queryset(self):
        return TypeToDoList.objects.filter(owner=self.request.user)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TypeToDoListDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a single to-do list type."""
    serializer_class = TypeToDoListSerializer
    def get_queryset(self):
        return TypeToDoList.objects.filter(owner=self.request.user)

# Tasks
class TaskListCreateView(generics.ListCreateAPIView):
    """List all tasks of the current user or create a new task."""
    serializer_class = TaskSerializer
    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a single task."""
    serializer_class = TaskSerializer
    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

# Reminders
class ReminderListCreateView(generics.ListCreateAPIView):
    """List all reminders for the current user's tasks or create a new reminder."""
    serializer_class = ReminderSerializer
    def get_queryset(self):
        return Reminder.objects.filter(task__owner=self.request.user)

class ReminderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a single reminder."""
    serializer_class = ReminderSerializer
    def get_queryset(self):
        return Reminder.objects.filter(task__owner=self.request.user)

# Events
class EventListCreateView(generics.ListCreateAPIView):
    """List all events for the current user's tasks or create a new event."""
    serializer_class = EventSerializer
    def get_queryset(self):
        return Event.objects.filter(task__owner=self.request.user)

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a single event."""
    serializer_class = EventSerializer
    def get_queryset(self):
        return Event.objects.filter(task__owner=self.request.user)

# Tags
class TagListCreateView(generics.ListCreateAPIView):
    """List all tags used in the current user's tasks or create a new tag."""
    serializer_class = TagSerializer
    def get_queryset(self):
        return Tag.objects.filter(tasks__owner=self.request.user).distinct()

class TagDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a single tag."""
    serializer_class = TagSerializer
    def get_queryset(self):
        return Tag.objects.filter(tasks__owner=self.request.user).distinct()