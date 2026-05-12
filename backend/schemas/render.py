from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime

class RenderCreate(BaseModel):
    scene_id: UUID4
    camera_id: UUID4
    is_sketch: bool = False
    
class RenderResponse(BaseModel):
    id: UUID4
    scene_id: UUID4
    camera_id: UUID4
    image_url: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
