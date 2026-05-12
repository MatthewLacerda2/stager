import logging
from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from typing import List
from google.genai import Client
from sqlalchemy.ext.asyncio import AsyncSession
from ...core.database import get_db
from ...repositories.scene_repository import SceneRepository
from ...repositories.chat_repository import ChatRepository
from ...repositories.chat_turn_repository import ChatTurnRepository
from ...repositories.agent_log_repository import AgentLogRepository
from ...schemas.chat import ChatCreate, ChatResume, ChatResponse, ChatInteractionResponse
from ...services.agents.gemini_agent import gemini_agent
from ..helpers import build_scene_state

router = APIRouter()

# Shared Gemini client (reused across requests)
_client = Client()

logger = logging.getLogger(__name__)

async def _run_agent_turn(db, scene_id, chat_id, turn_id, prompt):
    """Run the Gemini agent loop for a single user prompt and persist results."""
    turn_repo = ChatTurnRepository(db)
    past_turns = await turn_repo.get_recent_history(chat_id, limit=32)

    messages = []
    for past in past_turns:
        messages.append({"role": "user", "parts": [{"text": past.user_prompt}]})
        messages.append({"role": "model", "parts": [{"text": past.agent_response}]})
        #TODO: mention toolcalls if any

    # Append current user prompt
    messages.append({"role": "user", "parts": [{"text": prompt}]})

    agent_result = await gemini_agent(
        messages=messages,
        client=_client,
        db=db,
        scene_id=str(scene_id),
    )

    # Persist the agent's text response back onto the turn
    if agent_result.text:
        await turn_repo.update(turn_id, {"agent_response": agent_result.text})
    else:
        logger.warning(f"Agent did not produce a text response for scene {scene_id} and chat {chat_id}")

    # Persist tool call logs
    if agent_result.tool_calls:
        log_repo = AgentLogRepository(db)
        for tc in agent_result.tool_calls:
            await log_repo.create({
                "chat_turn_id": turn_id,
                "tool_call_id": tc.id,
                "tool_name": tc.name,
                "tool_input": tc.args,
                "tool_output": tc.response,
            })

    return agent_result


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

    agent_result = await _run_agent_turn(db, request.scene_id, chat.id, turn.id, request.prompt)

    # Re-fetch scene with updated state after agent mutations
    scene = await scene_repo.get_full_scene(request.scene_id)
    state = build_scene_state(scene)

    return ChatInteractionResponse(
        chat_id=chat.id,
        turn_id=turn.id,
        agent_response=agent_result.text or None,
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

    agent_result = await _run_agent_turn(db, chat.scene_id, chat.id, turn.id, request.prompt)

    scene_repo = SceneRepository(db)
    scene = await scene_repo.get_full_scene(chat.scene_id)
    state = build_scene_state(scene)

    return ChatInteractionResponse(
        chat_id=chat.id,
        turn_id=turn.id,
        agent_response=agent_result.text or None,
        scene_state=state,
    )


@router.delete("/{chat_id}", status_code=204)
async def delete_chat(chat_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete a chat and its history."""
    chat_repo = ChatRepository(db)
    deleted = await chat_repo.delete(chat_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Chat not found")
