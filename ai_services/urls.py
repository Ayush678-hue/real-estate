"""
URL configuration for AI Services.
"""

from django.urls import path
from . import views

app_name = 'ai_services'

urlpatterns = [
    path(
        'generate-description/',
        views.GenerateDescriptionView.as_view(),
        name='generate-description',
    ),
    path(
        'estimate-value/',
        views.EstimateValueView.as_view(),
        name='estimate-value',
    ),
    path(
        'chat/',
        views.ChatView.as_view(),
        name='chat',
    ),
    path(
        'tag-image/',
        views.TagImageView.as_view(),
        name='tag-image',
    ),
]
