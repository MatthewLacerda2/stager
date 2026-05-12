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

    async def semantic_search(self, scene_id: str, query_str: str, query_embedding: list[float], limit: int = 5) -> List[SceneObject]:
        from sqlalchemy import literal, case, any_

        words = [w.lower() for w in query_str.split() if w]
        if words:
            # Calculate match score: how many queried words exist in the keywords array
            keyword_score = sum(
                case((literal(w) == any_(BlenderObject.keywords), 1), else_=0)
                for w in words
            )
        else:
            keyword_score = literal(0)

        query = (
            select(self.model)
            .join(self.model.blender_object)
            .where(self.model.scene_id == scene_id)
            .order_by(
                keyword_score.desc(),
                BlenderObject.description_embedding.cosine_distance(query_embedding).asc()
            )
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
