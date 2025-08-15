from django.urls import path
from .views import (
    TypeToDoListListCreateView, TypeToDoListDetailView,
    TaskListCreateView, TaskDetailView,
    ReminderListCreateView, ReminderDetailView,
    EventListCreateView, EventDetailView,
    TagListCreateView, TagDetailView,
)

urlpatterns = [
    # APIi - Type lists (list all or create, get/update/delete one)
    path("type-lists/", TypeToDoListListCreateView.as_view(), name="typelist-list-create"),
    path("type-lists/<int:pk>/", TypeToDoListDetailView.as_view(), name="typelist-detail"),

    # API - Tasks (list all or create, get/update/delete one)
    path("tasks/", TaskListCreateView.as_view(), name="task-list-create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),

    # API - Reminders (list all or create, get/update/delete one)
    path("reminders/", ReminderListCreateView.as_view(), name="reminder-list-create"),
    path("reminders/<int:pk>/", ReminderDetailView.as_view(), name="reminder-detail"),

    # API - Events (list all or create, get/update/delete one)
    path("events/", EventListCreateView.as_view(), name="event-list-create"),
    path("events/<int:pk>/", EventDetailView.as_view(), name="event-detail"),

    # API - Tags (list all or create, get/update/delete one)
    path("tags/", TagListCreateView.as_view(), name="tag-list-create"),
    path("tags/<int:pk>/", TagDetailView.as_view(), name="tag-detail"),
]