import ollama
from typing import List
from ollama import GenerateResponse

def describe_asset_with_ollama(image_paths: List[str]) -> str:
    """
    Passes screenshot paths to Ollama to generate a detailed 3D asset description.
    Ollama accepts the file paths directly in the images array!
    """
    prompt = (
        "You are looking at 5 renders of from around a .obj file."
        "Describe the asset in detail. You must say what the object is, describe the primary shape and relevant details."
        "Your description be useful for a semantic search, similar to how Google's AI generated answers are."
        "Return only the description. Do NOT start with things like 'Here is a detailed description'."
    )
    
    response:GenerateResponse = ollama.generate(
        model='gemma4:e4b',
        prompt=prompt,
        images=image_paths
    )
    
    return response.get("response", "").strip()
