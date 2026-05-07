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

The App does NOT create objects, AI is not good enough for that yet. We pick from a pool and place them, much like 3D artists do in Sketchfab.

The tools are (mostly) Python scripts that manipulate Blender.

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

- group_objs: group objects in scene with semantic retrieval
- blender_objects: description and embedding, pos, rot, scale, ...
- cameras: render settings, fov, pos, rot, ...
- lights: pos, rot, scale, color, intensity, ...
- renders: image_url, embedding, ...

# Tech stack

- Alembic (Database Migration)
- FastAPI (Fast, Python)
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