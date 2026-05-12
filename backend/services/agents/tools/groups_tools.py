from typing import Optional, Dict, Any
from ..context import get_scene_id, get_db_session, run_async
from ....repositories.group_object_repository import GroupObjectRepository

def create_group(
    name: str,
    pos_x: float = 0.0, pos_y: float = 0.0, pos_z: float = 0.0,
    rot_x: float = 0.0, rot_y: float = 0.0, rot_z: float = 0.0,
    scale_x: float = 1.0, scale_y: float = 1.0, scale_z: float = 1.0
) -> Dict[str, Any]:
    """
    Creates a Blender Empty node to act as a shared transform parent for clusters of objects.
    
    Args:
        name: Name of the group, e.g., "dining-table-cluster".
        pos_x: X position coordinate.
        pos_y: Y position coordinate.
        pos_z: Z position coordinate.
        rot_x: X rotation coordinate in degrees.
        rot_y: Y rotation coordinate in degrees.
        rot_z: Z rotation coordinate in degrees.
        scale_x: X scale coordinate.
        scale_y: Y scale coordinate.
        scale_z: Z scale coordinate.
    """
    db = get_db_session()
    scene_id = get_scene_id()
    repo = GroupObjectRepository(db)

    group = run_async(repo.create({
        "scene_id": scene_id,
        "name": name,
        "pos_x": pos_x, "pos_y": pos_y, "pos_z": pos_z,
        "rot_x": rot_x, "rot_y": rot_y, "rot_z": rot_z,
        "scale_x": scale_x, "scale_y": scale_y, "scale_z": scale_z,
    }))
    return {"id": str(group.id), "status": "created"}

def update_group(
    group_object_id: str,
    pos_x: Optional[float] = None, pos_y: Optional[float] = None, pos_z: Optional[float] = None,
    rot_x: Optional[float] = None, rot_y: Optional[float] = None, rot_z: Optional[float] = None,
    scale_x: Optional[float] = None, scale_y: Optional[float] = None, scale_z: Optional[float] = None
) -> Dict[str, Any]:
    """
    Moves, rotates, or scales an entire group at once. Only provided fields will be updated.
    
    Args:
        group_object_id: Target group object ID.
        pos_x: X position coordinate.
        pos_y: Y position coordinate.
        pos_z: Z position coordinate.
        rot_x: X rotation coordinate in degrees.
        rot_y: Y rotation coordinate in degrees.
        rot_z: Z rotation coordinate in degrees.
        scale_x: X scale coordinate.
        scale_y: Y scale coordinate.
        scale_z: Z scale coordinate.
    """
    db = get_db_session()
    repo = GroupObjectRepository(db)

    updates = {}
    for field, value in [
        ("pos_x", pos_x), ("pos_y", pos_y), ("pos_z", pos_z),
        ("rot_x", rot_x), ("rot_y", rot_y), ("rot_z", rot_z),
        ("scale_x", scale_x), ("scale_y", scale_y), ("scale_z", scale_z),
    ]:
        if value is not None:
            updates[field] = value

    if not updates:
        return {"id": group_object_id, "status": "no changes"}

    result = run_async(repo.update(group_object_id, updates))
    if result is None:
        return {"error": f"Group {group_object_id} not found"}
    return {"id": group_object_id, "status": "updated"}

def delete_group(group_object_id: str, delete_children: bool = False) -> Dict[str, Any]:
    """
    Removes the group Empty node.
    
    Args:
        group_object_id: Target group object ID.
        delete_children: If true, all child objects are also deleted. If false, all children are safely detached with the transformations preserved.
    """
    db = get_db_session()
    repo = GroupObjectRepository(db)
    deleted = run_async(repo.delete_with_children(group_object_id, delete_children))
    if not deleted:
        return {"error": f"Group {group_object_id} not found"}
    return {"id": group_object_id, "status": "deleted"}
