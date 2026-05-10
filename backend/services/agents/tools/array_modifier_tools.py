from typing import Optional, Dict, Any

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
    pass

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
    pass

def delete_array_modifier(array_modifier_id: str) -> Dict[str, Any]:
    """
    Removes the Array modifier from the object.
    
    Args:
        array_modifier_id: Target array modifier ID.
    """
    pass
