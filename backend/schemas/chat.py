from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime
from .scene import SceneState

class ChatCreate(BaseModel):
    scene_id: UUID4
    prompt: str

class ChatResume(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    id: UUID4
    scene_id: UUID4
    created_at: datetime
    
    class Config:
        from_attributes = True

class ChatTurnResponse(BaseModel):
    id: UUID4
    chat_id: UUID4
    user_prompt: str
    agent_response: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class ChatInteractionResponse(BaseModel):
    chat_id: UUID4
    turn_id: UUID4
    agent_response: Optional[str] = None
    scene_state: SceneState
