"""HTML views for the MyPlanner app.

This module provides the classic (server-rendered) HTML views, including:
- Authentication (login redirector, logout handler, registration)
- Home (logged-in landing page)
- [Other sections: tasks, lists, filters, settings, reminders, comments, events]
"""

# Standard library
import json

# Django
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import FormView

# Local apps
from .forms import (
    CommentForm,
    EventForm,
    MyTagsBulkForm,
    TaskForm,
    TypeToDoListForm,
    ReminderForm,
)
from .models import Comment, Event, Reminder, Tag, Task, TypeToDoList


# ---------- AUTH / LANDING ----------

def landing_redirect(request):
    """
    Root redirect:
    - Anonymous users → login page
    - Authenticated users → Home
    """
    if request.user.is_authenticated:
        return redirect("home")
    return redirect("html-login")


def html_logout(request):
    """
    Log the user out and send them to the login page.
    Always uses an explicit redirect instead of the class-based LogoutView
    so the target is unambiguous.
    """
    logout(request)
    return redirect("html-login")


class RegisterView(FormView):
    """
    Simple registration page based on Django's built-in UserCreationForm.
    - If the user is already authenticated, redirect to Home (registration is pointless).
    - On success, create the account and redirect to Login with a success message.
    """
    template_name = "planner/auth_register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("html-login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Account created. Please sign in.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please fix the errors below.")
        return super().form_invalid(form)


# ---------- HOME ----------

@login_required
def home(request):
    """
    Home (app landing) for logged-in users.
    Anonymous users are prevented by @login_required (and also by landing_redirect at '/').
    """
    return render(request, "planner/home.html")


# ---------- TASKS ----------

@login_required
def html_task_list(request):
    """List all tasks owned by the current user."""
    tasks = (
        Task.objects
        .filter(owner=request.user)
        .select_related("list")
        .prefetch_related("tags")
        .order_by("list__name", "title")
    )
    return render(request, "planner/task_list.html", {"tasks": tasks})


@login_required
def html_task_create(request):
    """Create a new task; on POST validate and redirect to task detail upon success."""
    initial = {}
    list_id = request.GET.get("list")
    if list_id:
        try:
            initial["list"] = TypeToDoList.objects.get(pk=list_id, owner=request.user)
        except TypeToDoList.DoesNotExist:
            pass

    if request.method == "POST":
        form = TaskForm(request.user, request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            if task.list.owner_id != request.user.id:
                form.add_error("list", "You cannot add a task to that list.")
            else:
                task.save()
                form.save_m2m()
                messages.success(request, "Task created successfully.")
                return redirect("html-task_detail", pk=task.pk)
    else:
        form = TaskForm(request.user, initial=initial)

    return render(request, "planner/task_form.html", {"form": form, "is_edit": False})


@login_required
def html_task_detail(request, pk):
    """Show task detail (with reminders and optional event), only for owner."""
    qs = (
        Task.objects
        .select_related("event")
        .filter(pk=pk, owner=request.user)
    )
    task = get_object_or_404(qs)

    back_url = request.session.get("back_url")
    ref = (request.META.get("HTTP_REFERER", "") or "").rstrip("/")
    if ref.endswith("/app/tasks"):
        back_url = ref
        request.session["back_url"] = back_url
    elif "/app/lists/" in ref and "/edit" not in ref and "/delete" not in ref:
        back_url = ref
        request.session["back_url"] = back_url

    reminders = task.reminders.order_by("remind_at")
    rform = ReminderForm()

    event = getattr(task, "event", None)
    eform = None
    if event is None:
        eform = EventForm()

    return render(
        request,
        "planner/task_detail.html",
        {
            "task": task,
            "back_url": back_url,
            "reminders": reminders,
            "rform": rform,
            "event": event,
            "eform": eform,
        },
    )


@login_required
def html_task_edit(request, pk):
    """Edit an existing task (owner only); on success redirect to task detail."""
    task = get_object_or_404(Task, pk=pk, owner=request.user)

    if request.method == "POST":
        form = TaskForm(request.user, request.POST, instance=task)
        if form.is_valid():
            chosen_list = form.cleaned_data.get("list")
            if chosen_list and chosen_list.owner_id != request.user.id:
                form.add_error("list", "You cannot move the task to that list.")
            else:
                form.save()
                messages.success(request, "Task updated.")
                return redirect("html-task_detail", pk=task.pk)
    else:
        form = TaskForm(request.user, instance=task)

    back_url = request.session.get("back_url") or None
    return render(
        request,
        "planner/task_form.html",
        {"form": form, "is_edit": True, "task": task, "back_url": back_url},
    )


@login_required
def html_task_delete(request, pk):
    """Confirm and delete a task (owner only); GET = confirm page, POST = delete."""
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == "POST":
        title = task.title
        task.delete()
        messages.success(request, f'Task "{title}" was deleted.')
        return redirect("html-task_list")
    return render(request, "planner/task_confirm_delete.html", {"task": task})


@require_POST
@login_required
def toggle_task_done(request, pk):
    """Toggle or set Task.is_completed; returns JSON with the new boolean state."""
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    done = None

    if "done" in request.POST:
        done_val = str(request.POST.get("done", "")).lower()
        done = done_val in ("1", "true", "on", "yes")

    if done is None:
        try:
            data = json.loads(request.body.decode() or "{}")
        except Exception:
            data = {}
        if "done" in data:
            done = str(data.get("done")).lower() in ("1", "true", "on", "yes")

    if done is None:
        task.is_completed = not task.is_completed
    else:
        task.is_completed = done

    task.save(update_fields=["is_completed"])
    return JsonResponse({"ok": True, "done": task.is_completed})


# ---------- LISTS ----------

@login_required
def html_list_index(request):
    """Show all lists owned by the current user, with task counts."""
    lists = (
        TypeToDoList.objects
        .filter(owner=request.user)
        .annotate(task_count=Count("tasks"))
        .order_by("name")
    )
    return render(request, "planner/typelist_list.html", {"lists": lists})


@login_required
def html_list_detail(request, pk):
    """Show a single list and its tasks for the current user."""
    list_obj = get_object_or_404(TypeToDoList, pk=pk, owner=request.user)
    tasks = (
        Task.objects
        .filter(owner=request.user, list=list_obj)
        .select_related("list")
        .prefetch_related("tags")
        .order_by("-id")
    )
    return render(request, "planner/typelist_detail.html", {"list": list_obj, "tasks": tasks})


@login_required
def html_list_create(request):
    """Create a new list; owner is the current user."""
    if request.method == "POST":
        form = TypeToDoListForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            messages.success(request, "List created.")
            return redirect("html-list_index")
    else:
        form = TypeToDoListForm()
    return render(request, "planner/typelist_form.html", {"form": form, "is_edit": False})


@login_required
def html_list_edit(request, pk):
    """Edit an existing list owned by the current user."""
    obj = get_object_or_404(TypeToDoList, pk=pk, owner=request.user)
    if request.method == "POST":
        form = TypeToDoListForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "List updated.")
            return redirect("html-list_index")
    else:
        form = TypeToDoListForm(instance=obj)
    return render(request, "planner/typelist_form.html", {"form": form, "is_edit": True, "obj": obj})


@login_required
def html_list_delete(request, pk):
    """Confirm and delete a list (owner only); GET = confirm page, POST = delete."""
    obj = get_object_or_404(TypeToDoList, pk=pk, owner=request.user)
    if request.method == "POST":
        name = obj.name
        obj.delete()
        messages.success(request, f'List "{name}" was deleted.')
        return redirect("html-list_index")
    return render(request, "planner/typelist_confirm_delete.html", {"obj": obj})


# ---------- FILTERS ----------

@login_required
def html_filters(request):
    """Filter tasks by search, list, priority, done and tags (AND logic)."""
    user = request.user
    tasks_qs = (
        Task.objects
        .select_related("list")
        .prefetch_related("tags")
        .filter(owner=user)
    )

    lists_qs = TypeToDoList.objects.filter(owner=user).order_by("name")
    tags_qs = Tag.objects.filter(tasks__owner=user).distinct().order_by("name")

    search = (request.GET.get("q") or "").strip()
    list_id = (request.GET.get("list") or "").strip()
    priority = (request.GET.get("priority") or "").strip()
    done = (request.GET.get("done") or "").strip()
    selected_tag_ids = request.GET.getlist("tags")

    if search:
        tasks_qs = tasks_qs.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(list__name__icontains=search) |
            Q(tags__name__icontains=search)
        ).distinct()

    if list_id:
        tasks_qs = tasks_qs.filter(list_id=list_id)
    if priority:
        tasks_qs = tasks_qs.filter(priority=int(priority))
    if done in ("0", "1"):
        tasks_qs = tasks_qs.filter(is_completed=(done == "1"))

    if selected_tag_ids:
        for tid in selected_tag_ids:
            tasks_qs = tasks_qs.filter(tags__id=tid)

    tasks_qs = tasks_qs.order_by("priority", "due_date", "title")

    return render(
        request,
        "planner/filters.html",
        {
            "tasks": tasks_qs,
            "lists": lists_qs,
            "tags": tags_qs,
            "q": search,
            "selected_list_id": list_id,
            "selected_priority": priority,
            "selected_done": done,
            "selected_tag_ids": selected_tag_ids,
        },
    )


# ---------- SETTINGS ----------

@login_required
def html_settings(request):
    """Settings page: manage tag deletion (select-all + permanent delete)."""
    tform = MyTagsBulkForm(request.user, request.POST or None, prefix="tags")
    if request.method == "POST":
        if "tags-delete" in request.POST and tform.is_valid():
            deleted = tform.delete_from_database()
            messages.success(request, f"Deleted {deleted} tag object(s).")
            return redirect("html-settings")
    return render(request, "planner/settings.html", {"tform": tform})


# ---------- REMINDERS ----------

@login_required
@require_POST
def html_reminder_add(request, pk):
    """Add a reminder to a task owned by the current user."""
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    form = ReminderForm(request.POST)
    if form.is_valid():
        rem = form.save(commit=False)
        rem.task = task
        rem.owner = request.user
        rem.save()
        messages.success(request, "Reminder added.")
    else:
        messages.error(request, "Could not add reminder. Check the date/time.")
    return redirect("html-task_detail", pk=task.pk)


@login_required
@require_POST
def html_reminder_delete(request, rid):
    """Delete a reminder (owner only)."""
    reminder = get_object_or_404(Reminder, pk=rid, owner=request.user)
    task_pk = reminder.task_id
    reminder.delete()
    messages.success(request, "Reminder deleted.")
    return redirect("html-task_detail", pk=task_pk)


# ---------- COMMENTS ----------

@login_required
@require_POST
def html_comment_add(request, task_pk):
    """Create a comment on a task owned by the current user."""
    task = get_object_or_404(Task, pk=task_pk, owner=request.user)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.task = task
        comment.author = request.user
        comment.save()
        messages.success(request, "Comment added.")
    else:
        for err in form.errors.get("body", []):
            messages.error(request, err)
    return redirect("html-task_detail", pk=task.pk)


@login_required
@require_POST
def html_comment_delete(request, pk):
    """Delete a comment if requester is the author or the task owner."""
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author_id != request.user.id and comment.task.owner_id != request.user.id:
        messages.error(request, "You cannot delete this comment.")
        return redirect("html-task_detail", pk=comment.task_id)

    task_id = comment.task_id
    comment.delete()
    messages.success(request, "Comment deleted.")
    return redirect("html-task_detail", pk=task_id)


# ---------- EVENTS ----------

@require_POST
@login_required
def html_event_add(request, task_pk):
    """Create a one-off calendar event for the given task (only if none exists)."""
    task = get_object_or_404(Task, pk=task_pk, owner=request.user)
    if hasattr(task, "event"):
        messages.error(request, "This task already has an event.")
        return redirect("html-task_detail", pk=task.pk)

    form = EventForm(request.POST)
    if form.is_valid():
        ev = form.save(commit=False)
        ev.task = task
        ev.full_clean()  # Respect Event.clean() validation.
        ev.save()
        messages.success(request, "Event added.")
    else:
        for f, errs in form.errors.items():
            messages.error(request, f"{f}: {', '.join(errs)}")
    return redirect("html-task_detail", pk=task.pk)


@login_required
def html_event_edit(request, pk):
    """Edit an existing event (task must be owned by the current user)."""
    ev = get_object_or_404(Event, pk=pk, task__owner=request.user)
    if request.method == "POST":
        form = EventForm(request.POST, instance=ev)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated.")
            return redirect("html-task_detail", pk=ev.task_id)
    else:
        form = EventForm(instance=ev)
    return render(request, "planner/event_form.html", {"form": form, "event": ev})


@login_required
def html_event_delete(request, pk):
    """Confirm and delete an event; GET = confirm page, POST = delete."""
    ev = get_object_or_404(Event, pk=pk, task__owner=request.user)
    if request.method == "POST":
        task_id = ev.task_id
        ev.delete()
        messages.success(request, "Event deleted.")
        return redirect("html-task_detail", pk=task_id)
    return render(request, "planner/event_confirm_delete.html", {"event": ev})