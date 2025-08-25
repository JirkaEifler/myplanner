"""API URL configuration for the planner app.

Provides REST API endpoints for:
- TypeToDoList
- Task
- Reminder
- Event
- Tag
"""

from django.urls import path
from .views import (
    TypeToDoListListCreateView, TypeToDoListDetailView,
    TaskListCreateView, TaskDetailView,
    ReminderListCreateView, ReminderDetailView,
    EventListCreateView, EventDetailView,
    TagListCreateView, TagDetailView,
)

urlpatterns = [
    # API - Type lists
    path("type-lists/", TypeToDoListListCreateView.as_view(), name="typelist-list-create"),
    path("type-lists/<int:pk>/", TypeToDoListDetailView.as_view(), name="typelist-detail"),

    # API - Tasks
    path("tasks/", TaskListCreateView.as_view(), name="task-list-create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),

    # API - Reminders
    path("reminders/", ReminderListCreateView.as_view(), name="reminder-list-create"),
    path("reminders/<int:pk>/", ReminderDetailView.as_view(), name="reminder-detail"),

    # API - Events
    path("events/", EventListCreateView.as_view(), name="event-list-create"),
    path("events/<int:pk>/", EventDetailView.as_view(), name="event-detail"),

    # API - Tags
    path("tags/", TagListCreateView.as_view(), name="tag-list-create"),
    path("tags/<int:pk>/", TagDetailView.as_view(), name="tag-detail"),
]