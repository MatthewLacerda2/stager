from backend.core import config
import os
from typing import List, Any, Dict
from pydantic import BaseModel
from google import genai
from google.genai import types
from ...core.config import settings
from google.genai.types import GenerateContentConfig

class GeminiAssetDescriptionModel(BaseModel):
    description: str
    keywords: List[str]

def get_gemini_config(json_schema: dict[str, Any]) -> GenerateContentConfig:
    return GenerateContentConfig(
        response_mime_type='application/json',
        response_schema=json_schema,
    )

def describe_asset_with_gemini(image_paths: List[str]) -> Dict[str, Any]:
    """
    Passes screenshot paths to Gemini using the modern google-genai SDK
    to generate a structured description and keywords for a 3D asset.
    """
    # Initialize the client with our configured API key
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    config = get_gemini_config(GeminiAssetDescriptionModel.model_json_schema())
    
    prompt = (
        "You are a describing agent for a 3D models library.\n"
        "You are looking at 5 renders of a 3D model captured from different rotating angles.\n"
        "Provide a description of the model and a list of keywords.\n"
        "The description must specify what the object is and what is it's form, describing space and volume, without ambiguity or vagueness.\n"
        "Be as specific as you can be but do not say something that isn't sure.\n"
        "The important thing is the object itself, not the visual or ambience of the scene.\n"
        "The keywords will be used to search for objects based on keywords\n"
        "Your description must NOT start with 'This is a...'\n"
    )
    
    parts = []
    for path in image_paths:
        if not os.path.exists(path):
            continue
        with open(path, "rb") as f:
            img_bytes = f.read()
        parts.append(
            types.Part.from_bytes(
                data=img_bytes,
                mime_type="image/png"
            )
        )
        
    if not parts:
        raise ValueError("No valid screenshot images found for photoshoot description.")

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-preview",
        contents=[prompt, *parts],
        config=config
    )
    
    import json
    try:
        data = json.loads(response.text.strip())
        return {
            "description": data.get("description", "").strip(),
            "keywords": [k.lower().strip() for k in data.get("keywords", []) if k.strip()]
        }
    except Exception as e:
        print(f"Error parsing Gemini JSON: {e}. Raw response: {response.text}")
        return {
            "description": response.text.strip(),
            "keywords": []
        }
