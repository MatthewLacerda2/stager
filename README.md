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
  - /services
    - /agents
      - /tools
    - /AssetIndexerService
    - /blender
  - /utils (contains utility functions)

## Asset Indexing Pipeline

Pipeline for indexing `.obj` or `.blend` assets.

- **`/services/AssetIndexerService/`** (Orchestrator & DB)
  - `indexer_job.py`: Receives raw files and calls the next scripts.
  - `blender_processor.py`: Wraps these Blender scripts in Python functions.
    - `extract_obj.py`: Extracts only the meshes, merges them, and exports to `.obj`.
    - `photoshoot.py`: Renders pictures around the object from different angles.
  - `ollama_description.py`: Describes the object based on the pictures.
  - `gemini_embedding.py`: Embeds the text description.
  - `save_indexed_obj.py`: Saves the data to the db and the .obj in storage/assets.

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