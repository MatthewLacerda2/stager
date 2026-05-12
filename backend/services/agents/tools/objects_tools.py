from typing import Optional, Dict, Any
from ..context import get_scene_id, get_db_session
from ....repositories.scene_object_repository import SceneObjectRepository

async def create_object(
    blender_object_id: str,
    pos_x: float = 0.0, pos_y: float = 0.0, pos_z: float = 0.0,
    rot_x: float = 0.0, rot_y: float = 0.0, rot_z: float = 0.0,
    scale_x: float = 1.0, scale_y: float = 1.0, scale_z: float = 1.0,
    group_object_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Instantiates a 3D asset from the library into the active scene.
    
    Args:
        blender_object_id: The ID from the asset library.
        pos_x: X position coordinate.
        pos_y: Y position coordinate.
        pos_z: Z position coordinate.
        rot_x: X rotation coordinate in degrees.
        rot_y: Y rotation coordinate in degrees.
        rot_z: Z rotation coordinate in degrees.
        scale_x: X scale coordinate.
        scale_y: Y scale coordinate.
        scale_z: Z scale coordinate.
        group_object_id: ID of the parent Empty group.
    """
    db = get_db_session()
    scene_id = get_scene_id()
    repo = SceneObjectRepository(db)

    data = {
        "scene_id": scene_id,
        "blender_object_id": blender_object_id,
        "pos_x": pos_x, "pos_y": pos_y, "pos_z": pos_z,
        "rot_x": rot_x, "rot_y": rot_y, "rot_z": rot_z,
        "scale_x": scale_x, "scale_y": scale_y, "scale_z": scale_z,
    }
    if group_object_id is not None:
        data["group_object_id"] = group_object_id

    obj = await repo.create(data)
    return {"id": str(obj.id), "status": "created"}

async def update_object(
    scene_object_id: str,
    pos_x: Optional[float] = None, pos_y: Optional[float] = None, pos_z: Optional[float] = None,
    rot_x: Optional[float] = None, rot_y: Optional[float] = None, rot_z: Optional[float] = None,
    scale_x: Optional[float] = None, scale_y: Optional[float] = None, scale_z: Optional[float] = None,
    group_object_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Modifies transforms or parent associations of an existing scene instance. Only provided fields will be updated.
    
    Args:
        scene_object_id: Target scene object ID.
        pos_x: X position coordinate.
        pos_y: Y position coordinate.
        pos_z: Z position coordinate.
        rot_x: X rotation coordinate in degrees.
        rot_y: Y rotation coordinate in degrees.
        rot_z: Z rotation coordinate in degrees.
        scale_x: X scale coordinate.
        scale_y: Y scale coordinate.
        scale_z: Z scale coordinate.
        group_object_id: Passing a valid UUID sets the parent; passing explicitly null/None unparents the object.
    """
    db = get_db_session()
    repo = SceneObjectRepository(db)

    updates = {}
    for field, value in [
        ("pos_x", pos_x), ("pos_y", pos_y), ("pos_z", pos_z),
        ("rot_x", rot_x), ("rot_y", rot_y), ("rot_z", rot_z),
        ("scale_x", scale_x), ("scale_y", scale_y), ("scale_z", scale_z),
    ]:
        if value is not None:
            updates[field] = value

    # group_object_id can explicitly be set to None to unparent
    if group_object_id is not None:
        updates["group_object_id"] = group_object_id

    if not updates:
        return {"id": scene_object_id, "status": "no changes"}

    result = await repo.update(scene_object_id, updates)
    if result is None:
        return {"error": f"Scene object {scene_object_id} not found"}
    return {"id": scene_object_id, "status": "updated"}

async def delete_object(scene_object_id: str) -> Dict[str, Any]:
    """
    Deletes an instance entirely from the scene.
    
    Args:
        scene_object_id: Target scene object ID.
    """
    db = get_db_session()
    repo = SceneObjectRepository(db)
    deleted = await repo.delete(scene_object_id)
    if not deleted:
        return {"error": f"Scene object {scene_object_id} not found"}
    return {"id": scene_object_id, "status": "deleted"}

