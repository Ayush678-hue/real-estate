"""
AI-Powered Property Description Generator.

Generates compelling marketing copy for property listings by building
structured prompts from property attributes and calling Gemini.
"""

import logging
from properties.models import Property
from ai_services.gemini_client import generate_text

logger = logging.getLogger(__name__)


def generate_property_description(property_id, save_to_property=False):
    """
    Generate an AI-powered marketing description for a property.

    Args:
        property_id: The ID of the property to describe.
        save_to_property: If True, updates the property's description field.

    Returns:
        dict with 'description' and 'property_id'.
    """
    try:
        prop = Property.objects.select_related('agent', 'agent__user').get(
            pk=property_id
        )
    except Property.DoesNotExist:
        raise ValueError(f"Property with ID {property_id} does not exist.")

    prompt = _build_prompt(prop)
    description = generate_text(prompt, temperature=0.8, max_tokens=1024)

    # Clean up potential markdown formatting from the response
    description = description.strip()
    if description.startswith('"') and description.endswith('"'):
        description = description[1:-1]

    if save_to_property:
        prop.description = description
        prop.save(update_fields=['description'])
        logger.info(f"Updated description for property #{property_id}")

    return {
        'property_id': prop.id,
        'title': prop.title,
        'description': description,
        'saved': save_to_property,
    }


def _build_prompt(prop):
    """Build a structured prompt from property attributes."""
    listing_label = "For Sale" if prop.listing_type == 'sale' else "For Rent"
    price_label = f"₹{prop.price:,.0f}"

    features = []
    if prop.bedrooms > 0:
        features.append(f"{prop.bedrooms} bedroom(s)")
    if prop.bathrooms > 0:
        features.append(f"{prop.bathrooms} bathroom(s)")
    if prop.area_sqft:
        features.append(f"{prop.area_sqft:,.0f} sq ft")

    features_str = ", ".join(features) if features else "Not specified"

    prompt = f"""You are an expert real estate copywriter. Write a compelling, professional
marketing description for this property listing. The description should be
engaging, highlight key selling points, and be 150-250 words long.

**Property Details:**
- Title: {prop.title}
- Type: {prop.get_property_type_display()}
- Listing: {listing_label}
- Price: {price_label}
- Features: {features_str}
- Address: {prop.address}
- City: {prop.city}, {prop.state}
- Country: {prop.country}

**Instructions:**
1. Write in a warm, professional tone
2. Highlight the property type and key features prominently
3. Mention the neighborhood/city as a selling point
4. Include a compelling opening line and a strong call-to-action at the end
5. Do NOT include the price in the description
6. Do NOT use excessive exclamation marks
7. Return ONLY the description text, no headers or labels
"""
    return prompt
