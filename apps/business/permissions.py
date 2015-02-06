from rest_framework import permissions


class BusinessPermissions(permissions.BasePermission):
    """
    Custom permission to only allow:

    - Any user to GET, OPTIONS, HEAD
    - Authenticated users to POST
    - Authenticated and business_administrator users to PUT, PATCH
    """

    def has_object_permission(self, request, view, obj=None):
        """
        Permissions for specific business instances
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated():
            if request.method == 'POST':
                return True
            elif obj and request.method in ('PUT', 'PATCH'):
                return request.user.has_perm("business.change_business", obj)
        return False

    def has_permission(self, request, view):
        """
        Permissions for all businesses
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated():
            if request.method == 'POST':
                return True
            elif request.method in ('PUT', 'PATCH'):
                # Handled by Object Permissions
                return True
        return False