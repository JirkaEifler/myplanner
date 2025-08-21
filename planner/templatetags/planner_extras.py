import hashlib
from django import template

register = template.Library()

@register.filter
def list_hue(name: str) -> int:
    """
    Deterministický odstín (0-359) pro daný název listu.
    Nepoužíváme built-in hash (ten je nasolený), ale md5 -> int -> % 360.
    """
    if not name:
        return 200  # fallback
    h = hashlib.md5(name.encode("utf-8")).hexdigest()
    num = int(h[:8], 16)  # stačí část
    return num % 360