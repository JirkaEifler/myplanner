"""HTML URL configuration for the planner app.

Provides classic HTML views for:
- Home
- Tasks (list, create, detail, edit, delete, toggle)
- Lists (list, create, detail, edit, delete)
- Filters
- Settings
- Reminders
- Comments
- Events
"""

from django.urls import path
from . import views_html as views

urlpatterns = [
    path("", views.home, name="home"),

    # Tasks
    path("app/tasks", views.html_task_list, name="html-task_list"),
    path("app/tasks/create", views.html_task_create, name="html-task_create"),
    path("app/tasks/<int:pk>", views.html_task_detail, name="html-task_detail"),
    path("app/tasks/<int:pk>/edit", views.html_task_edit, name="html-task_edit"),
    path("app/tasks/<int:pk>/delete", views.html_task_delete, name="html-task_delete"),
    path("app/tasks/<int:pk>/toggle-done/", views.toggle_task_done, name="html-task_toggle_done"),

    # Lists
    path("app/lists", views.html_list_index, name="html-list_index"),
    path("app/lists/create", views.html_list_create, name="html-list_create"),
    path("app/lists/<int:pk>", views.html_list_detail, name="html-list_detail"),
    path("app/lists/<int:pk>/edit", views.html_list_edit, name="html-list_edit"),
    path("app/lists/<int:pk>/delete", views.html_list_delete, name="html-list_delete"),

    # Filters
    path("app/filters", views.html_filters, name="html-filters"),

    # Settings
    path("app/settings", views.html_settings, name="html-settings"),

    # Reminders
    path("app/tasks/<int:pk>/reminders/add", views.html_reminder_add, name="html-reminder_add"),
    path("app/reminders/<int:rid>/delete", views.html_reminder_delete, name="html-reminder_delete"),

    # Comments
    path("tasks/<int:task_pk>/comments/add/", views.html_comment_add, name="html-comment_add"),
    path("comments/<int:pk>/delete/", views.html_comment_delete, name="html-comment_delete"),

    # Events
    path("tasks/<int:task_pk>/events/add/", views.html_event_add, name="html-event_add"),
    path("events/<int:pk>/edit/", views.html_event_edit, name="html-event_edit"),
    path("events/<int:pk>/delete/", views.html_event_delete, name="html-event_delete"),
]