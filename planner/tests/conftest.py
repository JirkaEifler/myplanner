"""
Module: conftest.py
Purpose: Shared pytest fixtures for the MyPlanner project.
Provides test users, authenticated clients, and sample lists/tasks.
"""

import pytest
from planner.models import TypeToDoList, Task


@pytest.fixture
def user(django_user_model):
    """
    Create and return a test user (Anna).
    """
    return django_user_model.objects.create_user(
        username="anna", email="anna@gmail.com", password="heslo1234"
    )


@pytest.fixture
def other_user(django_user_model):
    """
    Create and return a second test user (Tom).
    """
    return django_user_model.objects.create_user(
        username="tom", email="tom@gmail.com", password="heslo1234"
    )


@pytest.fixture
def auth_client(client, user):
    """
    Return a Django test client logged in as `user`.
    """
    client.login(username="anna", password="heslo1234")
    return client


@pytest.fixture
def my_list(user):
    """
    Create and return a to-do list owned by `user`.
    """
    return TypeToDoList.objects.create(name="My list", owner=user)


@pytest.fixture
def other_list(other_user):
    """
    Create and return a to-do list owned by `other_user`.
    """
    return TypeToDoList.objects.create(name="Tom list", owner=other_user)


@pytest.fixture
def my_task(user, my_list):
    """
    Create and return a task owned by `user` in `my_list`.
    """
    return Task.objects.create(
        title="My task", owner=user, list=my_list, priority=1
    )


@pytest.fixture
def other_task(other_user, other_list):
    """
    Create and return a task owned by `other_user` in `other_list`.
    """
    return Task.objects.create(
        title="Tom task", owner=other_user, list=other_list, priority=2
    )