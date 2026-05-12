from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete, select
from .base import BaseRepository
from ..models.group_object import GroupObject
from ..models.scene_object import SceneObject

class GroupObjectRepository(BaseRepository[GroupObject]):
    def __init__(self, db: AsyncSession):
        super().__init__(GroupObject, db)

    async def get_by_scene_id(self, scene_id) -> list[GroupObject]:
        query = select(self.model).where(self.model.scene_id == scene_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def delete_with_children(self, group_object_id: str, delete_children: bool = False) -> bool:
        """
        Deletes a group and handles children appropriately.
        If delete_children is True, child scene objects are deleted.
        If False, children are safely detached with their global transforms calculated and applied.
        """
        if delete_children:
            await self.db.execute(
                delete(SceneObject)
                .where(SceneObject.group_object_id == group_object_id)
            )
        else:
            # 1. Fetch the parent group to get its transform
            group_res = await self.db.execute(select(self.model).where(self.model.id == group_object_id))
            group = group_res.scalar_one_or_none()
            
            if group:
                # 2. Fetch all children
                children_res = await self.db.execute(select(SceneObject).where(SceneObject.group_object_id == group_object_id))
                children = children_res.scalars().all()
                
                # 3. Apply math and update each child
                import math
                rx = math.radians(group.rot_x)
                ry = math.radians(group.rot_y)
                rz = math.radians(group.rot_z)
                
                for child in children:
                    # Apply parent scale to child local position
                    px = child.pos_x * group.scale_x
                    py = child.pos_y * group.scale_y
                    pz = child.pos_z * group.scale_z

                    # Apply parent rotation (Assuming XYZ Euler order)
                    # Rotate X
                    py1 = py * math.cos(rx) - pz * math.sin(rx)
                    pz1 = py * math.sin(rx) + pz * math.cos(rx)
                    px1 = px
                    # Rotate Y
                    px2 = px1 * math.cos(ry) + pz1 * math.sin(ry)
                    pz2 = -px1 * math.sin(ry) + pz1 * math.cos(ry)
                    py2 = py1
                    # Rotate Z
                    px3 = px2 * math.cos(rz) - py2 * math.sin(rz)
                    py3 = px2 * math.sin(rz) + py2 * math.cos(rz)
                    pz3 = pz2
                    
                    # Final world position
                    new_pos_x = group.pos_x + px3
                    new_pos_y = group.pos_y + py3
                    new_pos_z = group.pos_z + pz3
                    
                    # Simple addition for rotation (Euler composition is complex, but this acts as an approximation)
                    new_rot_x = group.rot_x + child.rot_x
                    new_rot_y = group.rot_y + child.rot_y
                    new_rot_z = group.rot_z + child.rot_z
                    
                    # Multiply scales
                    new_scale_x = group.scale_x * child.scale_x
                    new_scale_y = group.scale_y * child.scale_y
                    new_scale_z = group.scale_z * child.scale_z

                    await self.db.execute(
                        update(SceneObject)
                        .where(SceneObject.id == child.id)
                        .values(
                            group_object_id=None,
                            pos_x=new_pos_x, pos_y=new_pos_y, pos_z=new_pos_z,
                            rot_x=new_rot_x, rot_y=new_rot_y, rot_z=new_rot_z,
                            scale_x=new_scale_x, scale_y=new_scale_y, scale_z=new_scale_z
                        )
                    )
        
        query = delete(self.model).where(self.model.id == group_object_id)
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount > 0
