import os
import shutil
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from ...models.blender_object import BlenderObject

async def save_indexed_asset(
    db: AsyncSession,
    original_name: str,
    temp_obj_path: str,
    temp_image_paths: List[str],
    description: str,
    embedding: list[float]
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
                description_embedding=embedding,
                asset_path=final_obj_path
            )
            db.add(new_object)
            await db.flush()  # Generates the UUID instantly inside the transaction
            
            # 2. Move files only after DB flush succeeds
            shutil.move(temp_obj_path, final_obj_path)
            
        return new_object
    except Exception as e:
        # Transaction rolls back automatically.
        raise e
