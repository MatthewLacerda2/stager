from typing import Optional, Dict, Any
from ..context import get_scene_id, get_db_session
from ....repositories.light_repository import LightRepository

async def create_light(
    type: str,
    pos_x: float = 0.0, pos_y: float = 0.0, pos_z: float = 0.0,
    rot_x: float = 0.0, rot_y: float = 0.0, rot_z: float = 0.0,
    scale_x: float = 1.0, scale_y: float = 1.0, scale_z: float = 1.0,
    color: str = "#FFFFFF",
    intensity: float = 100.0
) -> Dict[str, Any]:
    """
    Instantiates a new light source in the scene.
    
    Args:
        type: Options -> POINT, SUN, SPOT, AREA.
        pos_x: X position coordinate.
        pos_y: Y position coordinate.
        pos_z: Z position coordinate.
        rot_x: X rotation coordinate in degrees.
        rot_y: Y rotation coordinate in degrees.
        rot_z: Z rotation coordinate in degrees.
        scale_x: X scale coordinate.
        scale_y: Y scale coordinate.
        scale_z: Z scale coordinate.
        color: Hex color string.
        intensity: Energy/power value.
    """
    db = get_db_session()
    scene_id = get_scene_id()
    repo = LightRepository(db)
    light = await repo.create({
        "scene_id": scene_id, "type": type,
        "pos_x": pos_x, "pos_y": pos_y, "pos_z": pos_z,
        "rot_x": rot_x, "rot_y": rot_y, "rot_z": rot_z,
        "scale_x": scale_x, "scale_y": scale_y, "scale_z": scale_z,
        "color": color, "intensity": intensity,
    })
    return {"id": str(light.id), "status": "created"}

async def update_light(
    light_id: str,
    pos_x: float = None, pos_y: float = None, pos_z: float = None,
    rot_x: float = None, rot_y: float = None, rot_z: float = None,
    scale_x: float = None, scale_y: float = None, scale_z: float = None,
    color: str = None,
    intensity: float = None
) -> Dict[str, Any]:
    """
    Modifies existing light properties. Only provided fields will be updated.
    
    Args:
        light_id: Target light ID.
        pos_x: X position coordinate.
        pos_y: Y position coordinate.
        pos_z: Z position coordinate.
        rot_x: X rotation coordinate in degrees.
        rot_y: Y rotation coordinate in degrees.
        rot_z: Z rotation coordinate in degrees.
        scale_x: X scale coordinate.
        scale_y: Y scale coordinate.
        scale_z: Z scale coordinate.
        color: Hex color string.
        intensity: Energy/power value.
    """
    db = get_db_session()
    repo = LightRepository(db)
    updates = {}
    for field, value in [
        ("pos_x", pos_x), ("pos_y", pos_y), ("pos_z", pos_z),
        ("rot_x", rot_x), ("rot_y", rot_y), ("rot_z", rot_z),
        ("scale_x", scale_x), ("scale_y", scale_y), ("scale_z", scale_z),
        ("color", color), ("intensity", intensity),
    ]:
        if value is not None:
            updates[field] = value
    if not updates:
        return {"id": light_id, "status": "no changes"}
    result = await repo.update(light_id, updates)
    if result is None:
        return {"error": f"Light {light_id} not found"}
    return {"id": light_id, "status": "updated"}

async def delete_light(light_id: str) -> Dict[str, Any]:
    """
    Removes a light source from the scene.
    
    Args:
        light_id: Target light ID.
    """
    db = get_db_session()
    repo = LightRepository(db)
    deleted = await repo.delete(light_id)
    if not deleted:
        return {"error": f"Light {light_id} not found"}
    return {"id": light_id, "status": "deleted"}
