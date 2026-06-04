from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .models import Inquiry
from .serializers import InquirySerializer, InquiryUpdateSerializer


class IsAgentOwnerOrAdmin(permissions.BasePermission):
    """Only the property's agent or admin can view/update inquiries."""

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.property.agent.user == request.user


class InquiryViewSet(viewsets.ModelViewSet):
    """ViewSet for property inquiries."""
    queryset = Inquiry.objects.select_related(
        'property', 'property__agent', 'property__agent__user', 'sender'
    ).all()

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return InquiryUpdateSerializer
        return InquirySerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsAgentOwnerOrAdmin()]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Inquiry.objects.none()
        if user.is_staff:
            return self.queryset
        if hasattr(user, 'agent_profile'):
            return self.queryset.filter(property__agent__user=user)
        return self.queryset.filter(sender=user)
