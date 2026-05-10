# stager
Create and visualize 3D scenarios with plain English text prompts. No artistic skill required.

It's similar to lovable.dev in the sense it's not meant for production-grade art, nor does it replace professional artists. It gets you good stuff fast.

# Architecture

The frontend sends the request to our api
The Api creates an agentic loop:
	It sends a request to Gemini with tools at it's disposal
  Gemini calls the tools. They:
    - update the db and tell the API how to update the frontend
	  - may move, rotate and scale stuff, change lights and materials
	  - are meant to remove as much cognitive load from the AI as possible
    - should allow for any operation in the least amount of tool calls

There is a pool of objects the AI can pick from, much like 3D artists do in Sketchfab.
The AI can also instantiate primitives.

The AI does NOT:
- Create brand new models.
- Animate things.

The tools are Python functions that manipulate Blender.

## Folder Structure

- /backend
  - /core (app's configurations)
  - /models
  - /repositories
  - /schemas
  - /api
    - /v1
  - /services (pipelines and tools)
    - /agents
    - /tools
  - /utils (contains utility functions)

## Database

- scenes: name, brief_description, detailed_description, embeddings
- chats: scene_id, created_at
- chat_turns: chat_id, user_prompt, agent_response
- agent_logs: chat_turn_id, tool_name, tool_input, tool_output
- blender_objects: name, description, description_embedding, asset_path
- group_objects: scene_id, name, pos, rot, scale
- scene_objects: scene_id, blender_object_id, group_object_id, pos, rot, scale
- array_modifiers: scene_object_id, count, offset_type, factor_x, factor_y, factor_z
- lights: scene_id, type, pos, rot, scale, color, intensity
- cameras: scene_id, name, pos, rot, fov, is_active
- renders: scene_id, camera_id, image_url, description, embeddings

## AI Tools

- search_library_objects: Semantic search over the base asset pool.
- search_scene_objects: Semantic search over objects currently in the active scene.
- describe_scene: Get a structured summary of the objects and their placement in the scene.
- create_object: Instantiate a 3D asset from the library into the scene.
- update_object: Modify transforms or parenting of a scene object.
- delete_object: Remove a scene object and its modifiers.
- create_group: Create an Empty node to group multiple objects.
- update_group: Move, rotate, or scale an entire group.
- delete_group: Remove a group and optionally delete its children.
- create_array_modifier: Apply an Array modifier to duplicate an object along an axis.
- update_array_modifier: Update parameters of an existing Array modifier.
- delete_array_modifier: Remove the Array modifier from an object.
- create_light: Instantiate a new light source (POINT, SUN, SPOT, AREA).
- update_light: Modify properties of an existing light.
- delete_light: Remove a light source.
- create_camera: Place a new camera viewpoint in the layout.
- update_camera: Adjust framing, resolution, or focal settings.
- delete_camera: Remove a camera.
- sketch_scene: Trigger a fast, lower-quality render for visual confirmation.
- render_scene: Trigger the high-fidelity production rendering pipeline.

# Tech stack

- Alembic (Database Migration)
- FastAPI
  - SQLAlchemy (ORM)
  - Gemini
  - Blender CLI and Python API (bpy)
- PostgreSQL
- React + Vite + TS
  - React Three Fiber
  - Three.js
  - GLTF

# How to run

`docker-compose build && docker-compose up -d`
`alembic upgrade head`

Or, you can run it locally:
`python -m venv venv`
`source venv/bin/activate`
`pip install -r requirements.txt`
`uvicorn app.main:app --reload`

In a separate terminal:
`cd frontend`
`npm i && npm run dev`