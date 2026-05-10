from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .base import BaseRepository
from ..models.blender_object import BlenderObject

class BlenderObjectRepository(BaseRepository[BlenderObject]):
    def __init__(self, db: AsyncSession):
        super().__init__(BlenderObject, db)

    async def semantic_search(self, query_embedding: list[float], limit: int = 5) -> List[BlenderObject]:
        query = (
            select(self.model)
            .order_by(self.model.description_embedding.cosine_distance(query_embedding))
            .limit(limit)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
