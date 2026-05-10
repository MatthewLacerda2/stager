from uuid import UUID
from typing import List
from fastapi import APIRouter, UploadFile, File
from ...schemas.blender_object import BlenderObjectResponse, BlenderObjectListResponse

router = APIRouter()

@router.get("/", response_model=List[BlenderObjectListResponse])
async def list_objects():
    """List all available library assets, indicating if they are currently placed in any scene."""
    pass

@router.post("/upload", response_model=List[BlenderObjectResponse])
async def upload_objects(files: List[UploadFile] = File(...)):
    """Upload batches of 3D objects to be indexed in the database."""
    pass

@router.delete("/{object_id}", status_code=204)
async def delete_object(object_id: UUID):
    """Delete a specific library object."""
    pass
