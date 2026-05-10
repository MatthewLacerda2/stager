# Stager AI Agent: Tool Definitions & Specification

This document defines the tools available to the Gemini agentic loop for manipulating 3D scenes in Blender via our FastAPI backend. 

## Design Principles for the AI Assistant
1. **Implicit Scene Context:** The agent does **not** need to pass `scene_id`. The backend middleware injects the active workspace context automatically.
2. **Atomic CRUD & Optionality:** `update_*` tools must treat all arguments except the target `id` as optional. Only update provided fields.
3. **Flat Hierarchy:** Groups act strictly as Blender Empties. Modifiers are managed sequentially via an integer index.

---

## 1. Discovery & Awareness Tools

### `search_library_objects`
* **Purpose:** Searches the immutable base asset pool (`blender_objects`) using semantic text matching.
* **Arguments:**
  * `query` (string, required): Plain English description of the desired object (e.g., "mid-century modern wooden chair").
  * `limit` (integer, optional, default: 5): Max results to return.
* **Returns:** A concise JSON list of matched assets containing only `id`, `name`, and a brief summary to conserve context tokens.

### `search_scene_objects`
* **Purpose:** Semantically searches instances (`scene_objects` and `group_objects`) *currently instantiated* inside the active scene.
* **Arguments:**
  * `query` (string, required): Description of what to find in the current layout.
* **Returns:** A list of matching scene objects, their current IDs, names, parent groups, and global transform coordinates.

### `describe_scene`
* **Purpose:** Programmatically generates a structured text summary of the current scene state to orient the agent.
* **Arguments:** None.
* **Returns:** A text payload detailing total object counts, group hierarchies, active camera framing, lighting setup, and general layout bounding boxes.

---

## 2. Object Management (Instances)

### `create_object`
* **Purpose:** Instantiates a 3D asset from the library into the active scene.
* **Arguments:**
  * `blender_object_id` (uuid, required): The ID from the asset library.
  * `pos_x`, `pos_y`, `pos_z` (floats, optional, default: 0.0)
  * `rot_x`, `rot_y`, `rot_z` (floats, optional, default: 0.0)
  * `scale_x`, `scale_y`, `scale_z` (floats, optional, default: 1.0)
  * `group_object_id` (uuid, optional, nullable): ID of the parent Empty group.

### `update_object`
* **Purpose:** Modifies transforms or parent associations of an existing scene instance.
* **Arguments:**
  * `scene_object_id` (uuid, required)
  * `pos_x`, `pos_y`, `pos_z` (floats, optional)
  * `rot_x`, `rot_y`, `rot_z` (floats, optional)
  * `scale_x`, `scale_y`, `scale_z` (floats, optional)
  * `group_object_id` (uuid, optional, nullable): Passing a valid UUID sets the parent; passing explicitly `null` unparents the object.

### `delete_object`
* **Purpose:** Deletes an instance entirely from the scene (cascades deletion to its modifier stack).
* **Arguments:**
  * `scene_object_id` (uuid, required)

---

## 3. Group Management (Empties)

### `create_group`
* **Purpose:** Creates a Blender Empty node to act as a shared transform parent for clusters of objects.
* **Arguments:**
  * `name` (string, required, e.g., "dining-table-cluster")
  * `pos_x`, `pos_y`, `pos_z` (floats, optional, default: 0.0)
  * `rot_x`, `rot_y`, `rot_z` (floats, optional, default: 0.0)
  * `scale_x`, `scale_y`, `scale_z` (floats, optional, default: 1.0)

### `update_group`
* **Purpose:** Moves, rotates, or scales an entire group at once.
* **Arguments:**
  * `group_object_id` (uuid, required)
  * `pos_x`, `pos_y`, `pos_z` (floats, optional)
  * `rot_x`, `rot_y`, `rot_z` (floats, optional)
  * `scale_x`, `scale_y`, `scale_z` (floats, optional)

### `delete_group`
* **Purpose:** Removes the group Empty node. Backend safely detaches/unparents all child objects.
* **Arguments:**
  * `group_object_id` (uuid, required)

---

## 4. Modifier Stack Management

### `create_modifier`
* **Purpose:** Applies a procedural Blender modifier to a specific scene instance.
* **Arguments:**
  * `scene_object_id` (uuid, required)
  * `type` (string, required): Default Blender modifier enum/string (e.g., "ARRAY", "MIRROR", "BEVEL").
  * `order_index` (integer, required): The target zero-based placement index in the stack. Backend shifts existing subsequent modifiers down automatically.
  * `data` (jsonb, required): Valid configuration payload for the modifier properties.

### `update_modifier`
* **Purpose:** Updates the parameters or the stack order of an existing modifier.
* **Arguments:**
  * `modifier_id` (uuid, required)
  * `order_index` (integer, optional): New target position in the execution stack.
  * `data` (jsonb, optional): Updated settings payload.

### `delete_modifier`
* **Purpose:** Removes a modifier from an object's stack and recalculates execution orders.
* **Arguments:**
  * `modifier_id` (uuid, required)

---

## 5. Illumination (Lights)

### `create_light`
* **Purpose:** Instantiates a new light source in the scene.
* **Arguments:**
  * `type` (string, required): Options -> `POINT`, `SUN`, `SPOT`, `AREA`.
  * `pos_x`, `pos_y`, `pos_z` (floats, optional, default: 0.0)
  * `rot_x`, `rot_y`, `rot_z` (floats, optional, default: 0.0)
  * `scale_x`, `scale_y`, `scale_z` (floats, optional, default: 1.0)
  * `color` (string, optional, default: "#FFFFFF"): Hex color string.
  * `intensity` (float, optional, default: 100.0): Energy/power value.

### `update_light`
* **Purpose:** Modifies existing light properties.
* **Arguments:**
  * `light_id` (uuid, required)
  * Optional transforms (`pos_*`, `rot_*`, `scale_*`), `color`, or `intensity`.

### `delete_light`
* **Purpose:** Removes a light source from the scene.
* **Arguments:**
  * `light_id` (uuid, required)

---

## 6. Framing & Cameras

### `create_camera`
* **Purpose:** Places a new camera viewpoint into the layout.
* **Arguments:**
  * `name` (string, required, e.g., "Close-up Shot")
  * `pos_x`, `pos_y`, `pos_z` (floats, optional, default: 0.0)
  * `rot_x`, `rot_y`, `rot_z` (floats, optional, default: 0.0)
  * `fov` (float, optional, default: 50.0): Field of View in millimeters/degrees.
  * `width` (integer, optional, default: 1920): Render output width.
  * `height` (integer, optional, default: 1080): Render output height.
  * `is_active` (boolean, optional, default: true): Whether this is the primary render camera.

### `update_camera`
* **Purpose:** Adjusts framing, resolution, or focal settings.
* **Arguments:**
  * `camera_id` (uuid, required)
  * Optional transforms (`pos_*`, `rot_*`), `fov`, `width`, `height`, or `is_active`. 
  * *Note:* If `is_active` is updated to `true`, backend must automatically toggle all other scene cameras to `false`.

### `delete_camera`
* **Purpose:** Removes a camera.
* **Arguments:**
  * `camera_id` (uuid, required)

---

## 7. Visual Feedback & Export

### `render_scene`
* **Purpose:** Fires the rendering pipeline.
* **Arguments:**
  * `camera_id` (uuid, optional): Defaults to active camera if omitted.
  * `is_sketch` (boolean, optional): If true, triggers a fast, lower-quality render (Viewport/Eevee).
* **Returns:** The database record payload from the `renders` table, including the final `image_url`.