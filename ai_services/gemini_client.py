"""
Centralized Google Gemini API client wrapper.
All AI services use this module to interact with the Gemini API.
"""

import logging
from django.conf import settings

logger = logging.getLogger(__name__)

_client = None


def get_client():
    """Return a configured Gemini GenerativeModel client (singleton)."""
    global _client
    if _client is not None:
        return _client

    try:
        from google import generativeai as genai
    except ImportError:
        raise ImportError(
            "google-generativeai is not installed. "
            "Run: pip install google-generativeai"
        )

    api_key = getattr(settings, 'GEMINI_API_KEY', None)
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is not configured. "
            "Set it in your .env file or Django settings."
        )

    genai.configure(api_key=api_key)
    _client = genai
    logger.info("Gemini API client initialized successfully.")
    return _client


def generate_text(prompt, model_name=None, temperature=0.7, max_tokens=2048):
    """
    Generate text using Gemini.

    Args:
        prompt: The text prompt to send.
        model_name: Override the default model name.
        temperature: Creativity (0.0 = deterministic, 1.0 = creative).
        max_tokens: Maximum tokens in the response.

    Returns:
        The generated text string.
    """
    client = get_client()
    model_name = model_name or getattr(
        settings, 'GEMINI_MODEL_NAME', 'gemini-2.0-flash'
    )
    model = client.GenerativeModel(model_name)

    generation_config = client.types.GenerationConfig(
        temperature=temperature,
        max_output_tokens=max_tokens,
    )

    try:
        response = model.generate_content(
            prompt,
            generation_config=generation_config,
        )
        return response.text
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        raise


def generate_with_image(prompt, image_data, mime_type="image/jpeg",
                        model_name=None, temperature=0.5, max_tokens=2048):
    """
    Generate text from a prompt + image (multimodal).

    Args:
        prompt: The text prompt.
        image_data: Raw image bytes.
        mime_type: MIME type of the image.
        model_name: Override the default model.
        temperature: Creativity level.
        max_tokens: Max response tokens.

    Returns:
        The generated text string.
    """
    client = get_client()
    model_name = model_name or getattr(
        settings, 'GEMINI_MODEL_NAME', 'gemini-2.0-flash'
    )
    model = client.GenerativeModel(model_name)

    generation_config = client.types.GenerationConfig(
        temperature=temperature,
        max_output_tokens=max_tokens,
    )

    image_part = {
        "mime_type": mime_type,
        "data": image_data,
    }

    try:
        response = model.generate_content(
            [prompt, image_part],
            generation_config=generation_config,
        )
        return response.text
    except Exception as e:
        logger.error(f"Gemini Vision API error: {e}")
        raise


def generate_chat(messages, system_instruction=None, model_name=None,
                   temperature=0.7, max_tokens=2048):
    """
    Multi-turn chat with Gemini.

    Args:
        messages: List of dicts with 'role' ('user'/'model') and 'parts' (text).
        system_instruction: Optional system prompt.
        model_name: Override the default model.
        temperature: Creativity level.
        max_tokens: Max response tokens.

    Returns:
        The model's reply text.
    """
    client = get_client()
    model_name = model_name or getattr(
        settings, 'GEMINI_MODEL_NAME', 'gemini-2.0-flash'
    )
    model = client.GenerativeModel(
        model_name,
        system_instruction=system_instruction,
    )

    generation_config = client.types.GenerationConfig(
        temperature=temperature,
        max_output_tokens=max_tokens,
    )

    chat = model.start_chat(history=messages[:-1])

    try:
        response = chat.send_message(
            messages[-1]['parts'],
            generation_config=generation_config,
        )
        return response.text
    except Exception as e:
        logger.error(f"Gemini Chat API error: {e}")
        raise
