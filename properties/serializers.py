from rest_framework import serializers
from .models import Property, PropertyImage


class PropertyImageSerializer(serializers.ModelSerializer):
    """Serializer for property images."""

    class Meta:
        model = PropertyImage
        fields = ['id', 'image', 'is_primary', 'created_at']
        read_only_fields = ['id', 'created_at']


class PropertyListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for property list views."""
    agent_name = serializers.CharField(
        source='agent.user.get_full_name', read_only=True
    )
    primary_image = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = [
            'id', 'title', 'property_type', 'listing_type', 'price',
            'bedrooms', 'bathrooms', 'area_sqft', 'city', 'state',
            'is_featured', 'agent_name', 'primary_image', 'created_at',
        ]

    def get_primary_image(self, obj):
        primary = obj.images.filter(is_primary=True).first()
        if primary:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(primary.image.url)
            return primary.image.url
        return None


class PropertyDetailSerializer(serializers.ModelSerializer):
    """Full serializer for property detail view."""
    images = PropertyImageSerializer(many=True, read_only=True)
    agent_name = serializers.CharField(
        source='agent.user.get_full_name', read_only=True
    )
    agent_id = serializers.IntegerField(source='agent.id', read_only=True)

    class Meta:
        model = Property
        fields = [
            'id', 'title', 'description', 'property_type', 'listing_type',
            'price', 'bedrooms', 'bathrooms', 'area_sqft',
            'address', 'city', 'state', 'zip_code', 'country',
            'latitude', 'longitude',
            'is_featured', 'is_published',
            'agent', 'agent_id', 'agent_name',
            'images', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PropertyCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating properties."""

    class Meta:
        model = Property
        fields = [
            'id', 'title', 'description', 'property_type', 'listing_type',
            'price', 'bedrooms', 'bathrooms', 'area_sqft',
            'address', 'city', 'state', 'zip_code', 'country',
            'latitude', 'longitude',
            'is_featured', 'is_published', 'agent',
        ]
        read_only_fields = ['id']
