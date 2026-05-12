from typing import List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from .base import BaseRepository
from ..models.chat import Chat

class ChatRepository(BaseRepository[Chat]):
    def __init__(self, db: AsyncSession):
        super().__init__(Chat, db)

    async def get_by_scene_id(self, scene_id) -> List[Chat]:
        query = (
            select(Chat)
            .where(Chat.scene_id == scene_id)
            .order_by(Chat.created_at.desc())
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
