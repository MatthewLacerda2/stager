from typing import Optional, Dict, Any

def create_light(
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
    pass

def update_light(
    light_id: str,
    pos_x: Optional[float] = None, pos_y: Optional[float] = None, pos_z: Optional[float] = None,
    rot_x: Optional[float] = None, rot_y: Optional[float] = None, rot_z: Optional[float] = None,
    scale_x: Optional[float] = None, scale_y: Optional[float] = None, scale_z: Optional[float] = None,
    color: Optional[str] = None,
    intensity: Optional[float] = None
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
    pass

def delete_light(light_id: str) -> Dict[str, Any]:
    """
    Removes a light source from the scene.
    
    Args:
        light_id: Target light ID.
    """
    pass
