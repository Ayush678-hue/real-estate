from rest_framework import viewsets, permissions, status, parsers
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Property, PropertyImage
from .serializers import (
    PropertyListSerializer,
    PropertyDetailSerializer,
    PropertyCreateUpdateSerializer,
    PropertyImageSerializer,
)
from .filters import PropertyFilter
from .permissions import IsAgentOrReadOnly, IsOwnerAgentOrReadOnly


class PropertyViewSet(viewsets.ModelViewSet):
    """ViewSet for property CRUD operations."""
    queryset = Property.objects.filter(is_published=True).select_related(
        'agent', 'agent__user'
    ).prefetch_related('images')
    permission_classes = [IsAgentOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PropertyFilter
    search_fields = ['title', 'description', 'address', 'city']
    ordering_fields = ['price', 'created_at', 'area_sqft', 'bedrooms']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return PropertyListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return PropertyCreateUpdateSerializer
        return PropertyDetailSerializer

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Return featured properties."""
        featured = self.get_queryset().filter(is_featured=True)
        page = self.paginate_queryset(featured)
        if page is not None:
            serializer = PropertyListSerializer(
                page, many=True, context={'request': request}
            )
            return self.get_paginated_response(serializer.data)
        serializer = PropertyListSerializer(
            featured, many=True, context={'request': request}
        )
        return Response(serializer.data)


class PropertyImageViewSet(viewsets.ModelViewSet):
    """ViewSet for managing property images."""
    serializer_class = PropertyImageSerializer
    permission_classes = [IsOwnerAgentOrReadOnly]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get_queryset(self):
        return PropertyImage.objects.filter(
            property_id=self.kwargs['property_pk']
        )

    def perform_create(self, serializer):
        property_obj = Property.objects.get(pk=self.kwargs['property_pk'])
        serializer.save(property=property_obj)
