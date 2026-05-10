from sqlalchemy.ext.asyncio import AsyncSession
from .base import BaseRepository
from ..models.scene import Scene

class SceneRepository(BaseRepository[Scene]):
    def __init__(self, db: AsyncSession):
        super().__init__(Scene, db)
