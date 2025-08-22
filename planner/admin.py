from django.contrib import admin
from .models import TypeToDoList, Task, Reminder, Tag, Event, Comment


@admin.register(TypeToDoList)
class TypeToDoListAdmin(admin.ModelAdmin):
    list_display = ("name", "owner")
    search_fields = ("name", "owner__username")
    list_select_related = ("owner",)
    ordering = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "list", "owner", "priority", "due_date", "is_completed")
    list_filter = ("list", "priority", "is_completed")
    search_fields = ("title", "description")
    list_select_related = ("list", "owner")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("task", "author", "created_at")
    search_fields = ("body", "task__title", "author__username")
    list_select_related = ("task", "author")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ("task", "owner", "remind_at", "created_at")
    search_fields = ("task__title", "owner__username")
    list_select_related = ("task", "owner")
    ordering = ("-remind_at",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("task", "start_time", "end_time")
    search_fields = ("task__title",)
    list_select_related = ("task",)
    ordering = ("-start_time",)