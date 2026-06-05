"""
URL configuration for real_estate project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request):
    """API root listing all available endpoints."""
    return Response({
        'accounts': {
            'register': reverse('accounts:register', request=request),
            'login': reverse('accounts:login', request=request),
            'logout': reverse('accounts:logout', request=request),
            'profile': reverse('accounts:profile', request=request),
        },
        'properties': reverse('properties:property-list', request=request),
        'agents': reverse('agents:agent-list', request=request),
        'inquiries': reverse('inquiries:inquiry-list', request=request),
        'ai_services': {
            'generate_description': reverse('ai_services:generate-description', request=request),
            'estimate_value': reverse('ai_services:estimate-value', request=request),
            'chat': reverse('ai_services:chat', request=request),
            'tag_image': reverse('ai_services:tag-image', request=request),
        },
    })


urlpatterns = [
    # API root
    path('', api_root, name='api-root'),
    path('api/v1/', api_root, name='api-v1-root'),

    path('admin/', admin.site.urls),

    # API v1 endpoints
    path('api/v1/accounts/', include('accounts.urls', namespace='accounts')),
    path('api/v1/properties/', include('properties.urls', namespace='properties')),
    path('api/v1/agents/', include('agents.urls', namespace='agents')),
    path('api/v1/inquiries/', include('inquiries.urls', namespace='inquiries')),
    path('api/v1/ai/', include('ai_services.urls', namespace='ai_services')),

    # DRF browsable API login
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
