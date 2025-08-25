"""App configuration for the Planner Django application."""

from django.apps import AppConfig


class PlannerConfig(AppConfig):
    """Configuration for the Planner app."""
    default_auto_field = "django.db.models.BigAutoField"
    name = "planner"