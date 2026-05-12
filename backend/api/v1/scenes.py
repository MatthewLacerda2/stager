from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from ...core.database import get_db
from ...repositories.scene_repository import SceneRepository
from ...schemas.scene import SceneCreate, SceneResponse, SceneFullResponse
from ..helpers import build_scene_state

router = APIRouter()

@router.post("/", response_model=SceneResponse)
async def create_scene(request: SceneCreate, db: AsyncSession = Depends(get_db)):
    """Create a new 3D scene."""
    repo = SceneRepository(db)
    scene = await repo.create(request.model_dump(exclude_unset=True))
    return scene

@router.get("/{scene_id}", response_model=SceneFullResponse)
async def get_scene(scene_id: UUID, db: AsyncSession = Depends(get_db)):
    """Fetch a scene's metadata along with its complete 3D viewport state (objects, lights, groups)."""
    repo = SceneRepository(db)
    scene = await repo.get_full_scene(scene_id)
    if not scene:
        raise HTTPException(status_code=404, detail="Scene not found")

    state = build_scene_state(scene)
    return SceneFullResponse(
        id=scene.id,
        name=scene.name,
        brief_description=scene.brief_description,
        created_at=scene.created_at,
        updated_at=scene.updated_at,
        state=state,
    )

@router.delete("/{scene_id}", status_code=204)
async def delete_scene(scene_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete a scene and all its contents."""
    repo = SceneRepository(db)
    deleted = await repo.delete(scene_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Scene not found")
