from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'properties'

router = DefaultRouter()
router.register(r'', views.PropertyViewSet, basename='property')

urlpatterns = [
    path(
        '<int:property_pk>/images/',
        views.PropertyImageViewSet.as_view({
            'get': 'list',
            'post': 'create',
        }),
        name='property-images',
    ),
    path(
        '<int:property_pk>/images/<int:pk>/',
        views.PropertyImageViewSet.as_view({
            'get': 'retrieve',
            'delete': 'destroy',
        }),
        name='property-image-detail',
    ),
    path('', include(router.urls)),
]
