from pydantic import BaseModel, UUID4
from typing import Optional

class BlenderObjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class BlenderObjectResponse(BaseModel):
    id: UUID4
    name: str
    description: Optional[str] = None
    asset_path: Optional[str] = None
    
    class Config:
        from_attributes = True

class BlenderObjectListResponse(BlenderObjectResponse):
    is_used: bool

