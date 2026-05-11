import os
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

# Import our modular pipeline steps
from .ollama_description import describe_asset_with_ollama
from .save_indexed_obj import save_indexed_asset
from ..gemini_embedding import get_gemini_embedding
from ..blender.blender_processor import run_blender_extract_obj, run_blender_photoshoot

async def index_asset(db: AsyncSession, raw_file_path: str) -> Optional[str]:
    """
    The orchestrator for the asset indexing pipeline.
    
    1. Runs Blender processor to extract/clean the .obj
    2. Runs Blender photoshoot to take 5 screenshots.
    3. Calls Ollama for multimodal description.
    4. Calls Gemini for text embeddings.
    5. Saves atomatically to the database.
    """
    if not os.path.exists(raw_file_path):
        raise FileNotFoundError(f"Raw file not found: {raw_file_path}")
        
    temp_workspace = os.path.join("storage", "temp_processing")
    os.makedirs(temp_workspace, exist_ok=True)
    
    original_name = os.path.basename(raw_file_path)
    
    # Step 1: Extract Obj
    temp_obj_path = os.path.join(temp_workspace, f"cleaned_{original_name}.obj")
    temp_obj_path, bounds_data = run_blender_extract_obj(raw_file_path, temp_obj_path)
    
    # Step 2: Photoshoot
    screenshot_paths = run_blender_photoshoot(temp_obj_path, temp_workspace)
    
    # Step 3: AI Visual Description (Ollama)
    description = describe_asset_with_ollama(screenshot_paths)
    
    # Step 4: Text Embedding (Gemini)
    embedding = get_gemini_embedding(description)
    
    # Step 5: Atomic Database Save
    new_object = await save_indexed_asset(
        db=db,
        original_name=original_name,
        temp_obj_path=temp_obj_path,
        description=description,
        embedding=embedding,
        bounds_data=bounds_data
    )
    
    return str(new_object.id)
