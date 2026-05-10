import ollama
from typing import List
from ollama import GenerateResponse

def describe_asset_with_ollama(image_paths: List[str]) -> str:
    """
    Passes screenshot paths to Ollama to generate a detailed 3D asset description.
    Ollama accepts the file paths directly in the images array!
    """
    prompt = (
        "You are looking at 5 different angles of a single 3D asset. "
        "Describe this asset in detail, including its category, shape, texture, material, "
        "and potential style/use-case. Return only the description."
    )
    
    response:GenerateResponse = ollama.generate(
        model='gemma4:e4b',
        prompt=prompt,
        images=image_paths
    )
    
    return response.get("response", "").strip()
