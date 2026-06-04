from django.contrib import admin
from .models import Property, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'property_type', 'listing_type', 'price',
        'city', 'state', 'agent', 'is_featured', 'is_published',
        'created_at',
    ]
    list_filter = [
        'property_type', 'listing_type', 'is_featured',
        'is_published', 'city', 'state',
    ]
    search_fields = ['title', 'description', 'address', 'city']
    inlines = [PropertyImageInline]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ['property', 'is_primary', 'created_at']
    list_filter = ['is_primary']
