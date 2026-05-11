import os
from typing import List
from google import genai
from google.genai import types
from ...core.config import settings

def describe_asset_with_gemini(image_paths: List[str]) -> str:
    """
    Passes screenshot paths to Gemini using the modern google-genai SDK
    to generate a detailed 3D asset description.
    """
    # Initialize the client with our configured API key
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    prompt = (
        "You are looking at 5 renders of a 3D model (.obj) captured from different rotating angles.\n"
        "Describe the asset in detail. You must say what the object is, describe the primary shape, and note relevant design details.\n"
        "The important thing is the object itself, not the visual or ambience of the scene\n"
        "Your description should be extremely useful for a semantic vector search, similar to how Google's AI generated answers are.\n"
        "Return ONLY the description. Do NOT start with intro text like 'Here is a detailed description' or markdown code blocks."
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
        contents=[prompt, *parts]
    )
    
    return response.text.strip()
