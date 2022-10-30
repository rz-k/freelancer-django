from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """The author or admin can use CRUD actions but
      Other users can only retrieve the data"""

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True

        if request.user == obj.user or request.user.is_superuser:
            return True
