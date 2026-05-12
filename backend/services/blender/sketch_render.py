import os
import uuid
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from ...repositories.scene_repository import SceneRepository
from .blender_processor import run_blender_render_camera

async def render_scene_blender(db: AsyncSession, scene_uuid: str, camera_id: str, is_sketch: bool = False) -> str:
    """
    Renders the scene from the specified camera viewpoint and returns the saved file path.
    """
    scene_repo = SceneRepository(db)
    scene = await scene_repo.get_full_scene(scene_uuid)
    if not scene:
        raise ValueError(f"Scene {scene_uuid} not found.")

    target_camera = next((c for c in scene.cameras if str(c.id) == camera_id), None)
    if not target_camera:
        raise ValueError(f"Camera {camera_id} not found in scene.")

    # Serialize scene for blender worker
    scene_data = {
        "objects": [],
        "lights": [],
        "camera": {
            "position": [target_camera.pos_x or 0, target_camera.pos_y or 0, target_camera.pos_z or 0],
            "rotation": [target_camera.rot_x or 0, target_camera.rot_y or 0, target_camera.rot_z or 0],
            "fov": target_camera.fov or 60.0
        }
    }

    for so in scene.scene_objects:
        if so.blender_object and so.blender_object.asset_path:
            scene_data["objects"].append({
                "asset_path": so.blender_object.asset_path,
                "position": [so.pos_x or 0, so.pos_y or 0, so.pos_z or 0],
                "rotation": [so.rot_x or 0, so.rot_y or 0, so.rot_z or 0],
                "scale": [so.scale_x or 1, so.scale_y or 1, so.scale_z or 1]
            })

    for light in scene.lights:
        scene_data["lights"].append({
            "type": light.type or "POINT",
            "position": [light.pos_x or 0, light.pos_y or 0, light.pos_z or 0],
            "rotation": [light.rot_x or 0, light.rot_y or 0, light.rot_z or 0],
            "intensity": light.intensity or 1.0,
            "color": light.color or "#ffffff"
        })

    render_id = str(uuid.uuid4())
    # Save renders to storage/renders/{scene_uuid}/render_{render_id}.png
    output_path = os.path.join("storage", "renders", scene_uuid, f"render_{render_id}.png")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Run the blocking network request in a thread pool to avoid blocking the event loop
    image_path = await asyncio.to_thread(run_blender_render_camera, scene_data, output_path, is_sketch)
    
    return image_path
