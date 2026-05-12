from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .base import BaseRepository
from ..models.chat_turn import ChatTurn

class ChatTurnRepository(BaseRepository[ChatTurn]):
    def __init__(self, db: AsyncSession):
        super().__init__(ChatTurn, db)

    async def get_recent_history(
        self,
        chat_id,
        limit: Optional[int] = 32,
        offset: Optional[int] = 0
    ) -> List[ChatTurn]:
        """
        Retrieves past turns for a chat, sorted chronologically (oldest first).
        Supports optional limit and offset for pagination.
        """
        query = (
            select(ChatTurn)
            .where(
                ChatTurn.chat_id == chat_id,
                ChatTurn.agent_response.is_not(None)
            )
            .order_by(ChatTurn.created_at.desc())
        )
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)

        result = await self.db.execute(query)
        turns = list(result.scalars().all())
        # Reverse to return in chronological order (oldest first)
        turns.reverse()
        return turns
