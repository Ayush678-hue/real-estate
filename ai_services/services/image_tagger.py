"""
Image Auto-Tagger.

Analyzes property images using Gemini's vision capabilities to
automatically detect and tag features (room type, amenities, quality).
"""

import json
import logging
from ai_services.gemini_client import generate_with_image

logger = logging.getLogger(__name__)


def tag_image(image_file=None, image_bytes=None, mime_type="image/jpeg",
              property_image_id=None):
    """
    Analyze a property image and generate auto-tags.

    Args:
        image_file: A Django UploadedFile or file-like object.
        image_bytes: Raw image bytes (alternative to image_file).
        mime_type: MIME type of the image.
        property_image_id: Optional PropertyImage ID to update with tags.

    Returns:
        dict with tags, room_type, description, and quality_score.
    """
    # Read image data
    if image_file:
        img_data = image_file.read()
        # Detect MIME type from content_type if available
        if hasattr(image_file, 'content_type'):
            mime_type = image_file.content_type
    elif image_bytes:
        img_data = image_bytes
    else:
        raise ValueError("Either image_file or image_bytes must be provided.")

    prompt = _build_prompt()

    try:
        response_text = generate_with_image(
            prompt=prompt,
            image_data=img_data,
            mime_type=mime_type,
            temperature=0.3,
            max_tokens=1024,
        )

        result = _parse_response(response_text)
    except Exception as e:
        logger.error(f"Image tagging failed: {e}")
        result = {
            'tags': [],
            'room_type': 'unknown',
            'description': 'Unable to analyze image.',
            'quality_score': 0,
            'error': str(e),
        }

    # Save tags to PropertyImage if provided
    if property_image_id and 'error' not in result:
        _save_tags(property_image_id, result)

    return result


def tag_property_image(property_image_id):
    """
    Analyze an existing PropertyImage by its ID.

    Args:
        property_image_id: ID of the PropertyImage model instance.

    Returns:
        dict with tags, room_type, description, and quality_score.
    """
    from properties.models import PropertyImage

    try:
        prop_image = PropertyImage.objects.get(pk=property_image_id)
    except PropertyImage.DoesNotExist:
        raise ValueError(
            f"PropertyImage with ID {property_image_id} does not exist."
        )

    # Read the image file
    with prop_image.image.open('rb') as f:
        img_data = f.read()

    # Determine MIME type from filename
    name = prop_image.image.name.lower()
    if name.endswith('.png'):
        mime_type = 'image/png'
    elif name.endswith('.webp'):
        mime_type = 'image/webp'
    else:
        mime_type = 'image/jpeg'

    return tag_image(
        image_bytes=img_data,
        mime_type=mime_type,
        property_image_id=property_image_id,
    )


def _build_prompt():
    """Build the image analysis prompt."""
    return """Analyze this real estate property image. Return a JSON object with exactly
these fields (no markdown, no code fences, just raw JSON):

{
    "tags": ["tag1", "tag2", ...],
    "room_type": "type of room or area",
    "description": "A 1-2 sentence description of what you see",
    "quality_score": 7.5
}

**Tag Guidelines:**
- Include 5-10 descriptive tags
- Tags should describe: room type, materials, style, features, condition
- Example tags: "kitchen", "hardwood_floors", "modern", "natural_light",
  "granite_countertop", "open_plan", "swimming_pool", "garden", "balcony",
  "marble", "spacious", "well_maintained", "newly_renovated"

**Room Type Options:**
- bedroom, kitchen, bathroom, living_room, dining_room, balcony, terrace,
  garden, swimming_pool, garage, exterior, lobby, office, laundry, storage

**Quality Score:**
- Rate the image quality and appeal from 1.0 (poor) to 10.0 (excellent)
- Consider: lighting, composition, cleanliness, staging, overall appeal

Return ONLY the JSON object, nothing else."""


def _parse_response(response_text):
    """Parse the Gemini response into a structured dict."""
    # Clean up potential markdown code fences
    text = response_text.strip()
    if text.startswith('```'):
        text = text.split('\n', 1)[-1]
    if text.endswith('```'):
        text = text.rsplit('```', 1)[0]
    text = text.strip()

    try:
        data = json.loads(text)
        return {
            'tags': data.get('tags', []),
            'room_type': data.get('room_type', 'unknown'),
            'description': data.get('description', ''),
            'quality_score': float(data.get('quality_score', 0)),
        }
    except (json.JSONDecodeError, ValueError) as e:
        logger.warning(f"Failed to parse image tagger response: {e}")
        return {
            'tags': [],
            'room_type': 'unknown',
            'description': text[:200],
            'quality_score': 0,
        }


def _save_tags(property_image_id, result):
    """Save auto-generated tags to the PropertyImage model."""
    from properties.models import PropertyImage

    try:
        prop_image = PropertyImage.objects.get(pk=property_image_id)
        prop_image.auto_tags = result
        prop_image.save(update_fields=['auto_tags'])
        logger.info(
            f"Saved auto-tags for PropertyImage #{property_image_id}"
        )
    except PropertyImage.DoesNotExist:
        logger.warning(
            f"PropertyImage #{property_image_id} not found for tag saving."
        )
