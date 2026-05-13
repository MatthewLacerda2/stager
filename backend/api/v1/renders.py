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

from ...services.blender.sketch_render import render_scene_blender

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

    # Trigger the actual Blender render pipeline here and populate image_url.
    try:
        image_url = await render_scene_blender(db, str(request.scene_id), str(request.camera_id), request.is_sketch)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Rendering failed: {str(e)}")

    repo = RenderRepository(db)
    render = await repo.create({
        "scene_id": request.scene_id,
        "camera_id": request.camera_id,
        "is_sketch": request.is_sketch,
        "image_url": image_url,
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
async def get_render_details(render_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get details of a specific render."""
    repo = RenderRepository(db)
    render = await repo.get_by_id(render_id)
    if not render:
        raise HTTPException(status_code=404, detail="Render not found")
    return render

@router.get("/{render_id}/file")
async def get_render_file(render_id: UUID, db: AsyncSession = Depends(get_db)):
    """Download the actual render PNG file."""
    import os
    from fastapi.responses import FileResponse
    repo = RenderRepository(db)
    render = await repo.get_by_id(render_id)
    if not render:
        raise HTTPException(status_code=404, detail="Render not found")
    
    if not render.image_url or not os.path.exists(render.image_url):
        raise HTTPException(status_code=404, detail="Render image file not found")
        
    filename = f"render_{render_id}.png"
    return FileResponse(
        path=render.image_url,
        media_type="image/png",
        filename=filename
    )

@router.delete("/{render_id}", status_code=204)
async def delete_render(render_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete a specific render."""
    repo = RenderRepository(db)
    deleted = await repo.delete(render_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Render not found")
