from django.urls import path
from . import views_html as views

urlpatterns = [
    # Home page
    path("", views.home, name="home"),

    # Tasks views
    path("app/tasks/", views.html_task_list, name="html-task_list"),
    path("app/tasks/create/", views.html_task_create, name="html-task_create"),
    path("app/tasks/<int:pk>/", views.html_task_detail, name="html-task_detail"),
    path("app/tasks/<int:pk>/edit/", views.html_task_edit, name="html-task_edit"),
    path("app/tasks/<int:pk>/delete/", views.html_task_delete, name="html-task_delete"),

    # TypeToDoList views
    path("app/lists/", views.html_list_index, name="html-list_index"),
    path("app/lists/create/", views.html_list_create, name="html-list_create"),
    path("app/lists/<int:pk>/", views.html_list_detail, name="html-list_detail"),
    path("app/lists/<int:pk>/edit/", views.html_list_edit, name="html-list_edit"),
    path("app/lists/<int:pk>/delete/", views.html_list_delete, name="html-list_delete"),

    # Toggle "done" (AJAX)
    path("tasks/<int:pk>/toggle-done/", views.toggle_task_done, name="html-task_toggle_done"),
]