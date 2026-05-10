from sqlalchemy.ext.asyncio import AsyncSession
from .base import BaseRepository
from ..models.chat_turn import ChatTurn

class ChatTurnRepository(BaseRepository[ChatTurn]):
    def __init__(self, db: AsyncSession):
        super().__init__(ChatTurn, db)
