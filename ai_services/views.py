"""
API views for all AI Services.
"""

import logging
from rest_framework import status, permissions, parsers
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    GenerateDescriptionSerializer,
    DescriptionResponseSerializer,
    EstimateValueSerializer,
    ValuationResponseSerializer,
    ChatSerializer,
    ChatResponseSerializer,
    TagImageSerializer,
    TagImageResponseSerializer,
)

logger = logging.getLogger(__name__)


class GenerateDescriptionView(APIView):
    """
    Generate an AI-powered marketing description for a property listing.

    POST /api/v1/ai/generate-description/
    Body: { "property_id": 5, "save": false }
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request):
        serializer = GenerateDescriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        from .services.description_generator import generate_property_description

        try:
            result = generate_property_description(
                property_id=serializer.validated_data['property_id'],
                save_to_property=serializer.validated_data.get('save', False),
            )
            return Response(
                DescriptionResponseSerializer(result).data,
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logger.error(f"Description generation failed: {e}")
            return Response(
                {'error': f'AI service error: {str(e)}'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


class EstimateValueView(APIView):
    """
    Estimate the market value of a property based on comparable listings.

    POST /api/v1/ai/estimate-value/
    Body: { "property_type": "apartment", "bedrooms": 3, "area_sqft": 1500, "city": "Mumbai" }
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = EstimateValueSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        from .services.valuation import estimate_property_value

        try:
            result = estimate_property_value(serializer.validated_data)
            return Response(
                ValuationResponseSerializer(result).data,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(f"Valuation failed: {e}")
            return Response(
                {'error': f'AI service error: {str(e)}'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


class ChatView(APIView):
    """
    Chat with the AI real estate assistant.

    POST /api/v1/ai/chat/
    Body: { "message": "Show me apartments in Mumbai", "session_id": "optional-uuid" }
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        from .services.chatbot import chat

        try:
            result = chat(
                message=serializer.validated_data['message'],
                session_id=serializer.validated_data.get('session_id'),
            )
            return Response(
                ChatResponseSerializer(result).data,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(f"Chatbot error: {e}")
            return Response(
                {'error': f'AI service error: {str(e)}'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


class TagImageView(APIView):
    """
    Analyze a property image and auto-generate feature tags.

    POST /api/v1/ai/tag-image/
    Body (multipart): { "image": <file> } or { "property_image_id": 5 }
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]

    def post(self, request):
        serializer = TagImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        from .services.image_tagger import tag_image, tag_property_image

        try:
            if serializer.validated_data.get('property_image_id'):
                result = tag_property_image(
                    serializer.validated_data['property_image_id']
                )
            else:
                result = tag_image(
                    image_file=serializer.validated_data['image'],
                )

            return Response(
                TagImageResponseSerializer(result).data,
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logger.error(f"Image tagging failed: {e}")
            return Response(
                {'error': f'AI service error: {str(e)}'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
