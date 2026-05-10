import bpy
import sys
import os

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
    print(f"Unsupported file type: {ext}")
    sys.exit(1)

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

# Join all meshes
meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
if not meshes:
    print("No meshes found in file.")
    sys.exit(1)

for obj in meshes:
    obj.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
if len(meshes) > 1:
    bpy.ops.object.join()

# Export
bpy.ops.wm.obj_export(filepath=output_file, export_selected_objects=True)
print(f"Successfully extracted to {output_file}")
