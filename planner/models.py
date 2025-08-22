from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

"""
Application data models:
1)  TypeToDoList    - user-owned list type/category
2)  Task            - single user task in a given list
3)  Tag             - label attached to tasks (M:N), reverse: task.tags
4)  Comment         - comments to a task (1:N)
5)  Reminder        - time-based reminder for a task (1:N)
6)  Event           - time window bound to a task (1:1)
"""


class TypeToDoList(models.Model):
    """Type of to-do list (e.g., daily, weekly, shopping, birthdays)."""
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(  # ForeignKey na model uživatele - každý typ seznamu patří jednomu konkrétnímu uživateli (user_id).
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="typelists",
        null=True,
        blank=True,
        help_text="Owner of this list type",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "To-Do List Type"
        verbose_name_plural = "To-Do List Types"

    def __str__(self):
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

    # Číselná priorita – 1 = nejvyšší, 4 = nejnižší
    priority = models.PositiveSmallIntegerField(
        choices=PRIORITY_CHOICES,
        default=4,
        db_index=True,
        help_text="1 = nejvyšší, 4 = nejnižší",
    )

    # relations
    list = models.ForeignKey(  # ForeignKey na TypeToDoList - každý úkol patří právě jednomu seznamu (list_id).
        TypeToDoList,
        on_delete=models.CASCADE,
        related_name="tasks",
        help_text="List to which this task belongs.",
    )
    users = models.ManyToManyField(  # ManyToManyField na uživatele - jeden úkol může mít více spolupracovníků a jeden uživatel může spolupracovat na více úkolech.
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="collaborating_tasks",  # user.collaborating_tasks.all()
        help_text="Optional collaborators on this task.",
    )
    owner = models.ForeignKey(  # ForeignKey na model uživatele – každý úkol má uloženého svého hlavního vlastníka (user_id).
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",  # user.tasks.all()
        null=True,
        blank=True,
        help_text="Primary owner of this task.",
    )

    class Meta:
        # Sjednocené řazení: nejdřív podle jména listu, pak priority, termínu a názvu
        ordering = ["list__name", "priority", "due_date", "title"]

    def __str__(self):
        status = "Completed" if self.is_completed else "Incomplete"
        return f"{self.title} ({status})"  # např. "Buy milk (Incomplete)"


class Reminder(models.Model):
    """Reminder bound to a specific task."""
    task = models.ForeignKey(  # ForeignKey na Task - každá připomínka je propojena s jedním konkrétním úkolem (task_id).
        Task,
        on_delete=models.CASCADE,
        related_name="reminders",
        help_text="Task that this reminder is for.",
    )
    remind_at = models.DateTimeField(db_index=True)
    note = models.CharField(max_length=255, blank=True)

    owner = models.ForeignKey(  # ForeignKey na model uživatele – každá připomínka má svého vlastníka, ale nemusí být povinný.
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reminders",
        null=True,   # dovolí hodnotu NULL v databázi
        blank=True,  # dovolí prázdné v Django formulářích/adminu
        help_text="Owner of this reminder.",
    )

    created_at = models.DateTimeField(  # kdy byla připomínka vytvořena
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ["remind_at"]

    def __str__(self):
        return f"Reminder for '{self.task.title}' at {self.remind_at:%Y-%m-%d %H:%M}"


class Tag(models.Model):
    """Tag/label that can be attached to many tasks (e.g. work, personal, shopping)."""
    name = models.CharField(max_length=255, unique=True)
    tasks = models.ManyToManyField(  # ManyToManyField na Task - jeden tag může být přiřazen k více úkolům a jeden úkol může mít více tagů.
        Task,
        related_name="tags",
        blank=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name


class Comment(models.Model):
    """Freeform comment to a task (1:N)."""
    task = models.ForeignKey(  # ForeignKey na Task – každý komentář patří právě jednomu úkolu.
        Task,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(  # ForeignKey na uživatele – kdo komentář napsal.
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="task_comments",
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]  # nejnovější nahoře

    def __str__(self):
        return f"Comment by {self.author} on {self.task}"


class Event(models.Model):
    """Event with fixed start/end time attached to a task."""
    task = models.OneToOneField(  # OneToOneField na Task - každá událost je svázaná s jedním konkrétním úkolem a úkol má právě jednu událost.
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
        """Ensure event end time is not earlier than start time."""
        if self.end_time and self.start_time and self.end_time < self.start_time:
            raise ValidationError("Event end time cannot be earlier than start time.")

    def __str__(self):
        return f"Event: {self.task.title} ({self.start_time} – {self.end_time})"