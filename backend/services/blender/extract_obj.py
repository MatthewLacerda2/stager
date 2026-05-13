import bpy
import sys
import os
import json
from mathutils import Vector

def process(input_file, output_file):
    # Clear scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Import
    ext = os.path.splitext(input_file)[1].lower()
    if ext == '.blend':
        bpy.ops.wm.open_mainfile(filepath=input_file)
    elif ext == '.obj':
        bpy.ops.wm.obj_import(filepath=input_file)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    # Set frame to 0
    bpy.context.scene.frame_set(0)

    # Apply modifiers to all meshes
    meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
    for obj in meshes:
        bpy.context.view_layer.objects.active = obj
        for mod in obj.modifiers:
            try:
                bpy.ops.object.modifier_apply(modifier=mod.name)
            except Exception as e:
                print(f"Could not apply modifier {mod.name}: {e}")

    # Delete non-meshes (lights, cameras, etc)
    for obj in bpy.context.scene.objects:
        if obj.type != 'MESH':
            obj.select_set(True)
        else:
            obj.select_set(False)
    bpy.ops.object.delete()

    # Join all meshes first to unify everything before separating
    meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
    if not meshes:
        raise ValueError("No meshes found in file.")

    for obj in meshes:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    if len(meshes) > 1:
        bpy.ops.object.join()

    # Separate the unified mesh by loose parts (mesh islands)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.mode_set(mode='OBJECT')

    # Get all the resulting separated mesh objects
    separated_meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
    
    extracted_objects = []
    base_dir = os.path.dirname(output_file)
    base_name = os.path.splitext(os.path.basename(output_file))[0]

    for idx, target in enumerate(separated_meshes):
        # Select ONLY this specific object
        bpy.ops.object.select_all(action='DESELECT')
        target.select_set(True)
        bpy.context.view_layer.objects.active = target

        # Calculate bounding box and sphere radius
        local_bbox_corners = [Vector(corner) for corner in target.bound_box]
        center_local = sum(local_bbox_corners, Vector()) / 8.0
        center_world = target.matrix_world @ center_local

        dimensions = target.dimensions
        boundbox_x = dimensions.x
        boundbox_y = dimensions.y
        boundbox_z = dimensions.z

        boundbox_offset_x = center_world.x
        boundbox_offset_y = center_world.y
        boundbox_offset_z = center_world.z

        radius = max((target.matrix_world @ v - center_world).length for v in local_bbox_corners)
        radius_offset_x = center_world.x
        radius_offset_y = center_world.y
        radius_offset_z = center_world.z

        bounds_data = {
            "boundbox_x": boundbox_x,
            "boundbox_y": boundbox_y,
            "boundbox_z": boundbox_z,
            "boundbox_offset_x": boundbox_offset_x,
            "boundbox_offset_y": boundbox_offset_y,
            "boundbox_offset_z": boundbox_offset_z,
            "radius": radius,
            "radius_offset_x": radius_offset_x,
            "radius_offset_y": radius_offset_y,
            "radius_offset_z": radius_offset_z,
        }

        # Use an indexed file name for each sub-mesh island
        part_output_file = os.path.join(base_dir, f"{base_name}_{idx}.obj")

        # Export the selected part
        bpy.ops.wm.obj_export(filepath=part_output_file, export_selected_objects=True)

        extracted_objects.append({
            "output_file": part_output_file,
            "bounds": bounds_data
        })

    return extracted_objects

if __name__ == "__main__":
    # Parse arguments passed after "--"
    argv = sys.argv
    if "--" not in argv:
        print("Error: No arguments provided.")
        sys.exit(1)

    args = argv[argv.index("--") + 1:]
    if len(args) < 2:
        print("Usage: blender -b -P extract_obj.py -- <input_file> <output_obj>")
        sys.exit(1)

    input_file = args[0]
    output_file = args[1]
    
    bounds = process(input_file, output_file)
    
    # Write sidecar for legacy CLI caller
    bounds_file = os.path.splitext(output_file)[0] + "_bounds.json"
    with open(bounds_file, "w") as f:
        json.dump(bounds, f)
        
    print(f"Successfully extracted to {output_file}")

