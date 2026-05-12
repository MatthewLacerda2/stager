from typing import List, Optional
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from .base import BaseRepository
from ..models.camera import Camera

class CameraRepository(BaseRepository[Camera]):
    def __init__(self, db: AsyncSession):
        super().__init__(Camera, db)

    async def get_active_camera(self, scene_id) -> Optional[Camera]:
        query = (
            select(Camera)
            .where(Camera.scene_id == scene_id, Camera.is_active == True)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def deactivate_all(self, scene_id) -> None:
        """Set is_active=False on all cameras in a scene."""
        await self.db.execute(
            update(Camera)
            .where(Camera.scene_id == scene_id)
            .values(is_active=False)
        )

    async def get_by_scene_id(self, scene_id) -> List[Camera]:
        query = select(Camera).where(Camera.scene_id == scene_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())
