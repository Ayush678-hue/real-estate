"""
Automated Valuation Model (AVM).

Estimates property market value by analyzing comparable properties in the
database and using Gemini for intelligent price analysis.
"""

import json
import logging
from decimal import Decimal
from django.db.models import Avg, Min, Max, Count, Q
from properties.models import Property
from ai_services.gemini_client import generate_text

logger = logging.getLogger(__name__)


def estimate_property_value(property_data):
    """
    Estimate the market value of a property based on comparable sales data.

    Args:
        property_data: dict with keys like property_type, bedrooms,
                       bathrooms, area_sqft, city, state.

    Returns:
        dict with estimated_price, price_range, confidence,
        comparable_count, and analysis.
    """
    comparables = _find_comparables(property_data)
    stats = _compute_stats(comparables, property_data)

    if stats['comparable_count'] == 0:
        return {
            'estimated_price': None,
            'price_range': {'low': None, 'high': None},
            'confidence': 'none',
            'comparable_count': 0,
            'comparable_properties': [],
            'analysis': (
                'No comparable properties found in the database. '
                'Try broadening your search criteria.'
            ),
        }

    # Build context for AI analysis
    comp_summaries = _summarize_comparables(comparables[:10])
    ai_analysis = _get_ai_analysis(property_data, stats, comp_summaries)

    return {
        'estimated_price': stats['estimated_price'],
        'price_range': stats['price_range'],
        'confidence': stats['confidence'],
        'comparable_count': stats['comparable_count'],
        'comparable_properties': comp_summaries,
        'analysis': ai_analysis,
    }


def _find_comparables(data):
    """Find comparable properties from the database."""
    qs = Property.objects.filter(is_published=True)

    # Match by property type (strict)
    if data.get('property_type'):
        qs = qs.filter(property_type=data['property_type'])

    # Match by city (strict)
    if data.get('city'):
        qs = qs.filter(city__iexact=data['city'])

    # Match by state (loose)
    if data.get('state'):
        qs = qs.filter(state__iexact=data['state'])

    # Bedroom range: ±1
    if data.get('bedrooms') is not None:
        beds = int(data['bedrooms'])
        qs = qs.filter(bedrooms__gte=max(0, beds - 1), bedrooms__lte=beds + 1)

    # Area range: ±30%
    if data.get('area_sqft') is not None:
        area = float(data['area_sqft'])
        qs = qs.filter(
            area_sqft__gte=area * 0.7,
            area_sqft__lte=area * 1.3,
        )

    return qs.order_by('-created_at')[:20]


def _compute_stats(comparables, data):
    """Compute pricing statistics from comparable properties."""
    count = comparables.count()
    if count == 0:
        return {
            'comparable_count': 0,
            'estimated_price': None,
            'price_range': {'low': None, 'high': None},
            'confidence': 'none',
        }

    agg = comparables.aggregate(
        avg_price=Avg('price'),
        min_price=Min('price'),
        max_price=Max('price'),
        avg_price_per_sqft=Avg('price') / Avg('area_sqft'),
    )

    avg_price = float(agg['avg_price'] or 0)

    # Compute price-per-sqft based estimate if area is provided
    if data.get('area_sqft') and agg.get('avg_price_per_sqft'):
        ppsf = float(agg['avg_price_per_sqft'])
        area = float(data['area_sqft'])
        sqft_estimate = ppsf * area
        # Blend average and sqft-based estimate
        estimated = (avg_price + sqft_estimate) / 2
    else:
        estimated = avg_price

    # Determine confidence
    if count >= 10:
        confidence = 'high'
    elif count >= 5:
        confidence = 'medium'
    else:
        confidence = 'low'

    # Price range: ±15% for high confidence, ±25% for low
    margin = 0.15 if confidence == 'high' else 0.20 if confidence == 'medium' else 0.25
    price_low = round(estimated * (1 - margin))
    price_high = round(estimated * (1 + margin))

    return {
        'comparable_count': count,
        'estimated_price': round(estimated),
        'price_range': {'low': price_low, 'high': price_high},
        'confidence': confidence,
    }


def _summarize_comparables(comparables):
    """Summarize comparable properties for the API response."""
    summaries = []
    for prop in comparables:
        summaries.append({
            'id': prop.id,
            'title': prop.title,
            'property_type': prop.property_type,
            'price': float(prop.price),
            'bedrooms': prop.bedrooms,
            'bathrooms': prop.bathrooms,
            'area_sqft': float(prop.area_sqft),
            'city': prop.city,
            'state': prop.state,
        })
    return summaries


def _get_ai_analysis(property_data, stats, comparables):
    """Use Gemini to provide intelligent analysis of the valuation."""
    prompt = f"""You are a real estate valuation expert. Analyze the following data and
provide a concise market analysis (100-150 words).

**Target Property:**
- Type: {property_data.get('property_type', 'N/A')}
- Bedrooms: {property_data.get('bedrooms', 'N/A')}
- Bathrooms: {property_data.get('bathrooms', 'N/A')}
- Area: {property_data.get('area_sqft', 'N/A')} sq ft
- City: {property_data.get('city', 'N/A')}, {property_data.get('state', 'N/A')}

**Market Data:**
- Comparable properties found: {stats['comparable_count']}
- Estimated value: ₹{stats['estimated_price']:,.0f}
- Price range: ₹{stats['price_range']['low']:,.0f} — ₹{stats['price_range']['high']:,.0f}
- Confidence: {stats['confidence']}

**Comparable Properties:**
{json.dumps(comparables[:5], indent=2)}

**Instructions:**
1. Explain why the estimated price is reasonable
2. Mention key factors affecting value (location, size, market trends)
3. Note any limitations of the estimate
4. Write in a professional, informative tone
5. Return ONLY the analysis text
"""

    try:
        return generate_text(prompt, temperature=0.5, max_tokens=512)
    except Exception as e:
        logger.error(f"AI analysis failed: {e}")
        return (
            f"Statistical estimate based on {stats['comparable_count']} "
            f"comparable properties. Confidence: {stats['confidence']}."
        )
