from typing import List, Tuple
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from .base import BaseRepository
from ..models.render import Render

class RenderRepository(BaseRepository[Render]):
    def __init__(self, db: AsyncSession):
        super().__init__(Render, db)

    async def get_paginated(self, offset: int = 0, limit: int = 10) -> Tuple[List[Render], int]:
        """Returns (items, total_count) for paginated listing."""
        count_query = select(func.count()).select_from(Render)
        count_result = await self.db.execute(count_query)
        total = count_result.scalar()

        query = (
            select(Render)
            .order_by(Render.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.db.execute(query)
        items = list(result.scalars().all())
        return items, total
