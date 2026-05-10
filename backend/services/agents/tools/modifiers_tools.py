from typing import Optional, Dict, Any

def create_modifier(
    scene_object_id: str,
    type: str,
    order_index: int,
    data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Applies a procedural Blender modifier to a specific scene instance.
    
    Args:
        scene_object_id: Target scene object ID.
        type: Default Blender modifier enum/string (e.g., "ARRAY", "MIRROR", "BEVEL").
        order_index: The zero-based placement index in the modifiers stack. Backend shifts existing subsequent modifiers down automatically.
        data: Valid configuration payload for the modifier properties.
    """
    pass

def update_modifier(
    modifier_id: str,
    order_index: Optional[int] = None,
    data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Updates the parameters or the stack order of an existing modifier. Only provided fields will be updated.
    
    Args:
        modifier_id: Target modifier ID.
        order_index: New target position in the execution stack.
        data: Updated settings payload.
    """
    pass

def delete_modifier(modifier_id: str) -> Dict[str, Any]:
    """
    Removes a modifier from an object's stack and recalculates execution orders.
    
    Args:
        modifier_id: Target modifier ID.
    """
    pass
