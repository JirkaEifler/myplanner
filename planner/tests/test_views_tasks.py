"""
Module: test_views_tasks.py
Purpose: Pytest test cases for Task views in the MyPlanner app.
Covers task list, detail, and create views with login, ownership,
and validation checks.
"""

import pytest
from django.urls import reverse
from planner.models import Task


# ===== TASK LIST =====

def test_task_list_requires_login(client):
    """
    Verify that task list view requires user to be logged in.
    """
    url = reverse("html-task_list")
    resp = client.get(url)
    assert resp.status_code in (302, 301)


def test_task_list_shows_only_current_user_tasks(auth_client, my_task, other_task):
    """
    Verify that task list shows only tasks owned by the current user.
    """
    url = reverse("html-task_list")
    resp = auth_client.get(url)
    assert resp.status_code == 200
    content = resp.content.decode()
    assert "My task" in content
    assert "Bob task" not in content


# ===== TASK DETAIL =====

def test_task_detail_ok_for_owner(auth_client, my_task):
    """
    Verify that a task owner can view their task detail.
    """
    url = reverse("html-task_detail", args=[my_task.pk])
    resp = auth_client.get(url)
    assert resp.status_code == 200
    assert "My task" in resp.content.decode()


def test_task_detail_404_for_foreign_task(auth_client, other_task):
    """
    Verify that accessing another user's task detail returns 404.
    """
    url = reverse("html-task_detail", args=[other_task.pk])
    resp = auth_client.get(url)
    assert resp.status_code == 404


# ===== TASK CREATE =====

def test_task_create_get_renders_form(auth_client):
    """
    Verify that GET request to create task view renders the form.
    """
    url = reverse("html-task_create")
    resp = auth_client.get(url)
    assert resp.status_code == 200
    assert "Title" in resp.content.decode()


def test_task_create_post_creates_task(auth_client, my_list):
    """
    Verify that POST request with valid data creates a new task.
    """
    url = reverse("html-task_create")
    data = {
        "title": "Created from test",
        "description": "desc",
        "list": my_list.pk,
        "priority": 1,
        "is_completed": False,
        "due_date": "",
        "tags": [],
        "new_tags": "",
    }
    before = Task.objects.count()
    resp = auth_client.post(url, data, follow=False)
    assert resp.status_code in (302, 303)
    assert Task.objects.count() == before + 1
    assert Task.objects.filter(title="Created from test").exists()


def test_task_create_cannot_use_foreign_list(auth_client, other_list):
    """
    Verify that creating a task in another user's list is not allowed.
    """
    url = reverse("html-task_create")
    data = {
        "title": "Should not be created",
        "description": "",
        "list": other_list.pk,
        "priority": 2,
        "is_completed": False,
        "due_date": "",
        "tags": [],
        "new_tags": "",
    }
    before = Task.objects.count()
    resp = auth_client.post(url, data)
    assert resp.status_code == 200
    assert Task.objects.count() == before

    html = resp.content.decode()
    assert (
        "You cannot add a task to that list." in html
        or "Select a valid choice" in html
        or "That choice is not one of the available choices" in html
    )