import random

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def get_job_tags(job_tags):
    """
    Add style(radom background-color) and <a> tags to each job tag.    
    """
    tags = job_tags.split(",")
    style_tags = ""
    color_tag = ["#ffc5f5", "#9777fa1f", "#c9ffc5", "#feffc5", "#ffcfc5", "#c5e3ff", "#c5fffc", "#c5ccff"]

    for tag in tags:
        style_tags += f"""
            <a href="#" class="btn tag-btn" style="background-color: {random.choice(color_tag)}">
            {tag}
            </a>"""
    return mark_safe(style_tags)
