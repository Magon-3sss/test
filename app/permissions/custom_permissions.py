from rest_framework import permissions

class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Your custom logic to determine if the user has permission
        return request.user.is_authenticated  # Check if the user is authenticated
