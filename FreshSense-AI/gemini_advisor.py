"""
FreshSense AI - Gemini Multimodal Vision & Zero-Waste Culinary Copilot
======================================================================
Integrates Google GenAI SDK with IoT environmental telemetry
to perform multimodal food safety diagnostics and dynamic zero-waste recipe recommendations.
"""

import json
import os
import pathlib
from io import BytesIO
from dotenv import load_dotenv, find_dotenv
from google import genai
from google.genai import types
from PIL import Image

def _load_api_key() -> str:
    """Bulletproof loader for Gemini API Key from .env or system environment."""
    this_dir = pathlib.Path(__file__).parent.resolve()
    env_paths = [
        this_dir / ".env",
        this_dir.parent / ".env",
        pathlib.Path.cwd() / ".env",
    ]
    for ep in env_paths:
        if ep.exists():
            load_dotenv(dotenv_path=ep, override=True)
            break
    
    load_dotenv(find_dotenv(), override=True)

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if api_key:
        api_key = api_key.strip().strip('"').strip("'")
    
    if not api_key or api_key == "your_actual_gemini_api_key_here":
        raise ValueError("GEMINI_API_KEY is not set or contains the default placeholder. Please add your real Gemini API key to the .env file.")
    
    return api_key


def get_client():
    api_key = _load_api_key()
    return genai.Client(api_key=api_key)


def analyze_food(image_bytes: bytes, temp: float, humidity: float, gas_ppm: float, freshness_score: float) -> dict:
    """
    Sends the food snapshot and real-time telemetry to Gemini
    and returns a structured nutritional/safety recommendation.
    Includes automatic multi-model fallback (gemini-3.6-flash -> gemini-2.5-flash -> gemini-2.0-flash -> gemini-1.5-flash).
    """
    try:
        client = get_client()
        # Load image via Pillow
        pil_image = Image.open(BytesIO(image_bytes))

        # Structured prompt guiding the multimodal reasoning
        prompt = f"""
You are FreshSense AI, an expert food scientist and zero-waste culinary copilot.
You are given an image of a food item alongside real-time IoT and ML telemetry:
- Ambient Temperature: {temp}°C
- Relative Humidity: {humidity}%
- MQ-135 Gas Telemetry (VOC/Ammonia): {gas_ppm} PPM
- Predicted ML Freshness Index: {freshness_score:.1f}/100

TASK:
1. Examine the visual features (discoloration, softening, bruising, mold).
2. Correlate visual cues with the sensor metrics.
3. Respond ONLY in valid JSON matching this exact structure:
{{
  "detected_item": "Name of the food/fruit",
  "visual_condition": "Brief 1-sentence observation of surface state",
  "safety_verdict": "Fresh" or "Cook Immediately" or "Discard",
  "estimated_safe_hours": <number representing remaining consumable hours>,
  "risk_reasoning": "1-2 sentences explaining why based on gas PPM and visual cues",
  "zero_waste_recipes": [
    {{
      "recipe_name": "Title of dish",
      "prep_time_minutes": <number>,
      "instructions": "Step-by-step summary to cook or preserve it quickly"
    }},
    {{
      "recipe_name": "Title of second quick dish",
      "prep_time_minutes": <number>,
      "instructions": "Step-by-step summary"
    }}
  ]
}}
"""

        candidate_models = [
            "gemini-3.6-flash",
            "gemini-2.5-flash",
            "gemini-2.0-flash",
            "gemini-1.5-flash",
            "gemini-1.5-pro",
        ]

        last_error = None
        for model_name in candidate_models:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=[pil_image, prompt],
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.2
                    )
                )
                if response and response.text:
                    return json.loads(response.text)
            except Exception as model_err:
                last_error = model_err
                continue

        if last_error:
            raise last_error

        return {
            "error": True,
            "message": "No response returned from Gemini models."
        }

    except Exception as e:
        return {
            "error": True,
            "message": f"Gemini API request failed: {str(e)}"
        }
