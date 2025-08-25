"""
Module: planner_extras.py
Purpose: Provide additional custom template filters for MyPlanner.
Includes deterministic color hue generation for list names.
"""

import hashlib
from django import template

register = template.Library()


@register.filter
def list_hue(name: str) -> int:
    """
    Return a deterministic hue (0–359) for the given list name.
    Uses MD5 hashing instead of Python's built-in hash (which is salted),
    converts part of the hash to an integer, and maps it to a hue value.
    """
    if not name:
        return 200  # Fallback hue
    h = hashlib.md5(name.encode("utf-8")).hexdigest()
    num = int(h[:8], 16)  # Use only part of the hash
    return num % 360