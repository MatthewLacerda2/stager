import os
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

# Import our modular pipeline steps
from .gemini_description import describe_asset_with_gemini
from .save_indexed_obj import save_indexed_asset
from ..gemini_embedding import get_gemini_embedding
from ..blender.blender_processor import run_blender_extract_obj, run_blender_photoshoot

async def index_asset(db: AsyncSession, raw_file_path: str) -> List[str]:
    """
    The orchestrator for the asset indexing pipeline.
    
    1. Runs Blender processor to extract/clean the .obj (potentially split into multiple sub-meshes)
    2. For each extracted mesh, runs photoshoot, gemini description, embedding, and saves to database.
    """
    if not os.path.exists(raw_file_path):
        raise FileNotFoundError(f"Raw file not found: {raw_file_path}")
        
    temp_workspace = os.path.join("storage", "temp_processing")
    os.makedirs(temp_workspace, exist_ok=True)
    
    original_name = os.path.basename(raw_file_path)
    base_name, _ = os.path.splitext(original_name)
    
    # Step 1: Extract Obj
    temp_obj_path = os.path.join(temp_workspace, f"cleaned_{original_name}.obj")
    extracted_items = run_blender_extract_obj(raw_file_path, temp_obj_path)
    
    indexed_ids = []
    
    for idx, (part_obj_path, bounds_data) in enumerate(extracted_items):
        part_name = f"{base_name}_part_{idx}"
        
        # Step 2: Photoshoot for this specific part
        screenshot_paths = run_blender_photoshoot(part_obj_path, temp_workspace)
        
        # Step 3: AI Visual Description (Gemini)
        description = describe_asset_with_gemini(screenshot_paths)
        
        # Step 4: Text Embedding (Gemini)
        embedding = get_gemini_embedding(description)
        
        # Step 5: Atomic Database Save
        new_object = await save_indexed_asset(
            db=db,
            original_name=part_name,
            temp_obj_path=part_obj_path,
            description=description,
            embedding=embedding,
            bounds_data=bounds_data
        )
        indexed_ids.append(str(new_object.id))
        
    return indexed_ids
