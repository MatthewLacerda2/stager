import os
import bpy
import sys
import math
from mathutils import Vector

def process(input_obj, output_dir):
    # Clear scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Import object
    bpy.ops.wm.obj_import(filepath=input_obj)
    meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
    if not meshes:
        raise ValueError("No meshes found.")

    for obj in meshes:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    if len(meshes) > 1:
        bpy.ops.object.join()

    target = bpy.context.active_object

    # Calculate bounding sphere radius
    local_bbox_corners = [Vector(corner) for corner in target.bound_box]
    center_local = sum(local_bbox_corners, Vector()) / 8.0
    center_world = target.matrix_world @ center_local

    radius = max((target.matrix_world @ v - center_world).length for v in local_bbox_corners)

    # Create an Empty at the center for the camera to pivot around
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=center_world)
    pivot = bpy.context.active_object

    # Setup Camera
    bpy.ops.object.camera_add(location=(center_world.x, center_world.y - 1, center_world.z))
    cam = bpy.context.active_object
    cam.data.lens = 35.0  # 35mm focal length

    # Calculate optimal camera distance based on FOV
    fov = cam.data.angle
    distance = (radius * 1.3) / math.sin(fov / 2.0)  # 1.3 padding to ensure it fits perfectly

    cam.location = (center_world.x, center_world.y - distance, center_world.z)

    # Parent camera to pivot and track the center
    cam.parent = pivot
    track = cam.constraints.new(type='TRACK_TO')
    track.target = pivot
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'

    bpy.context.scene.camera = cam

    # Setup Lighting
    bpy.ops.object.light_add(type='SUN', location=(center_world.x + 5, center_world.y - 5, center_world.z + 10))
    light1 = bpy.context.object
    light1.data.energy = 3.0

    bpy.ops.object.light_add(type='SUN', location=(center_world.x - 5, center_world.y + 5, center_world.z + 5))
    light2 = bpy.context.object
    light2.data.energy = 1.0

    # Render settings
    # EEVEE was replaced by EEVEE-Next (BLENDER_EEVEE_NEXT) in newer Blender releases (4.2+)
    try:
        bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    except Exception:
        try:
            bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
        except Exception:
            bpy.context.scene.render.engine = 'BLENDER_WORKBENCH'
            
    bpy.context.scene.render.resolution_x = 720
    bpy.context.scene.render.resolution_y = 720

    # Create output dir
    os.makedirs(output_dir, exist_ok=True)

    # Render 5 pictures
    angles = 5
    images = []
    for i in range(angles):
        # Rotate pivot around Z axis (360/5 = 72 degrees)
        pivot.rotation_euler[2] = math.radians(i * (360.0 / angles))
        bpy.context.view_layer.update()
        
        filepath = os.path.join(output_dir, f"shot_{i}.png")
        bpy.context.scene.render.filepath = filepath
        bpy.ops.render.render(write_still=True)
        images.append(filepath)
        
    return images

if __name__ == "__main__":
    argv = sys.argv
    if "--" not in argv:
        print("Error: No arguments provided.")
        sys.exit(1)

    args = argv[argv.index("--") + 1:]
    if len(args) < 2:
        print("Usage: blender -b -P photoshoot.py -- <input_obj> <output_dir>")
        sys.exit(1)

    input_obj = args[0]
    output_dir = args[1]
    
    process(input_obj, output_dir)
    print(f"Photoshoot complete! Saved to {output_dir}")
