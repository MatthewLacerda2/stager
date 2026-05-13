const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

// --- TypeScript Interfaces ---

export interface BlenderObjectCreate {
  name: string;
  description?: string | null;
}

export interface BlenderObjectResponse {
  id: string;
  name: string;
  description?: string | null;
  asset_path?: string | null;
}

export interface BlenderObjectListResponse extends BlenderObjectResponse {
  is_used: boolean;
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
 * List all available library assets, indicating if they are currently placed in any scene.
 */
export async function listObjects(): Promise<BlenderObjectListResponse[]> {
  const response = await fetch(`${API_BASE_URL}/objects/`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
    },
  });
  return handleResponse<BlenderObjectListResponse[]>(response);
}

/**
 * Upload a 3D object to be indexed in the database.
 * @param file The File object (e.g., .blend, .gltf, etc.) to upload.
 */
export async function uploadObject(file: File): Promise<BlenderObjectResponse> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/objects/upload`, {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      // Note: 'Content-Type' header must NOT be manually set for FormData to allow the browser to auto-set boundary
    },
    body: formData,
  });
  return handleResponse<BlenderObjectResponse>(response);
}

/**
 * Delete a specific library object.
 */
export async function deleteObject(objectId: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/objects/${objectId}`, {
    method: 'DELETE',
  });
  return handleResponse<void>(response);
}
