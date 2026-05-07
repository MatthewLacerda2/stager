# stager
Create and visualize 3D scenarios with plain English text prompts. No artistic skill required.

It's similar to lovable.dev in the sense it's not meant for production-grade art, nor does it replace professional artists. It gets you good stuff fast.

# Architecture

the frontend sends the request to our api
the api creates an agentic loop:
	It sends a request to Ollama wit tools at it's disposal
	If Gemini replies with a tool call, the tool may read/update the db or call Blender via Linux commands;
	the tools may move or instantiate objects, lights, materials, and update the db so the app knows the scenary;
	the tools are meant to remove as much cognitive load from the AI as possible and use the least and easier steps to apply the operation the user wants;
	the response is sent to the user so they get the updated version of the scene and/or the renders

the app does NOT create objects, AI is not good enough for that yet. we pick from a pool and place them, much like 3D artists do in sketchfab. the app does create materials procedurally

# Tech stack

- Alembic (Database Migration)
- FastAPI (Fast, Python)
  - SQLAlchemy (ORM)
  - Ollama
- PostgreSQL
- React + Vite + TS
  - React Three Fiber
  - Three.js
  - GLTF
- Blender CLI in Linux

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