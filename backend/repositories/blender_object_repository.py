from typing import List, Tuple
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from .base import BaseRepository
from ..models.blender_object import BlenderObject
from ..models.scene_object import SceneObject

class BlenderObjectRepository(BaseRepository[BlenderObject]):
    def __init__(self, db: AsyncSession):
        super().__init__(BlenderObject, db)

    async def semantic_search(self, query_str: str, query_embedding: list[float], limit: int = 16) -> List[BlenderObject]:
        from sqlalchemy import literal, case, any_

        words = [w.lower() for w in query_str.split() if w]
        if words:
            # Calculate match score: how many queried words exist in the keywords array
            keyword_score = sum(
                case((literal(w) == any_(self.model.keywords), 1), else_=0)
                for w in words
            )
        else:
            keyword_score = literal(0)

        query = (
            select(self.model)
            .order_by(
                keyword_score.desc(),
                self.model.description_embedding.cosine_distance(query_embedding).asc()
            )
            .limit(limit)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_all_with_usage(self) -> List[Tuple[BlenderObject, bool]]:
        """Returns all blender objects along with whether they are placed in any scene."""
        is_used_subq = (
            exists()
            .where(SceneObject.blender_object_id == BlenderObject.id)
            .correlate(BlenderObject)
        )
        query = select(BlenderObject, is_used_subq.label("is_used"))
        result = await self.db.execute(query)
        return list(result.all())
