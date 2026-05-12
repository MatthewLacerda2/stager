from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from ...core.database import get_db
from ...repositories.scene_repository import SceneRepository
from ...repositories.chat_repository import ChatRepository
from ...repositories.chat_turn_repository import ChatTurnRepository
from ...schemas.chat import ChatCreate, ChatResume, ChatResponse, ChatInteractionResponse
from ..helpers import build_scene_state

router = APIRouter()

@router.post("/", response_model=ChatInteractionResponse)
async def create_chat(request: ChatCreate, db: AsyncSession = Depends(get_db)):
    """Start a new chat for a scene and process the first prompt."""
    scene_repo = SceneRepository(db)
    scene = await scene_repo.get_full_scene(request.scene_id)
    if not scene:
        raise HTTPException(status_code=404, detail="Scene not found")

    chat_repo = ChatRepository(db)
    chat = await chat_repo.create({"scene_id": request.scene_id})

    turn_repo = ChatTurnRepository(db)
    turn = await turn_repo.create({
        "chat_id": chat.id,
        "user_prompt": request.prompt,
    })

    # TODO: Run the Gemini agent loop here.
    # The agent would process the prompt, call tools that mutate the scene,
    # and return a text response. For now we just record the turn.

    # Re-fetch scene with updated state after agent mutations
    scene = await scene_repo.get_full_scene(request.scene_id)
    state = build_scene_state(scene)

    return ChatInteractionResponse(
        chat_id=chat.id,
        turn_id=turn.id,
        agent_response=turn.agent_response,
        scene_state=state,
    )

@router.get("/scene/{scene_id}", response_model=List[ChatResponse])
async def list_chats(scene_id: UUID, db: AsyncSession = Depends(get_db)):
    """List all past chats belonging to a specific scene."""
    scene_repo = SceneRepository(db)
    scene = await scene_repo.get_by_id(scene_id)
    if not scene:
        raise HTTPException(status_code=404, detail="Scene not found")

    chat_repo = ChatRepository(db)
    chats = await chat_repo.get_by_scene_id(scene_id)
    return chats

@router.post("/{chat_id}/resume", response_model=ChatInteractionResponse)
async def resume_chat(chat_id: UUID, request: ChatResume, db: AsyncSession = Depends(get_db)):
    """Send a new prompt to an existing chat and process it."""
    chat_repo = ChatRepository(db)
    chat = await chat_repo.get_by_id(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    turn_repo = ChatTurnRepository(db)
    turn = await turn_repo.create({
        "chat_id": chat.id,
        "user_prompt": request.prompt,
    })

    # TODO: Run the Gemini agent loop here.

    scene_repo = SceneRepository(db)
    scene = await scene_repo.get_full_scene(chat.scene_id)
    state = build_scene_state(scene)

    return ChatInteractionResponse(
        chat_id=chat.id,
        turn_id=turn.id,
        agent_response=turn.agent_response,
        scene_state=state,
    )

@router.delete("/{chat_id}", status_code=204)
async def delete_chat(chat_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete a chat and its history."""
    chat_repo = ChatRepository(db)
    deleted = await chat_repo.delete(chat_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Chat not found")
