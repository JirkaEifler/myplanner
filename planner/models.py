"""Domain models for the Planner app.

Models:
1) TypeToDoList - user-owned list type/category
2) Task         – a single user task in a given list
3) Tag          – label attached to tasks (M:N)
4) Comment      – freeform comment on a task (1:N)
5) Reminder     – time-based reminder for a task (1:N)
6) Event        – fixed start/end time window bound to a task (1:1)
"""

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class TypeToDoList(models.Model):
    """Type/category of a to‑do list (e.g., Daily, Weekly, Shopping)."""

    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="typelists",
        null=True,
        blank=True,
        help_text="Owner of this list type.",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "To-Do List Type"
        verbose_name_plural = "To-Do List Types"

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    """Single task belonging to a list type and owned by a user."""

    PRIORITY_CHOICES = (
        (1, "Priority 1"),
        (2, "Priority 2"),
        (3, "Priority 3"),
        (4, "Priority 4"),
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True, db_index=True)
    is_completed = models.BooleanField(default=False)
    priority = models.PositiveSmallIntegerField(
        choices=PRIORITY_CHOICES,
        default=4,
        db_index=True,
        help_text="1 = highest priority, 4 = lowest.",
    )

    # Relations
    list = models.ForeignKey(
        TypeToDoList,
        on_delete=models.CASCADE,
        related_name="tasks",
        help_text="List to which this task belongs.",
    )
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="collaborating_tasks",
        help_text="Optional collaborators on this task.",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True,
        blank=True,
        help_text="Primary owner of this task.",
    )

    class Meta:
        # Consistent ordering: list name → priority → due date → title
        ordering = ["list__name", "priority", "due_date", "title"]

    def __str__(self) -> str:
        status = "Completed" if self.is_completed else "Incomplete"
        return f"{self.title} ({status})"


class Reminder(models.Model):
    """Time-based reminder associated with a specific task."""

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="reminders",
        help_text="Task that this reminder is for.",
    )
    remind_at = models.DateTimeField(db_index=True)
    note = models.CharField(max_length=255, blank=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reminders",
        null=True,
        blank=True,
        help_text="Owner of this reminder.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ["remind_at"]

    def __str__(self) -> str:
        return f"Reminder for '{self.task.title}' at {self.remind_at:%Y-%m-%d %H:%M}"


class Tag(models.Model):
    """Tag/label that can be attached to many tasks (e.g., Work, Personal)."""

    name = models.CharField(max_length=255, unique=True)
    tasks = models.ManyToManyField(
        Task,
        related_name="tags",
        blank=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self) -> str:
        return self.name


class Comment(models.Model):
    """Freeform comment posted on a task."""

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="task_comments",
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Newest comments first
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Comment by {self.author} on {self.task}"


class Event(models.Model):
    """Event with fixed start/end timestamps attached to a task (1:1)."""

    task = models.OneToOneField(
        Task,
        on_delete=models.CASCADE,
        related_name="event",
        help_text="Task that this event details.",
    )
    start_time = models.DateTimeField(db_index=True)
    end_time = models.DateTimeField(db_index=True)

    class Meta:
        ordering = ["start_time"]

    def clean(self) -> None:
        """Ensure the end time is not earlier than the start time."""
        if self.end_time and self.start_time and self.end_time < self.start_time:
            raise ValidationError("Event end time cannot be earlier than start time.")

    def __str__(self) -> str:
        return f"Event: {self.task.title} ({self.start_time} – {self.end_time})"