from pydantic import BaseModel, UUID4
from typing import Optional, List
from datetime import datetime

class SceneBase(BaseModel):
    name: Optional[str] = None
    brief_description: Optional[str] = None

class SceneCreate(SceneBase):
    pass

class SceneResponse(SceneBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# --- Viewport State Synchronization Schemas ---
class Vector3D(BaseModel):
    x: float
    y: float
    z: float

class Transform3D(BaseModel):
    pos: Vector3D
    rot: Vector3D
    scale: Vector3D

class SceneObjectState(BaseModel):
    id: UUID4
    name: str # The referenced BlenderObject name
    blender_object_id: UUID4
    group_object_id: Optional[UUID4] = None
    transform: Transform3D

class LightState(BaseModel):
    id: UUID4
    type: str # POINT, SUN, SPOT, AREA
    transform: Transform3D
    color: str
    intensity: float

class GroupObjectState(BaseModel):
    id: UUID4
    name: str
    transform: Transform3D

class SceneState(BaseModel):
    objects: List[SceneObjectState]
    lights: List[LightState]
    groups: List[GroupObjectState]

class SceneFullResponse(SceneResponse):
    """Returns the scene's metadata along with its complete 3D viewport state."""
    state: SceneState
