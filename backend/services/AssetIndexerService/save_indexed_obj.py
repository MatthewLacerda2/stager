import os
import shutil
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from ...models.blender_object import BlenderObject

async def save_indexed_asset(
    db: AsyncSession,
    original_name: str,
    temp_obj_path: str,
    description: str,
    keywords: List[str],
    embedding: list[float],
    bounds_data: dict
) -> BlenderObject:
    """
    Moves processed files to permanent storage and atomically saves the DB record.
    """
    storage_dir = os.path.join("storage", "assets")
    os.makedirs(storage_dir, exist_ok=True)
    
    final_obj_name = os.path.basename(temp_obj_path)
    final_obj_path = os.path.join(storage_dir, final_obj_name)
    
    try:
        async with db.begin():
            # 1. Create the database record
            new_object = BlenderObject(
                name=original_name,
                description=description,
                keywords=keywords,
                description_embedding=embedding,
                asset_path=final_obj_path,
                boundbox_x=bounds_data.get("boundbox_x"),
                boundbox_y=bounds_data.get("boundbox_y"),
                boundbox_z=bounds_data.get("boundbox_z"),
                boundbox_offset_x=bounds_data.get("boundbox_offset_x"),
                boundbox_offset_y=bounds_data.get("boundbox_offset_y"),
                boundbox_offset_z=bounds_data.get("boundbox_offset_z"),
                radius=bounds_data.get("radius"),
                radius_offset_x=bounds_data.get("radius_offset_x"),
                radius_offset_y=bounds_data.get("radius_offset_y"),
                radius_offset_z=bounds_data.get("radius_offset_z")
            )
            db.add(new_object)
            await db.flush()  # Generates the UUID instantly inside the transaction
            
            # 2. Move files only after DB flush succeeds
            shutil.move(temp_obj_path, final_obj_path)
            
        return new_object
    except Exception as e:
        # Transaction rolls back automatically.
        raise e
