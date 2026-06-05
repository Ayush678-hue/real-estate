"""
Serializers for AI Services API endpoints.
"""

from rest_framework import serializers


class GenerateDescriptionSerializer(serializers.Serializer):
    """Input serializer for AI property description generation."""
    property_id = serializers.IntegerField(
        help_text="ID of the property to generate a description for."
    )
    save = serializers.BooleanField(
        default=False,
        help_text="If true, saves the generated description to the property."
    )


class DescriptionResponseSerializer(serializers.Serializer):
    """Output serializer for generated description."""
    property_id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    saved = serializers.BooleanField()


class EstimateValueSerializer(serializers.Serializer):
    """Input serializer for property valuation."""
    property_type = serializers.ChoiceField(
        choices=['house', 'apartment', 'condo', 'land', 'commercial'],
        help_text="Type of property."
    )
    bedrooms = serializers.IntegerField(
        min_value=0,
        help_text="Number of bedrooms."
    )
    bathrooms = serializers.IntegerField(
        min_value=0,
        required=False,
        default=1,
        help_text="Number of bathrooms."
    )
    area_sqft = serializers.FloatField(
        min_value=0,
        help_text="Area in square feet."
    )
    city = serializers.CharField(
        max_length=100,
        help_text="City name."
    )
    state = serializers.CharField(
        max_length=100,
        required=False,
        default='',
        help_text="State name."
    )


class ValuationResponseSerializer(serializers.Serializer):
    """Output serializer for property valuation."""
    estimated_price = serializers.IntegerField(allow_null=True)
    price_range = serializers.DictField()
    confidence = serializers.CharField()
    comparable_count = serializers.IntegerField()
    comparable_properties = serializers.ListField()
    analysis = serializers.CharField()


class ChatSerializer(serializers.Serializer):
    """Input serializer for chatbot messages."""
    message = serializers.CharField(
        max_length=2000,
        help_text="Your message to the real estate assistant."
    )
    session_id = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Session ID for multi-turn conversation. Omit to start a new chat."
    )


class ChatResponseSerializer(serializers.Serializer):
    """Output serializer for chatbot response."""
    session_id = serializers.CharField()
    reply = serializers.CharField()
    property_ids = serializers.ListField(child=serializers.IntegerField())
    properties = serializers.ListField()


class TagImageSerializer(serializers.Serializer):
    """Input serializer for image auto-tagging."""
    image = serializers.ImageField(
        required=False,
        help_text="Upload a property image to analyze."
    )
    property_image_id = serializers.IntegerField(
        required=False,
        help_text="ID of an existing PropertyImage to analyze."
    )

    def validate(self, attrs):
        if not attrs.get('image') and not attrs.get('property_image_id'):
            raise serializers.ValidationError(
                "Provide either 'image' (file upload) or 'property_image_id'."
            )
        return attrs


class TagImageResponseSerializer(serializers.Serializer):
    """Output serializer for image tags."""
    tags = serializers.ListField(child=serializers.CharField())
    room_type = serializers.CharField()
    description = serializers.CharField()
    quality_score = serializers.FloatField()
