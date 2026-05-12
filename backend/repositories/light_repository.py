from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .base import BaseRepository
from ..models.light import Light

class LightRepository(BaseRepository[Light]):
    def __init__(self, db: AsyncSession):
        super().__init__(Light, db)

    async def get_by_scene_id(self, scene_id) -> List[Light]:
        query = select(Light).where(Light.scene_id == scene_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())
