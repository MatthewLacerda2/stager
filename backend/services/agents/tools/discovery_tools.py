from typing import List, Dict, Any
from ..context import get_scene_id, get_db_session
from ....services.gemini_embedding import get_gemini_embedding
from ....repositories.blender_object_repository import BlenderObjectRepository
from ....repositories.scene_object_repository import SceneObjectRepository
from ....repositories.group_object_repository import GroupObjectRepository
from ....repositories.light_repository import LightRepository
from ....repositories.camera_repository import CameraRepository

async def search_library_objects(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Searches the asset pool using semantic text matching.
    
    Args:
        query: Plain English description of the desired object (e.g., "mid-century modern wooden chair").
        limit: Max results to return.
    
    Returns:
        A concise JSON list of matched assets containing only id, name, and a brief summary.
    """
    db = get_db_session()
    embedding = get_gemini_embedding(query)
    repo = BlenderObjectRepository(db)
    results = await repo.semantic_search(embedding, limit=limit)
    return [
        {
            "id": str(obj.id),
            "name": obj.name,
            "description": (obj.description or "")[:1024],
        }
        for obj in results
    ]

async def search_scene_objects(query: str) -> List[Dict[str, Any]]:
    """
    Semantically searches instances (scene_objects and group_objects) currently instantiated inside the active scene.
    
    Args:
        query: Description of what to find in the current layout.
    
    Returns:
        A list of matching scene objects, their current IDs, names, parent groups, and global transform coordinates.
    """
    db = get_db_session()
    scene_id = get_scene_id()
    embedding = get_gemini_embedding(query)
    repo = SceneObjectRepository(db)
    results = await repo.semantic_search(scene_id, embedding)
    return [
        {
            "id": str(so.id),
            "name": so.blender_object.name if so.blender_object else "",
            "blender_object_id": str(so.blender_object_id),
            "group_object_id": str(so.group_object_id) if so.group_object_id else None,
            "group_name": so.group_object.name if so.group_object else None,
            "pos": {"x": so.pos_x, "y": so.pos_y, "z": so.pos_z},
            "rot": {"x": so.rot_x, "y": so.rot_y, "z": so.rot_z},
            "scale": {"x": so.scale_x, "y": so.scale_y, "z": so.scale_z},
        }
        for so in results
    ]

async def describe_scene() -> str:
    """
    Programmatically generates a structured text summary of the objects placements in the scene.
    
    Returns:
        A text payload detailing total object counts, group hierarchies, active camera framing, lighting setup, and general layout bounding boxes.
    """
    db = get_db_session()
    scene_id = get_scene_id()

    so_repo = SceneObjectRepository(db)
    scene_objects = await so_repo.get_all_by_scene_id(scene_id)

    go_repo = GroupObjectRepository(db)
    groups = await go_repo.get_by_scene_id(scene_id)

    light_repo = LightRepository(db)
    lights = await light_repo.get_by_scene_id(scene_id)

    cam_repo = CameraRepository(db)
    cameras = await cam_repo.get_by_scene_id(scene_id)

    lines = []
    lines.append(f"=== Scene Summary ===")
    lines.append(f"Objects: {len(scene_objects)} | Groups: {len(groups)} | Lights: {len(lights)} | Cameras: {len(cameras)}")
    lines.append("")

    if groups:
        lines.append("-- Groups --")
        for g in groups:
            children = [so for so in scene_objects if so.group_object_id == g.id]
            child_names = ", ".join(
                so.blender_object.name for so in children if so.blender_object
            ) or "none"
            lines.append(f"  {g.name} (id={g.id}): pos=({g.pos_x:.1f},{g.pos_y:.1f},{g.pos_z:.1f}) children=[{child_names}]")
        lines.append("")

    ungrouped = [so for so in scene_objects if so.group_object_id is None]
    if ungrouped:
        lines.append("-- Ungrouped Objects --")
        for so in ungrouped:
            name = so.blender_object.name if so.blender_object else "?"
            lines.append(f"  {name} (id={so.id}): pos=({so.pos_x:.1f},{so.pos_y:.1f},{so.pos_z:.1f})")
        lines.append("")

    if lights:
        lines.append("-- Lights --")
        for lt in lights:
            lines.append(f"  {lt.type} (id={lt.id}): pos=({lt.pos_x:.1f},{lt.pos_y:.1f},{lt.pos_z:.1f}) color={lt.color} intensity={lt.intensity}")
        lines.append("")

    if cameras:
        lines.append("-- Cameras --")
        for cam in cameras:
            active = " [ACTIVE]" if cam.is_active else ""
            lines.append(f"  {cam.name}{active} (id={cam.id}): pos=({cam.pos_x:.1f},{cam.pos_y:.1f},{cam.pos_z:.1f}) fov={cam.fov}")

    return "\n".join(lines)
