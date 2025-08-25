"""
Module: list_extras.py
Purpose: Provide custom template filters for MyPlanner.
Contains filters used for dynamic styling of lists.
"""

from django import template

register = template.Library()


@register.filter
def list_hue(value):
    """
    Convert a list name into a numeric hue value for CSS styling.
    Uses Python's built-in hash and maps the result into a 0–359 range.
    """
    if not value:
        return 0
    return hash(value) % 360