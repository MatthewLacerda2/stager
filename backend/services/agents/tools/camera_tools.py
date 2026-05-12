from typing import Optional, Dict, Any
from ..context import get_scene_id, get_db_session, run_async
from ....repositories.camera_repository import CameraRepository

def create_camera(
    name: str,
    pos_x: float = 0.0, pos_y: float = 0.0, pos_z: float = 0.0,
    rot_x: float = 0.0, rot_y: float = 0.0, rot_z: float = 0.0,
    fov: float = 50.0,
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
        is_active: Whether this is the primary render camera.
    """
    db = get_db_session()
    scene_id = get_scene_id()
    repo = CameraRepository(db)

    if is_active:
        run_async(repo.deactivate_all(scene_id))

    cam = run_async(repo.create({
        "scene_id": scene_id, "name": name,
        "pos_x": pos_x, "pos_y": pos_y, "pos_z": pos_z,
        "rot_x": rot_x, "rot_y": rot_y, "rot_z": rot_z,
        "fov": fov, "is_active": is_active,
    }))
    return {"id": str(cam.id), "status": "created"}

def update_camera(
    camera_id: str,
    pos_x: Optional[float] = None, pos_y: Optional[float] = None, pos_z: Optional[float] = None,
    rot_x: Optional[float] = None, rot_y: Optional[float] = None, rot_z: Optional[float] = None,
    fov: Optional[float] = None,
    is_active: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Adjusts framing, resolution, or focal settings. Only provided fields will be updated.
    
    Args:
        camera_id: Target camera ID.
        pos_x: X position coordinate.
        pos_y: Y position coordinate.
        pos_z: Z position coordinate.
        rot_x: X rotation coordinate in degrees.
        rot_y: Y rotation coordinate in degrees.
        rot_z: Z rotation coordinate in degrees.
        fov: Field of View in millimeters/degrees.
        is_active: Whether this is the primary render camera.
    """
    db = get_db_session()
    repo = CameraRepository(db)
    updates = {}
    for field, value in [
        ("pos_x", pos_x), ("pos_y", pos_y), ("pos_z", pos_z),
        ("rot_x", rot_x), ("rot_y", rot_y), ("rot_z", rot_z),
        ("fov", fov), ("is_active", is_active),
    ]:
        if value is not None:
            updates[field] = value
    if not updates:
        return {"id": camera_id, "status": "no changes"}

    if is_active is True:
        scene_id = get_scene_id()
        run_async(repo.deactivate_all(scene_id))

    result = run_async(repo.update(camera_id, updates))
    if result is None:
        return {"error": f"Camera {camera_id} not found"}
    return {"id": camera_id, "status": "updated"}

def delete_camera(camera_id: str) -> Dict[str, Any]:
    """
    Removes a camera.
    
    Args:
        camera_id: Target camera ID.
    """
    db = get_db_session()
    repo = CameraRepository(db)
    deleted = run_async(repo.delete(camera_id))
    if not deleted:
        return {"error": f"Camera {camera_id} not found"}
    return {"id": camera_id, "status": "deleted"}
