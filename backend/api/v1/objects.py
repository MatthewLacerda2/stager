import os
import shutil
from uuid import UUID
from typing import List
from ...core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from ...repositories.blender_object_repository import BlenderObjectRepository
from ...schemas.blender_object import BlenderObjectResponse, BlenderObjectListResponse
from ...services.AssetIndexerService.indexer_job import index_asset

router = APIRouter()

UPLOAD_DIR = os.path.join("storage", "uploads")

@router.get("/", response_model=List[BlenderObjectListResponse])
async def list_objects(db: AsyncSession = Depends(get_db)):
    """List all available library assets, indicating if they are currently placed in any scene."""
    repo = BlenderObjectRepository(db)

    rows = await repo.get_all_with_usage()
    return [
        BlenderObjectListResponse(
            id=obj.id,
            name=obj.name,
            description=obj.description,
            asset_path=obj.asset_path,
            is_used=is_used,
        )
        for obj, is_used in rows
    ]

@router.post("/upload", response_model=BlenderObjectResponse)
async def upload_object(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    """Upload a 3D object to be indexed in the database."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    raw_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(raw_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        new_id = await index_asset(db, raw_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Indexing failed: {e}")
    finally:
        # Clean up the raw upload
        if os.path.exists(raw_path):
            os.remove(raw_path)

    repo = BlenderObjectRepository(db)
    obj = await repo.get_by_id(new_id)
    return obj

@router.delete("/{object_id}", status_code=204)
async def delete_object(object_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete a specific library object."""
    repo = BlenderObjectRepository(db)
    deleted = await repo.delete(object_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Object not found")
