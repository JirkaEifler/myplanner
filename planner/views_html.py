from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TaskForm, TypeToDoListForm
from .models import Task, TypeToDoList


# Home page
@login_required
def home(request):
    """Render the app landing page (requires login)."""
    return render(request, "planner/home.html")

# TASKS

# Task List
@login_required
def html_task_list(request):
    """List all tasks owned by the current user (newest first)."""
    tasks = (
        Task.objects
        .filter(owner=request.user)
        .select_related("list")
        .order_by("-id")
    )
    return render(request, "planner/task_list.html", {"tasks": tasks})


# Task Detail
@login_required
def html_task_detail(request, pk):
    """Show details of a single task owned by the current user."""
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    return render(request, "planner/task_detail.html", {"task": task})


# Task Create
@login_required
def html_task_create(request):
    """Create a new task, preselecting a list from ?list=<id> if it belongs to the user."""
    list_id = request.GET.get("list")
    initial = {}

    # Preselect list from ?list=<id>
    if list_id:
        try:
            list_obj = TypeToDoList.objects.get(pk=list_id, owner=request.user)
            initial["list"] = list_obj
        except TypeToDoList.DoesNotExist:
            pass  # ignore foreign/invalid IDs

    if request.method == "POST":
        form = TaskForm(request.user, request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user

            # Extra safety: selected list must be owned by the user
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


# Task Edit
@login_required
def html_task_edit(request, pk):
    """Edit an existing task owned by the current user."""
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

    return render(
        request,
        "planner/task_form.html",
        {"form": form, "is_edit": True, "task": task},
    )


# Task Delete
@login_required
def html_task_delete(request, pk):
    """Show a confirm screen and delete the task on POST (owner only)."""
    task = get_object_or_404(Task, pk=pk, owner=request.user)

    if request.method == "POST":
        title = task.title
        task.delete()
        messages.success(request, f'Task "{title}" was deleted.')
        return redirect("html-task_list")

    return render(request, "planner/task_confirm_delete.html", {"task": task})


# LISTS

# List Index
@login_required
def html_list_index(request):
    """Show all user's lists with task counts."""
    lists = (
        TypeToDoList.objects
        .filter(owner=request.user)
        .annotate(task_count=Count("tasks"))
        .order_by("name")
    )
    return render(request, "planner/typelist_list.html", {"lists": lists})


# List Detail
@login_required
def html_list_detail(request, pk):
    """Show a single list and the user's tasks within it."""
    list_obj = get_object_or_404(TypeToDoList, pk=pk, owner=request.user)
    tasks = (
        Task.objects
        .filter(owner=request.user, list=list_obj)
        .select_related("list")
        .order_by("-id")
    )
    return render(request, "planner/typelist_detail.html", {"list": list_obj, "tasks": tasks})


# List Create
@login_required
def html_list_create(request):
    """Create a new list; the current user becomes the owner."""
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


# List Edit
@login_required
def html_list_edit(request, pk):
    """Edit an existing list (owner only)."""
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


# List Delete
@login_required
def html_list_delete(request, pk):
    """Show a confirm screen and delete the list on POST (owner only)."""
    obj = get_object_or_404(TypeToDoList, pk=pk, owner=request.user)

    if request.method == "POST":
        name = obj.name
        obj.delete()
        messages.success(request, f'List "{name}" was deleted.')
        return redirect("html-list_index")

    return render(request, "planner/typelist_confirm_delete.html", {"obj": obj})