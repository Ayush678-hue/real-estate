from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Agent
from .serializers import AgentSerializer, AgentCreateSerializer
from properties.serializers import PropertyListSerializer


class AgentViewSet(viewsets.ModelViewSet):
    """ViewSet for agent profiles."""
    queryset = Agent.objects.select_related('user').all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return AgentCreateSerializer
        return AgentSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def perform_update(self, serializer):
        """Only allow agents to update their own profiles."""
        if serializer.instance.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('You can only update your own profile.')
        serializer.save()

    @action(detail=True, methods=['get'])
    def properties(self, request, pk=None):
        """List all properties belonging to this agent."""
        agent = self.get_object()
        properties = agent.properties.filter(is_published=True)
        page = self.paginate_queryset(properties)
        if page is not None:
            serializer = PropertyListSerializer(
                page, many=True, context={'request': request}
            )
            return self.get_paginated_response(serializer.data)
        serializer = PropertyListSerializer(
            properties, many=True, context={'request': request}
        )
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='top-agents')
    def top_agents(self, request):
        """List top/verified agents."""
        top = self.get_queryset().filter(is_verified=True)
        page = self.paginate_queryset(top)
        if page is not None:
            serializer = AgentSerializer(
                page, many=True, context={'request': request}
            )
            return self.get_paginated_response(serializer.data)
        serializer = AgentSerializer(
            top, many=True, context={'request': request}
        )
        return Response(serializer.data)
