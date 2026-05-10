from sqlalchemy.ext.asyncio import AsyncSession
from .base import BaseRepository
from ..models.chat import Chat

class ChatRepository(BaseRepository[Chat]):
    def __init__(self, db: AsyncSession):
        super().__init__(Chat, db)
