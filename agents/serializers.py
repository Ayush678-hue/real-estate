from rest_framework import serializers
from .models import Agent
from accounts.serializers import UserSerializer


class AgentSerializer(serializers.ModelSerializer):
    """Serializer for agent profiles."""
    user = UserSerializer(read_only=True)
    property_count = serializers.IntegerField(read_only=True)
    specializations_list = serializers.SerializerMethodField()

    class Meta:
        model = Agent
        fields = [
            'id', 'user', 'license_number', 'agency_name', 'bio',
            'experience_years', 'specializations', 'specializations_list',
            'is_verified', 'property_count', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'user', 'is_verified', 'created_at', 'updated_at']

    def get_specializations_list(self, obj):
        if obj.specializations:
            return [s.strip() for s in obj.specializations.split(',')]
        return []


class AgentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating agent profiles."""

    class Meta:
        model = Agent
        fields = [
            'license_number', 'agency_name', 'bio',
            'experience_years', 'specializations',
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        user.user_type = 'agent'
        user.save(update_fields=['user_type'])
        return Agent.objects.create(user=user, **validated_data)
