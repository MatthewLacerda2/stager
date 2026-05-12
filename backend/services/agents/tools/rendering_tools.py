from typing import Optional, Dict, Any
from ..context import get_scene_id, get_db_session, run_async
from ....repositories.render_repository import RenderRepository
from ....repositories.camera_repository import CameraRepository
from ...blender.sketch_render import render_scene_sketch

def render_scene(camera_id: Optional[str] = None, is_sketch: bool = False) -> Dict[str, Any]:
    """
    Fires the rendering pipeline.
    
    Args:
        camera_id: Target viewpoint. If omitted, uses the active scene camera.
        is_sketch: If true, triggers a fast lower-quality render.
        
    Returns:
        The database record payload from the renders table, including the final image_url.
    """
    db = get_db_session()
    scene_id = get_scene_id()

    if camera_id is None:
        cam_repo = CameraRepository(db)
        active_cam = run_async(cam_repo.get_active_camera(scene_id))
        if active_cam is None:
            return {"error": "No active camera in the scene. Create one first."}
        camera_id = str(active_cam.id)

    image_url = render_scene_sketch(str(scene_id), camera_id)

    repo = RenderRepository(db)
    render = run_async(repo.create({
        "scene_id": scene_id,
        "camera_id": camera_id,
        "is_sketch": is_sketch,
        "image_url": image_url,
    }))
    return {
        "id": str(render.id),
        "image_url": render.image_url,
        "status": "rendered",
    }
