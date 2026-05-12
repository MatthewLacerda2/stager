from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from .base import BaseRepository
from ..models.scene import Scene
from ..models.scene_object import SceneObject

class SceneRepository(BaseRepository[Scene]):
    def __init__(self, db: AsyncSession):
        super().__init__(Scene, db)

    async def get_full_scene(self, scene_id) -> Scene | None:
        """Eagerly load all scene children needed for SceneState."""
        query = (
            select(Scene)
            .where(Scene.id == scene_id)
            .options(
                selectinload(Scene.scene_objects).selectinload(SceneObject.blender_object),
                selectinload(Scene.group_objects),
                selectinload(Scene.lights),
                selectinload(Scene.cameras),
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
