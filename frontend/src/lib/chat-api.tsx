import type { SceneState } from './scene-api';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

// --- TypeScript Interfaces ---

export interface ChatCreate {
  scene_id: string;
  prompt: string;
}

export interface ChatResume {
  prompt: string;
}

export interface ChatResponse {
  id: string;
  scene_id: string;
  created_at: string;
}

export interface ChatTurnResponse {
  id: string;
  chat_id: string;
  user_prompt: string;
  agent_response?: string | null;
  created_at: string;
}

export interface ChatInteractionResponse {
  chat_id: string;
  turn_id: string;
  agent_response?: string | null;
  scene_state: SceneState;
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
 * Start a new chat for a scene and process the first prompt.
 */
export async function createChat(data: ChatCreate): Promise<ChatInteractionResponse> {
  const response = await fetch(`${API_BASE_URL}/chats/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  return handleResponse<ChatInteractionResponse>(response);
}

/**
 * List all past chats belonging to a specific scene.
 */
export async function listChats(sceneId: string): Promise<ChatResponse[]> {
  const response = await fetch(`${API_BASE_URL}/chats/scene/${sceneId}`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
    },
  });
  return handleResponse<ChatResponse[]>(response);
}

/**
 * Send a new prompt to an existing chat and process it.
 */
export async function resumeChat(chatId: string, data: ChatResume): Promise<ChatInteractionResponse> {
  const response = await fetch(`${API_BASE_URL}/chats/${chatId}/resume`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  return handleResponse<ChatInteractionResponse>(response);
}

/**
 * Retrieve the conversation history (turns) for an existing chat.
 */
export async function getChatHistory(chatId: string): Promise<ChatTurnResponse[]> {
  const response = await fetch(`${API_BASE_URL}/chats/${chatId}/history`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
    },
  });
  return handleResponse<ChatTurnResponse[]>(response);
}

/**
 * Delete a chat and its history.
 */
export async function deleteChat(chatId: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/chats/${chatId}`, {
    method: 'DELETE',
  });
  return handleResponse<void>(response);
}
