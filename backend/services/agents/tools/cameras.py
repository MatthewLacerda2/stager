from typing import Optional, Dict, Any

def create_camera(
    name: str,
    pos_x: float = 0.0, pos_y: float = 0.0, pos_z: float = 0.0,
    rot_x: float = 0.0, rot_y: float = 0.0, rot_z: float = 0.0,
    fov: float = 50.0,
    width: int = 1920,
    height: int = 1080,
    is_active: bool = True
) -> Dict[str, Any]:
    """
    Places a new camera viewpoint into the layout.
    
    Args:
        name: Name of the camera, e.g., "Close-up Shot".
        pos_x: X position coordinate.
        pos_y: Y position coordinate.
        pos_z: Z position coordinate.
        rot_x: X rotation coordinate in degrees.
        rot_y: Y rotation coordinate in degrees.
        rot_z: Z rotation coordinate in degrees.
        fov: Field of View in millimeters/degrees.
        width: Render output width.
        height: Render output height.
        is_active: Whether this is the primary render camera.
    """
    pass

def update_camera(
    camera_id: str,
    pos_x: Optional[float] = None, pos_y: Optional[float] = None, pos_z: Optional[float] = None,
    rot_x: Optional[float] = None, rot_y: Optional[float] = None, rot_z: Optional[float] = None,
    fov: Optional[float] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    is_active: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Adjusts framing, resolution, or focal settings. Only provided fields will be updated.
    Note: If is_active is updated to true, backend automatically toggles all other scene cameras to false.
    
    Args:
        camera_id: Target camera ID.
        pos_x: X position coordinate.
        pos_y: Y position coordinate.
        pos_z: Z position coordinate.
        rot_x: X rotation coordinate in degrees.
        rot_y: Y rotation coordinate in degrees.
        rot_z: Z rotation coordinate in degrees.
        fov: Field of View in millimeters/degrees.
        width: Render output width.
        height: Render output height.
        is_active: Whether this is the primary render camera.
    """
    pass

def delete_camera(camera_id: str) -> Dict[str, Any]:
    """
    Removes a camera.
    
    Args:
        camera_id: Target camera ID.
    """
    pass
