from django.contrib import admin
from .models import Agent


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'agency_name', 'license_number',
        'experience_years', 'is_verified', 'created_at',
    ]
    list_filter = ['is_verified', 'experience_years']
    search_fields = [
        'user__username', 'user__email', 'agency_name', 'license_number',
    ]
    readonly_fields = ['created_at', 'updated_at']
