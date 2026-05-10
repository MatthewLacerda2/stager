from sqlalchemy.ext.asyncio import AsyncSession
from .base import BaseRepository
from ..models.array_modifier import ArrayModifier

class ArrayModifierRepository(BaseRepository[ArrayModifier]):
    def __init__(self, db: AsyncSession):
        super().__init__(ArrayModifier, db)
