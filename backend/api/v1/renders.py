from fastapi import APIRouter
from uuid import UUID
from ...schemas.render import RenderCreate, RenderResponse
from ...schemas.pagination import PaginatedResponse

router = APIRouter()

@router.post("/", response_model=RenderResponse)
async def create_render(request: RenderCreate):
    """Request a new render (sketch or high-fidelity) for a camera."""
    pass

@router.get("/", response_model=PaginatedResponse[RenderResponse])
async def list_renders(offset: int = 0, limit: int = 10):
    """Get all renders sorted by most recent, paginated."""
    pass

@router.get("/{render_id}", response_model=RenderResponse)
async def get_render(render_id: UUID):
    """Get details of a specific render."""
    pass

@router.delete("/{render_id}", status_code=204)
async def delete_render(render_id: UUID):
    """Delete a specific render."""
    pass
