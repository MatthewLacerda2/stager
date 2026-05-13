const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

// --- TypeScript Interfaces ---

export interface RenderCreate {
  scene_id: string;
  camera_id: string;
  is_sketch?: boolean;
}

export interface RenderResponse {
  id: string;
  scene_id: string;
  camera_id: string;
  is_sketch: boolean;
  image_url?: string | null;
  description?: string | null;
  created_at: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  offset: number;
  limit: number;
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
 * Request a new render (sketch or high-fidelity) for a camera.
 */
export async function createRender(data: RenderCreate): Promise<RenderResponse> {
  const response = await fetch(`${API_BASE_URL}/renders/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  return handleResponse<RenderResponse>(response);
}

/**
 * Get all renders sorted by most recent, paginated.
 */
export async function listRenders(offset = 0, limit = 10): Promise<PaginatedResponse<RenderResponse>> {
  const params = new URLSearchParams({
    offset: offset.toString(),
    limit: limit.toString(),
  });

  const response = await fetch(`${API_BASE_URL}/renders/?${params.toString()}`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
    },
  });
  return handleResponse<PaginatedResponse<RenderResponse>>(response);
}

/**
 * Get details of a specific render.
 */
export async function getRenderDetails(renderId: string): Promise<RenderResponse> {
  const response = await fetch(`${API_BASE_URL}/renders/${renderId}`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
    },
  });
  return handleResponse<RenderResponse>(response);
}

/**
 * Get the direct download URL for a render image file.
 */
export function getRenderFileUrl(renderId: string): string {
  return `${API_BASE_URL}/renders/${renderId}/file`;
}

/**
 * Delete a specific render.
 */
export async function deleteRender(renderId: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/renders/${renderId}`, {
    method: 'DELETE',
  });
  return handleResponse<void>(response);
}