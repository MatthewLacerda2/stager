from sqlalchemy.ext.asyncio import AsyncSession
from .base import BaseRepository
from ..models.camera import Camera

class CameraRepository(BaseRepository[Camera]):
    def __init__(self, db: AsyncSession):
        super().__init__(Camera, db)
