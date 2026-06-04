from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'inquiries'

router = DefaultRouter()
router.register(r'', views.InquiryViewSet, basename='inquiry')

urlpatterns = [
    path('', include(router.urls)),
]
