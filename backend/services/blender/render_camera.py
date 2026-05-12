import bpy
import math
from mathutils import Vector, Euler
import os
import sys

def build_scene(scene_data):
    # Clear scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Create scene objects
    for obj_data in scene_data.get('objects', []):
        asset_path = obj_data.get('asset_path')
        if not asset_path or not os.path.exists(asset_path):
            print(f"Warning: Asset path not found: {asset_path}")
            continue
            
        ext = os.path.splitext(asset_path)[1].lower()
        
        before_import = set(bpy.context.scene.objects)
        if ext == '.blend':
            # Append from blend file
            with bpy.data.libraries.load(asset_path, link=False) as (data_from, data_to):
                data_to.objects = data_from.objects
            for obj in data_to.objects:
                if obj is not None:
                    bpy.context.scene.collection.objects.link(obj)
        elif ext == '.obj':
            bpy.ops.wm.obj_import(filepath=asset_path)
        
        after_import = set(bpy.context.scene.objects)
        new_objects = list(after_import - before_import)
        
        if not new_objects:
            continue
            
        # Group imported objects under an empty to control their transform together
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        parent_empty = bpy.context.active_object
        
        for new_obj in new_objects:
            new_obj.parent = parent_empty
            
        # Apply transforms
        pos = obj_data.get('position', [0, 0, 0])
        rot = obj_data.get('rotation', [0, 0, 0])
        scale = obj_data.get('scale', [1, 1, 1])
        
        parent_empty.location = Vector(pos)
        parent_empty.rotation_euler = Euler((math.radians(rot[0]), math.radians(rot[1]), math.radians(rot[2])), 'XYZ')
        parent_empty.scale = Vector(scale)

    # Setup Lights
    for light_data in scene_data.get('lights', []):
        light_type = light_data.get('type', 'POINT')
        if light_type == 'DIRECTIONAL':
            light_type = 'SUN'
            
        bpy.ops.object.light_add(type=light_type)
        light_obj = bpy.context.active_object
        
        pos = light_data.get('position', [0, 0, 0])
        rot = light_data.get('rotation', [0, 0, 0])
        
        light_obj.location = Vector(pos)
        light_obj.rotation_euler = Euler((math.radians(rot[0]), math.radians(rot[1]), math.radians(rot[2])), 'XYZ')
        
        light_obj.data.energy = light_data.get('intensity', 1.0)
        
        color = light_data.get('color', '#ffffff')
        if isinstance(color, str) and color.startswith('#'):
            h = color.lstrip('#')
            if len(h) >= 6:
                rgb = tuple(int(h[i:i+2], 16)/255.0 for i in (0, 2, 4))
                light_obj.data.color = rgb
        elif isinstance(color, (list, tuple)) and len(color) >= 3:
            light_obj.data.color = color[:3]

    # Setup Camera
    cam_data = scene_data.get('camera', {})
    bpy.ops.object.camera_add()
    cam_obj = bpy.context.active_object
    
    pos = cam_data.get('position', [0, -10, 0])
    rot = cam_data.get('rotation', [90, 0, 0])
    fov = cam_data.get('fov', 60.0)
    
    cam_obj.location = Vector(pos)
    cam_obj.rotation_euler = Euler((math.radians(rot[0]), math.radians(rot[1]), math.radians(rot[2])), 'XYZ')
    cam_obj.data.angle = math.radians(fov)
    
    bpy.context.scene.camera = cam_obj

def process(scene_data, output_path, is_sketch=False):
    build_scene(scene_data)
    
    # Render settings
    # CYCLES is a pure software-based CPU raytracer that runs 100% stably in headless Linux environments.
    bpy.context.scene.render.engine = 'CYCLES'
    try:
        bpy.context.scene.cycles.device = 'CPU'
        if is_sketch:
            bpy.context.scene.cycles.samples = 16  # Ultra low samples for blazing-fast renders
        else:
            bpy.context.scene.cycles.samples = 256 # High quality
    except Exception as e:
        print(f"Warning setting up cycles: {e}")
        pass
        
    # Disable denoising since Debian/Ubuntu apt builds of Blender often omit Intel OpenImageDenoise (OIDN)
    for vl in bpy.context.scene.view_layers:
        try:
            vl.cycles.use_denoising = False
        except Exception:
            pass
            
    bpy.context.scene.render.resolution_x = 720
    bpy.context.scene.render.resolution_y = 720

    # Create output dir
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    bpy.context.scene.render.filepath = output_path
    
    bpy.ops.render.render(write_still=True)
    
    return output_path

if __name__ == "__main__":
    import json
    
    argv = sys.argv
    if "--" not in argv:
        print("Error: No arguments provided.")
        sys.exit(1)

    args = argv[argv.index("--") + 1:]
    if len(args) < 3:
        print("Usage: blender -b -P render_camera.py -- <scene_json_path> <output_path> <is_sketch>")
        sys.exit(1)

    scene_json_path = args[0]
    output_path = args[1]
    is_sketch = args[2].lower() == 'true'
    
    with open(scene_json_path, 'r') as f:
        scene_data = json.load(f)
        
    process(scene_data, output_path, is_sketch)
    print(f"Render complete! Saved to {output_path}")
