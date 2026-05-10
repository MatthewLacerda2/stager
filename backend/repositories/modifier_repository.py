from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from .base import BaseRepository
from ..models.modifier import Modifier

class ModifierRepository(BaseRepository[Modifier]):
    def __init__(self, db: AsyncSession):
        super().__init__(Modifier, db)

    async def _shift_orders(self, scene_object_id: str, from_order: int, shift: int):
        """Internal helper to shift modifier execution orders up or down."""
        await self.db.execute(
            update(self.model)
            .where(self.model.scene_object_id == scene_object_id)
            .where(self.model.execution_order >= from_order)
            .values(execution_order=self.model.execution_order + shift)
        )

    async def create_at_order(self, obj_in: dict) -> Modifier:
        """Creates a new modifier and shifts subsequent modifiers down."""
        scene_object_id = obj_in['scene_object_id']
        order_index = obj_in['execution_order']
        
        await self._shift_orders(scene_object_id, order_index, 1)
        
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete_at_order(self, modifier_id: str) -> bool:
        """Deletes a modifier and shifts subsequent modifiers up to fill the gap."""
        result = await self.db.execute(select(self.model).where(self.model.id == modifier_id))
        mod = result.scalar_one_or_none()
        if not mod:
            return False
            
        scene_object_id = mod.scene_object_id
        order_index = mod.execution_order
        
        await self.db.execute(delete(self.model).where(self.model.id == modifier_id))
        await self._shift_orders(scene_object_id, order_index + 1, -1)
        
        await self.db.commit()
        return True
        
    async def update_order(self, modifier_id: str, new_order: int, obj_in: dict) -> Modifier:
        """Updates a modifier, recalculating stack order if its index changed."""
        result = await self.db.execute(select(self.model).where(self.model.id == modifier_id))
        mod = result.scalar_one_or_none()
        if not mod:
            return None
            
        scene_object_id = mod.scene_object_id
        old_order = mod.execution_order
        
        if new_order != old_order:
            # Shift down everything above old_order (remove the gap)
            await self._shift_orders(scene_object_id, old_order + 1, -1)
            # Shift up everything at or above new_order (create a gap)
            await self._shift_orders(scene_object_id, new_order, 1)
            
        obj_in['execution_order'] = new_order
        
        update_stmt = (
            update(self.model)
            .where(self.model.id == modifier_id)
            .values(**obj_in)
            .returning(self.model)
        )
        res = await self.db.execute(update_stmt)
        await self.db.commit()
        return res.scalar_one_or_none()
