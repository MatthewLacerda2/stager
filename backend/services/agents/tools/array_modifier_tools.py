import logging
from typing import Optional, Dict, Any
from ..context import get_db_session, run_async
from ....repositories.array_modifier_repository import ArrayModifierRepository

logger = logging.getLogger(__name__)

def create_array_modifier(
    scene_object_id: str,
    count: int = 2,
    offset_type: str = "relative",
    factor_x: float = 1.0,
    factor_y: float = 0.0,
    factor_z: float = 0.0
) -> Dict[str, Any]:
    """
    Applies an Array modifier to a scene object to instantiate it multiple times.
    Note: An object can only have one Array modifier.
    
    Args:
        scene_object_id: Target scene object ID.
        count: Number of instances to create (default 2).
        offset_type: Either 'relative' (based on object bounding box) or 'constant' (absolute units).
        factor_x: Offset factor along the X axis.
        factor_y: Offset factor along the Y axis.
        factor_z: Offset factor along the Z axis.
    """
    db = get_db_session()
    repo = ArrayModifierRepository(db)

    #if offset type is not relative nor constant, log an error, set to relative, and continue
    if offset_type not in ["relative", "constant"]:
        logger.warning(f"Offset type {offset_type} is not relative nor constant, setting to relative")
        offset_type = "relative"

    modifier = run_async(repo.create({
        "scene_object_id": scene_object_id,
        "count": count,
        "offset_type": offset_type,
        "factor_x": factor_x,
        "factor_y": factor_y,
        "factor_z": factor_z,
    }))
    return {"id": str(modifier.id), "status": "created"}

def update_array_modifier(
    array_modifier_id: str,
    count: Optional[int] = None,
    offset_type: Optional[str] = None,
    factor_x: Optional[float] = None,
    factor_y: Optional[float] = None,
    factor_z: Optional[float] = None
) -> Dict[str, Any]:
    """
    Updates the parameters of an existing Array modifier. Only provided fields will be updated.
    
    Args:
        array_modifier_id: Target array modifier ID.
        count: Number of instances to create.
        offset_type: Either 'relative' or 'constant'.
        factor_x: Offset factor along the X axis.
        factor_y: Offset factor along the Y axis.
        factor_z: Offset factor along the Z axis.
    """
    db = get_db_session()
    repo = ArrayModifierRepository(db)

    updates = {}
    for field, value in [
        ("count", count), ("offset_type", offset_type),
        ("factor_x", factor_x), ("factor_y", factor_y), ("factor_z", factor_z),
    ]:
        if value is not None:
            updates[field] = value

    if not updates:
        return {"id": array_modifier_id, "status": "no changes"}

    result = run_async(repo.update(array_modifier_id, updates))
    if result is None:
        return {"error": f"Array modifier {array_modifier_id} not found"}
    return {"id": array_modifier_id, "status": "updated"}

def delete_array_modifier(array_modifier_id: str) -> Dict[str, Any]:
    """
    Removes the Array modifier from the object.
    
    Args:
        array_modifier_id: Target array modifier ID.
    """
    db = get_db_session()
    repo = ArrayModifierRepository(db)
    deleted = run_async(repo.delete(array_modifier_id))
    if not deleted:
        return {"error": f"Array modifier {array_modifier_id} not found"}
    return {"id": array_modifier_id, "status": "deleted"}
