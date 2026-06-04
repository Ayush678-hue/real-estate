from rest_framework import serializers
from .models import Inquiry


class InquirySerializer(serializers.ModelSerializer):
    """Serializer for property inquiries."""
    property_title = serializers.CharField(
        source='property.title', read_only=True
    )
    sender_username = serializers.CharField(
        source='sender.username', read_only=True, default=None
    )

    class Meta:
        model = Inquiry
        fields = [
            'id', 'property', 'property_title', 'sender', 'sender_username',
            'name', 'email', 'phone', 'message', 'status', 'created_at',
        ]
        read_only_fields = ['id', 'sender', 'status', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['sender'] = request.user
        return super().create(validated_data)


class InquiryUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating inquiry status."""

    class Meta:
        model = Inquiry
        fields = ['status']
