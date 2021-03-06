#--- IOT_Server - api app custom permissions-----------------------------------
#--- Original Release: December 2018
#--- By: Conrad Eggan
#--- Email: Conrade@RedCatMfg.com

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


class IsSuperUser(permissions.BasePermission):
    """
    Custom permission allows only superuser access.
    """
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_superuser

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class IsStaff(permissions.BasePermission):
    """
    Custom permission allows only staff access.
    """
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_staff


class GetOnlyUnlessIsStaff(permissions.BasePermission):
    """
    Allows get only unless Staff member
    """
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        #Otherwise must be staff
        return request.user and request.user.is_staff