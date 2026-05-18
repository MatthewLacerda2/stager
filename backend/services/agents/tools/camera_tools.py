import math
from typing import Optional, Dict, Any
from ..context import get_scene_id, get_db_session
from ....repositories.camera_repository import CameraRepository

async def create_camera(
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
        await repo.deactivate_all(scene_id)

    cam = await repo.create({
        "scene_id": scene_id, "name": name,
        "pos_x": pos_x, "pos_y": pos_y, "pos_z": pos_z,
        "rot_x": rot_x, "rot_y": rot_y, "rot_z": rot_z,
        "fov": fov, "is_active": is_active,
    })
    return {"id": str(cam.id), "status": "created"}

async def update_camera(
    camera_id: str,
    pos_x: float = None, pos_y: float = None, pos_z: float = None,
    rot_x: float = None, rot_y: float = None, rot_z: float = None,
    fov: float = None,
    is_active: bool = None
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
        await repo.deactivate_all(scene_id)

    result = await repo.update(camera_id, updates)
    if result is None:
        return {"error": f"Camera {camera_id} not found"}
    return {"id": camera_id, "status": "updated"}

async def delete_camera(camera_id: str) -> Dict[str, Any]:
    """
    Removes a camera.
    
    Args:
        camera_id: Target camera ID.
    """
    db = get_db_session()
    repo = CameraRepository(db)
    deleted = await repo.delete(camera_id)
    if not deleted:
        return {"error": f"Camera {camera_id} not found"}
    return {"id": camera_id, "status": "deleted"}

async def camera_look_at(
    camera_id: str,
    target_x: float,
    target_y: float,
    target_z: float
) -> Dict[str, Any]:
    """
    Rotates a camera to face a specific target point in 3D space, analogous to Transform.LookAt() in Unity.
    
    Args:
        camera_id: Target camera ID.
        target_x: X coordinate of the target point.
        target_y: Y coordinate of the target point.
        target_z: Z coordinate of the target point.
    """
    db = get_db_session()
    repo = CameraRepository(db)
    
    camera = await repo.get_by_id(camera_id)
    if not camera:
        return {"error": f"Camera {camera_id} not found"}
        
    pos_x = camera.pos_x if camera.pos_x is not None else 0.0
    pos_y = camera.pos_y if camera.pos_y is not None else 0.0
    pos_z = camera.pos_z if camera.pos_z is not None else 0.0
    
    dx = target_x - pos_x
    dy = target_y - pos_y
    dz = target_z - pos_z
    
    dist = math.sqrt(dx**2 + dy**2 + dz**2)
    if dist < 1e-6:
        return {"error": "Camera position and target position are identical; cannot determine look direction."}
        
    # Normalized forward vector pointing from camera to target
    fx = dx / dist
    fy = dy / dist
    fz = dz / dist
    
    # Check for singularity (looking straight up or down)
    horizontal_dist = math.sqrt(fx**2 + fy**2)
    if horizontal_dist < 1e-6:
        if fz > 0:
            rot_x = 180.0
            rot_y = 0.0
            rot_z = 0.0
        else:
            rot_x = 0.0
            rot_y = 0.0
            rot_z = 0.0
    else:
        # General case (not looking straight up/down)
        # alpha (X rotation / pitch)
        alpha = math.atan2(horizontal_dist, -fz)
        # beta (Y rotation / roll) is 0 because we keep the camera's local X-axis parallel to the world XY plane
        beta = 0.0
        # gamma (Z rotation / yaw)
        gamma = math.atan2(-fx, fy)
        
        rot_x = math.degrees(alpha)
        rot_y = math.degrees(beta)
        rot_z = math.degrees(gamma)
        
    result = await repo.update(camera_id, {
        "rot_x": rot_x,
        "rot_y": rot_y,
        "rot_z": rot_z
    })
    
    if result is None:
        return {"error": f"Camera {camera_id} not found during update"}
        
    return {
        "id": camera_id,
        "status": "updated",
        "rotation": {"rot_x": rot_x, "rot_y": rot_y, "rot_z": rot_z}
    }
