from fastapi import APIRouter
from uuid import UUID
from ...schemas.scene import SceneCreate, SceneResponse, SceneFullResponse

router = APIRouter()

@router.post("/", response_model=SceneResponse)
async def create_scene(request: SceneCreate):
    """Create a new 3D scene."""
    pass

@router.get("/{scene_id}", response_model=SceneFullResponse)
async def get_scene(scene_id: UUID):
    """Fetch a scene's metadata along with its complete 3D viewport state (objects, lights, groups)."""
    pass

@router.delete("/{scene_id}", status_code=204)
async def delete_scene(scene_id: UUID):
    """Delete a scene and all its contents."""
    pass
