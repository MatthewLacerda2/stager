from typing import List
from sqlalchemy import select
from .base import BaseRepository
from sqlalchemy.orm import joinedload
from ..models.scene_object import SceneObject
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.blender_object import BlenderObject

class SceneObjectRepository(BaseRepository[SceneObject]):
    def __init__(self, db: AsyncSession):
        super().__init__(SceneObject, db)

    async def semantic_search(self, scene_id: str, query_embedding: list[float], limit: int = 5) -> List[SceneObject]:
        query = (
            select(self.model)
            .join(self.model.blender_object)
            .where(self.model.scene_id == scene_id)
            .order_by(BlenderObject.description_embedding.cosine_distance(query_embedding))
            .options(joinedload(self.model.blender_object))
            .options(joinedload(self.model.group_object))
            .limit(limit)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_all_by_scene_id(self, scene_id: str) -> List[SceneObject]:
        query = (
            select(self.model)
            .where(self.model.scene_id == scene_id)
            .options(joinedload(self.model.blender_object))
            .options(joinedload(self.model.group_object))
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
