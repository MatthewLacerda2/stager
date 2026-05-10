from typing import Optional, Dict, Any

def create_object(
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
    pass

def update_object(
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
    pass

def delete_object(scene_object_id: str) -> Dict[str, Any]:
    """
    Deletes an instance entirely from the scene.
    
    Args:
        scene_object_id: Target scene object ID.
    """
    pass
