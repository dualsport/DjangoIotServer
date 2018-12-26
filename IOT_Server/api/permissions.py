from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to allow only owners of an object to view or edit.
    """

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        else:
            return False

