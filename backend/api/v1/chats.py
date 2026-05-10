from fastapi import APIRouter
from uuid import UUID
from typing import List
from ...schemas.chat import ChatCreate, ChatResume, ChatResponse, ChatInteractionResponse

router = APIRouter()

@router.post("/", response_model=ChatInteractionResponse)
async def create_chat(request: ChatCreate):
    """Start a new chat for a scene and process the first prompt."""
    pass

@router.get("/scene/{scene_id}", response_model=List[ChatResponse])
async def list_chats(scene_id: UUID):
    """List all past chats belonging to a specific scene."""
    pass

@router.post("/{chat_id}/resume", response_model=ChatInteractionResponse)
async def resume_chat(chat_id: UUID, request: ChatResume):
    """Send a new prompt to an existing chat and process it."""
    pass

@router.delete("/{chat_id}", status_code=204)
async def delete_chat(chat_id: UUID):
    """Delete a chat and its history."""
    pass
