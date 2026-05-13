const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

// --- TypeScript Interfaces ---

export interface Vector3D {
  x: number;
  y: number;
  z: number;
}

export interface Transform3D {
  pos: Vector3D;
  rot: Vector3D;
  scale: Vector3D;
}

export interface SceneObjectState {
  id: string;
  name: string; // The referenced BlenderObject name
  blender_object_id: string;
  group_object_id?: string | null;
  transform: Transform3D;
}

export interface LightState {
  id: string;
  type: 'POINT' | 'SUN' | 'SPOT' | 'AREA';
  transform: Transform3D;
  color: string;
  intensity: number;
}

export interface GroupObjectState {
  id: string;
  name: string;
  transform: Transform3D;
}

export interface SceneState {
  objects: SceneObjectState[];
  lights: LightState[];
  groups: GroupObjectState[];
}

export interface SceneCreate {
  name?: string;
  brief_description?: string;
}

export interface SceneResponse {
  id: string;
  name?: string;
  brief_description?: string;
  created_at: string;
  updated_at: string;
}

export interface SceneFullResponse extends SceneResponse {
  state: SceneState;
}

// --- Helper for handling fetch responses ---

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const errorText = await response.text().catch(() => 'Unknown error');
    throw new Error(`API Error (${response.status}): ${errorText}`);
  }
  
  if (response.status === 204) {
    return null as T;
  }
  
  return response.json() as Promise<T>;
}

// --- API Functions ---

/**
 * List all available 3D scenes.
 */
export async function listScenes(): Promise<SceneResponse[]> {
  const response = await fetch(`${API_BASE_URL}/scenes/`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
    },
  });
  return handleResponse<SceneResponse[]>(response);
}

/**
 * Create a new 3D scene.
 */
export async function createScene(data: SceneCreate): Promise<SceneResponse> {
  const response = await fetch(`${API_BASE_URL}/scenes/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  return handleResponse<SceneResponse>(response);
}

/**
 * Fetch a scene's metadata along with its complete 3D viewport state (objects, lights, groups).
 */
export async function getScene(sceneId: string): Promise<SceneFullResponse> {
  const response = await fetch(`${API_BASE_URL}/scenes/${sceneId}`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
    },
  });
  return handleResponse<SceneFullResponse>(response);
}

/**
 * Delete a scene and all its contents.
 */
export async function deleteScene(sceneId: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/scenes/${sceneId}`, {
    method: 'DELETE',
  });
  return handleResponse<void>(response);
}
