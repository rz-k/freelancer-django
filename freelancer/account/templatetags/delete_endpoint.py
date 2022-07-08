from django import template
from django.urls import reverse

register = template.Library()


@register.filter
def get_delete_endpoint(job_object, id):
    """
    Return the delete endpoint for the related model instance.
    """
    if job_object.__class__.__name__ == "Project":
        end_point = reverse("project:delete-project", kwargs={"id": id})
    else:
        end_point = reverse("job:delete-job", kwargs={"id": id})

    return end_point
