from sqlalchemy.ext.asyncio import AsyncSession
from .base import BaseRepository
from ..models.agent_log import AgentLog

class AgentLogRepository(BaseRepository[AgentLog]):
    def __init__(self, db: AsyncSession):
        super().__init__(AgentLog, db)
