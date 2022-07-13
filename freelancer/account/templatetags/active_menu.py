from django import template
from django.urls import reverse

register = template.Library()


@register.filter
def is_active(request, item_name):
    """
    Identify the selected menu item.

    Returns:
    --------
        return the active class name or none.
    """
    url_path = request.path.split("/")[-2]
    if item_name in url_path:
        return "active"
    else:
        return 