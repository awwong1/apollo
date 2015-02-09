from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission for is Administrator, or read only
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_staff:
            return True
        return False