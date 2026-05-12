"""Helpers shared across endpoint modules."""
from ..models.scene import Scene
from ..schemas.scene import (
    SceneState, SceneObjectState, LightState, GroupObjectState,
    Vector3D, Transform3D,
)


def build_scene_state(scene: Scene) -> SceneState:
    """Build a SceneState schema from a fully-loaded Scene ORM instance.

    Expects that `scene.scene_objects` (with `.blender_object`),
    `scene.lights`, and `scene.group_objects` are eagerly loaded.
    """
    objects = [
        SceneObjectState(
            id=so.id,
            name=so.blender_object.name or "",
            blender_object_id=so.blender_object_id,
            group_object_id=so.group_object_id,
            transform=Transform3D(
                pos=Vector3D(x=so.pos_x, y=so.pos_y, z=so.pos_z),
                rot=Vector3D(x=so.rot_x, y=so.rot_y, z=so.rot_z),
                scale=Vector3D(x=so.scale_x, y=so.scale_y, z=so.scale_z),
            ),
        )
        for so in scene.scene_objects
    ]
    lights = [
        LightState(
            id=lt.id,
            type=lt.type,
            transform=Transform3D(
                pos=Vector3D(x=lt.pos_x, y=lt.pos_y, z=lt.pos_z),
                rot=Vector3D(x=lt.rot_x, y=lt.rot_y, z=lt.rot_z),
                scale=Vector3D(x=lt.scale_x, y=lt.scale_y, z=lt.scale_z),
            ),
            color=lt.color,
            intensity=lt.intensity,
        )
        for lt in scene.lights
    ]
    groups = [
        GroupObjectState(
            id=go.id,
            name=go.name or "",
            transform=Transform3D(
                pos=Vector3D(x=go.pos_x, y=go.pos_y, z=go.pos_z),
                rot=Vector3D(x=go.rot_x, y=go.rot_y, z=go.rot_z),
                scale=Vector3D(x=go.scale_x, y=go.scale_y, z=go.scale_z),
            ),
        )
        for go in scene.group_objects
    ]
    return SceneState(objects=objects, lights=lights, groups=groups)
