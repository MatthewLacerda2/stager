from sqlalchemy.ext.asyncio import AsyncSession
from .base import BaseRepository
from ..models.render import Render

class RenderRepository(BaseRepository[Render]):
    def __init__(self, db: AsyncSession):
        super().__init__(Render, db)
