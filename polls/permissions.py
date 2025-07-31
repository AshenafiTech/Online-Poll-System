"""
This file is now deprecated. All permissions have been moved to polls/api/permissions.py.
"""
from rest_framework import permissions
from rest_framework import permissions

class IsPollCreatorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the creator of a poll to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the creator
        return obj.created_by == request.user
