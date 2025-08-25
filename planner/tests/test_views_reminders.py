"""
Module: test_views_reminders.py
Purpose: Pytest test cases for Reminder views in the MyPlanner app.
Covers adding and deleting reminders, with checks for authentication
and ownership validation.
"""

import pytest
from datetime import timedelta
from django.urls import reverse
from django.utils import timezone

from planner.models import Reminder


# ===== ADD REMINDER =====

def test_add_reminder_requires_login(client, my_task):
    """
    Verify that adding a reminder without login redirects to login page.
    """
    url = reverse("html-reminder_add", args=[my_task.pk])
    resp = client.post(url, {"remind_at": "2030-01-01T09:00", "note": "ping"})
    assert resp.status_code in (302, 301)


def test_add_reminder_ok_for_owner(auth_client, my_task):
    """
    Verify that the task owner can successfully add a reminder.
    """
    url = reverse("html-reminder_add", args=[my_task.pk])
    when = (timezone.now() + timedelta(days=1)).replace(microsecond=0)
    data = {"remind_at": when.strftime("%Y-%m-%dT%H:%M"), "note": "call mom"}

    before = Reminder.objects.filter(task=my_task).count()
    resp = auth_client.post(url, data, follow=False)

    assert resp.status_code in (302, 303)
    after = Reminder.objects.filter(task=my_task).count()
    assert after == before + 1

    r = Reminder.objects.filter(task=my_task).latest("id")
    assert r.note == "call mom"
    assert abs((r.remind_at - when).total_seconds()) < 60


def test_cannot_add_reminder_to_foreign_task(auth_client, other_task):
    """
    Verify that a user cannot add a reminder to another user's task.
    """
    url = reverse("html-reminder_add", args=[other_task.pk])
    when = (timezone.now() + timedelta(days=1)).replace(microsecond=0)
    data = {"remind_at": when.strftime("%Y-%m-%dT%H:%M"), "note": "nope"}

    before = Reminder.objects.count()
    resp = auth_client.post(url, data)
    assert resp.status_code == 404
    assert Reminder.objects.count() == before


# ===== DELETE REMINDER =====

def test_delete_reminder_ok_for_owner(auth_client, my_task):
    """
    Verify that the task owner can delete their reminder successfully.
    """
    r = Reminder.objects.create(
        task=my_task,
        owner=my_task.owner,
        remind_at=(timezone.now() + timedelta(days=2)),
        note="tmp"
    )
    url = reverse("html-reminder_delete", args=[r.pk])

    before = Reminder.objects.filter(task=my_task).count()
    resp = auth_client.post(url, follow=False)

    assert resp.status_code in (302, 303)
    assert Reminder.objects.filter(task=my_task).count() == before - 1
    assert not Reminder.objects.filter(pk=r.pk).exists()


def test_cannot_delete_foreign_reminder(auth_client, other_task):
    """
    Verify that a user cannot delete another user's reminder.
    """
    r = Reminder.objects.create(
        task=other_task,
        owner=other_task.owner,
        remind_at=(timezone.now() + timedelta(days=2)),
        note="foreign"
    )
    url = reverse("html-reminder_delete", args=[r.pk])

    before = Reminder.objects.count()
    resp = auth_client.post(url)
    assert resp.status_code == 404
    assert Reminder.objects.count() == before