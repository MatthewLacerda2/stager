from sqlalchemy.ext.asyncio import AsyncSession
from .base import BaseRepository
from ..models.light import Light

class LightRepository(BaseRepository[Light]):
    def __init__(self, db: AsyncSession):
        super().__init__(Light, db)
