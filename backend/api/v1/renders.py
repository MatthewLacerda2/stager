from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from ...core.database import get_db
from ...repositories.render_repository import RenderRepository
from ...repositories.scene_repository import SceneRepository
from ...repositories.camera_repository import CameraRepository
from ...schemas.render import RenderCreate, RenderResponse
from ...schemas.pagination import PaginatedResponse

router = APIRouter()

@router.post("/", response_model=RenderResponse)
async def create_render(request: RenderCreate, db: AsyncSession = Depends(get_db)):
    """Request a new render (sketch or high-fidelity) for a camera."""
    scene_repo = SceneRepository(db)
    scene = await scene_repo.get_by_id(request.scene_id)
    if not scene:
        raise HTTPException(status_code=404, detail="Scene not found")

    camera_repo = CameraRepository(db)
    camera = await camera_repo.get_by_id(request.camera_id)
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")

    # TODO: Trigger the actual Blender render pipeline here and populate image_url/description.

    repo = RenderRepository(db)
    render = await repo.create({
        "scene_id": request.scene_id,
        "camera_id": request.camera_id,
    })
    return render

@router.get("/", response_model=PaginatedResponse[RenderResponse])
async def list_renders(offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    """Get all renders sorted by most recent, paginated."""
    repo = RenderRepository(db)
    items, total = await repo.get_paginated(offset=offset, limit=limit)
    return PaginatedResponse(
        items=items,
        total=total,
        offset=offset,
        limit=limit,
    )

@router.get("/{render_id}", response_model=RenderResponse)
async def get_render(render_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get details of a specific render."""
    repo = RenderRepository(db)
    render = await repo.get_by_id(render_id)
    if not render:
        raise HTTPException(status_code=404, detail="Render not found")
    return render

@router.delete("/{render_id}", status_code=204)
async def delete_render(render_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete a specific render."""
    repo = RenderRepository(db)
    deleted = await repo.delete(render_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Render not found")
