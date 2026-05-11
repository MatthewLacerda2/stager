# blender -b -P render_test.py
import os
import bpy

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create 8x8 plane
bpy.ops.mesh.primitive_plane_add(size=8, location=(0, 0, 0))
plane = bpy.context.object
plane.name = "BasePlane"

# Create box
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
box = bpy.context.object
box.name = "Box"

# Create triangle (using a cone with 3 vertices)
bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=1, depth=1, location=(0, 0, 3))
triangle = bpy.context.object
triangle.name = "Triangle"

# Materials
def create_material(name, color):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes["Principled BSDF"].inputs[0].default_value = color
    return mat

plane.data.materials.append(create_material("WhiteMat", (1, 1, 1, 1)))
box.data.materials.append(create_material("GreenMat", (0, 1, 0, 1)))
triangle.data.materials.append(create_material("RedMat", (1, 0, 0, 1)))

# Light
bpy.ops.object.light_add(type='SUN', location=(5, 5, 5))
light = bpy.context.object
light.data.energy = 2

# Camera
bpy.ops.object.camera_add(location=(10, -10, 10))
cam = bpy.context.object
cam.rotation_euler = (1.1, 0, 0.78)
bpy.context.scene.camera = cam

# Render settings
bpy.context.scene.render.resolution_x = 720
bpy.context.scene.render.resolution_y = 720
bpy.context.scene.render.filepath = os.path.abspath('test_render.png')
bpy.ops.render.render(write_still=True)

# Save .blend file
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath('test_scene.blend'))
print("Successfully generated test_render.png and test_scene.blend!")
