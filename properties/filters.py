import django_filters
from .models import Property


class PropertyFilter(django_filters.FilterSet):
    """Filter set for property listings."""
    price_min = django_filters.NumberFilter(
        field_name='price', lookup_expr='gte'
    )
    price_max = django_filters.NumberFilter(
        field_name='price', lookup_expr='lte'
    )
    bedrooms_min = django_filters.NumberFilter(
        field_name='bedrooms', lookup_expr='gte'
    )
    bathrooms_min = django_filters.NumberFilter(
        field_name='bathrooms', lookup_expr='gte'
    )
    area_min = django_filters.NumberFilter(
        field_name='area_sqft', lookup_expr='gte'
    )
    area_max = django_filters.NumberFilter(
        field_name='area_sqft', lookup_expr='lte'
    )
    search = django_filters.CharFilter(
        method='search_filter', label='Search'
    )

    class Meta:
        model = Property
        fields = [
            'property_type', 'listing_type', 'city', 'state',
            'country', 'is_featured',
        ]

    def search_filter(self, queryset, name, value):
        """Search across title, description, and address."""
        from django.db.models import Q
        return queryset.filter(
            Q(title__icontains=value)
            | Q(description__icontains=value)
            | Q(address__icontains=value)
            | Q(city__icontains=value)
        )
