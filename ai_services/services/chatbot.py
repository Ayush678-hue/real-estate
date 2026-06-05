"""
Real Estate AI Chatbot.

Conversational assistant that answers buyer questions about properties,
neighborhoods, and the platform using Gemini with property database context.
"""

import json
import logging
import uuid
from django.db.models import Q
from properties.models import Property
from ai_services.gemini_client import generate_chat

logger = logging.getLogger(__name__)

SYSTEM_INSTRUCTION = """You are a friendly, knowledgeable real estate assistant for an Indian
real estate platform. Your job is to help buyers find properties, answer
questions about listings, and provide helpful advice.

**Your capabilities:**
- Search and recommend properties based on buyer preferences
- Answer questions about specific property listings
- Provide general real estate buying/renting advice
- Explain property features and neighborhood information

**Rules:**
1. Only recommend properties that exist in the provided context
2. If no matching properties are found, say so honestly
3. Always be polite, professional, and helpful
4. When listing properties, include key details (title, price, bedrooms, city)
5. Use Indian Rupee (₹) for all prices
6. If a question is not related to real estate, politely redirect the conversation
7. Keep responses concise but informative (under 200 words)
"""


def chat(message, session_id=None):
    """
    Process a chat message and return an AI response with relevant properties.

    Args:
        message: The user's message text.
        session_id: Optional session ID for multi-turn conversation.

    Returns:
        dict with session_id, reply, and matching property IDs.
    """
    from ai_services.models import ChatSession, ChatMessage

    # Get or create session
    if session_id:
        try:
            session = ChatSession.objects.get(session_id=session_id)
        except ChatSession.DoesNotExist:
            session = ChatSession.objects.create(session_id=session_id)
    else:
        session = ChatSession.objects.create()

    # Save user message
    ChatMessage.objects.create(
        session=session,
        role='user',
        content=message,
    )

    # Find relevant properties based on the message
    relevant_properties = _search_properties(message)
    property_context = _build_property_context(relevant_properties)

    # Build conversation history
    history = _build_history(session)

    # Add property context to the latest message
    enhanced_message = message
    if property_context:
        enhanced_message = (
            f"{message}\n\n"
            f"[AVAILABLE PROPERTIES FROM DATABASE]\n{property_context}"
        )

    # Replace the last message with the enhanced version
    if history:
        history[-1] = {'role': 'user', 'parts': enhanced_message}
    else:
        history.append({'role': 'user', 'parts': enhanced_message})

    # Get AI response
    try:
        reply = generate_chat(
            messages=history,
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.7,
            max_tokens=1024,
        )
    except Exception as e:
        logger.error(f"Chatbot error: {e}")
        reply = (
            "I'm sorry, I'm having trouble processing your request right now. "
            "Please try again in a moment."
        )

    # Save assistant reply
    ChatMessage.objects.create(
        session=session,
        role='model',
        content=reply,
    )

    # Extract property IDs from the relevant results
    property_ids = [p.id for p in relevant_properties[:5]]

    return {
        'session_id': str(session.session_id),
        'reply': reply,
        'property_ids': property_ids,
        'properties': _serialize_properties(relevant_properties[:5]),
    }


def _search_properties(message):
    """Extract search criteria from the message and query the database."""
    msg_lower = message.lower()
    filters = Q(is_published=True)

    # Property type detection
    type_map = {
        'apartment': 'apartment', 'flat': 'apartment',
        'house': 'house', 'villa': 'house', 'bungalow': 'house',
        'condo': 'condo', 'condominium': 'condo',
        'land': 'land', 'plot': 'land',
        'commercial': 'commercial', 'office': 'commercial', 'shop': 'commercial',
    }
    for keyword, ptype in type_map.items():
        if keyword in msg_lower:
            filters &= Q(property_type=ptype)
            break

    # Listing type detection
    if any(w in msg_lower for w in ['rent', 'rental', 'lease']):
        filters &= Q(listing_type='rent')
    elif any(w in msg_lower for w in ['buy', 'purchase', 'sale']):
        filters &= Q(listing_type='sale')

    # Price detection (basic patterns like "under 50 lakh", "below 1 crore")
    import re
    price_patterns = [
        (r'under\s+(\d+)\s*(?:lakh|lac|l)', lambda m: int(m.group(1)) * 100000),
        (r'below\s+(\d+)\s*(?:lakh|lac|l)', lambda m: int(m.group(1)) * 100000),
        (r'under\s+(\d+)\s*(?:crore|cr)', lambda m: int(m.group(1)) * 10000000),
        (r'below\s+(\d+)\s*(?:crore|cr)', lambda m: int(m.group(1)) * 10000000),
        (r'(\d+)\s*(?:lakh|lac|l)\s*(?:to|-)?\s*(\d+)\s*(?:lakh|lac|l)',
         lambda m: None),  # Range — handled separately
    ]
    for pattern, converter in price_patterns:
        match = re.search(pattern, msg_lower)
        if match and converter(match):
            max_price = converter(match)
            filters &= Q(price__lte=max_price)
            break

    # Bedroom detection
    bed_match = re.search(r'(\d+)\s*(?:bhk|bed|bedroom)', msg_lower)
    if bed_match:
        filters &= Q(bedrooms=int(bed_match.group(1)))

    # City detection — search in known cities from DB
    cities = Property.objects.values_list('city', flat=True).distinct()
    for city in cities:
        if city.lower() in msg_lower:
            filters &= Q(city__iexact=city)
            break

    return list(
        Property.objects.filter(filters)
        .select_related('agent', 'agent__user')
        .order_by('-is_featured', '-created_at')[:10]
    )


def _build_property_context(properties):
    """Format properties as text context for the AI."""
    if not properties:
        return ""

    lines = []
    for i, p in enumerate(properties[:5], 1):
        listing = "For Sale" if p.listing_type == 'sale' else "For Rent"
        lines.append(
            f"{i}. {p.title} | {p.get_property_type_display()} | {listing}\n"
            f"   Price: ₹{p.price:,.0f} | {p.bedrooms} BHK | {p.area_sqft} sq ft\n"
            f"   Location: {p.address}, {p.city}, {p.state}\n"
            f"   Agent: {p.agent.user.get_full_name()}"
        )
    return "\n\n".join(lines)


def _build_history(session):
    """Build conversation history for the Gemini chat API."""
    from ai_services.models import ChatMessage

    messages = ChatMessage.objects.filter(session=session).order_by('created_at')
    history = []
    for msg in messages:
        history.append({
            'role': msg.role,
            'parts': msg.content,
        })
    return history


def _serialize_properties(properties):
    """Serialize property objects for the API response."""
    return [
        {
            'id': p.id,
            'title': p.title,
            'property_type': p.property_type,
            'listing_type': p.listing_type,
            'price': float(p.price),
            'bedrooms': p.bedrooms,
            'bathrooms': p.bathrooms,
            'area_sqft': float(p.area_sqft),
            'city': p.city,
            'state': p.state,
        }
        for p in properties
    ]
