from rest_framework import permissions


class IsAgentOrReadOnly(permissions.BasePermission):
    """Allow agents to create/edit properties; others can only read."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated
            and hasattr(request.user, 'agent_profile')
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.agent.user == request.user


class IsOwnerAgentOrReadOnly(permissions.BasePermission):
    """Only the agent who owns the property can modify it."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.agent.user == request.user
