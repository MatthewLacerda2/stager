from typing import Optional, Dict, Any

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
    pass

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
    pass

def delete_group(group_object_id: str, delete_children: bool = False) -> Dict[str, Any]:
    """
    Removes the group Empty node.
    
    Args:
        group_object_id: Target group object ID.
        delete_children: If true, all child objects are also deleted. If false, all children are safely detached with the transformations preserved.
    """
    pass
