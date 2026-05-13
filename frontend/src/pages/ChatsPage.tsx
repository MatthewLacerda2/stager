import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  listChats,
  createChat,
  deleteChat,
  type ChatResponse,
} from '../lib/chat-api';
import {
  getScene,
  type SceneFullResponse,
} from '../lib/scene-api';

export default function ChatsPage() {
  const { sceneId } = useParams<{ sceneId: string }>();
  const navigate = useNavigate();
  
  const [scene, setScene] = useState<SceneFullResponse | null>(null);
  const [chats, setChats] = useState<ChatResponse[]>([]);
  const [newChatPrompt, setNewChatPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (sceneId) {
      fetchSceneData();
    }
  }, [sceneId]);

  const fetchSceneData = async () => {
    if (!sceneId) return;
    setLoading(true);
    setError(null);
    try {
      const sceneData = await getScene(sceneId);
      setScene(sceneData);
      
      const chatsData = await listChats(sceneId);
      setChats(chatsData);
    } catch (err: any) {
      setError(err.message || 'Failed to load scene data');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateChat = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!sceneId || !newChatPrompt.trim()) return;
    setActionLoading(true);
    setError(null);
    try {
      const newSession = await createChat({
        scene_id: sceneId,
        prompt: newChatPrompt
      });
      setNewChatPrompt('');
      // Navigate straight to the chat room
      navigate(`/scenes/${sceneId}/chats/${newSession.chat_id}`);
    } catch (err: any) {
      setError(err.message || 'Failed to initialize session');
      setActionLoading(false);
    }
  };

  const handleDeleteChat = async (chatId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!confirm('Are you sure you want to delete this chat session? This cannot be undone.')) return;
    setActionLoading(true);
    setError(null);
    try {
      await deleteChat(chatId);
      await fetchSceneData();
    } catch (err: any) {
      setError(err.message || 'Failed to delete chat session');
    } finally {
      setActionLoading(false);
    }
  };

  if (!sceneId) return null;

  return (
    <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-8">
      {loading && (
        <div className="absolute inset-0 bg-slate-950/60 backdrop-blur-sm z-50 flex flex-col items-center justify-center gap-3">
          <div className="w-12 h-12 border-4 border-purple-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-slate-400 font-medium">Loading workspace...</p>
        </div>
      )}

      {/* LEFT PANEL: SCENE SUMMARY & NEW SESSION CREATOR */}
      <div className="lg:col-span-1 space-y-6">
        
        {/* Workspace details card */}
        {scene && (
          <div className="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-6 backdrop-blur-sm">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-500 mb-1.5">Active Workspace</h4>
            <h3 className="text-lg font-bold text-slate-100">{scene.name}</h3>
            <p className="text-xs text-slate-400 leading-relaxed mt-2">{scene.brief_description || 'No description provided.'}</p>
            
            <div className="mt-5 pt-4 border-t border-slate-800/60 grid grid-cols-2 gap-3 text-xs">
              <div className="bg-slate-950/40 border border-slate-800/40 p-2.5 rounded-xl">
                <span className="block text-slate-500 text-[10px] uppercase font-bold">Total Objects</span>
                <span className="text-slate-200 font-mono font-bold text-sm">{scene.state?.objects?.length || 0}</span>
              </div>
              <div className="bg-slate-950/40 border border-slate-800/40 p-2.5 rounded-xl">
                <span className="block text-slate-500 text-[10px] uppercase font-bold">Light Sources</span>
                <span className="text-slate-200 font-mono font-bold text-sm">{scene.state?.lights?.length || 0}</span>
              </div>
            </div>
          </div>
        )}

        {/* Start new chat session */}
        <div className="bg-slate-900/50 border border-slate-800/80 rounded-2xl p-6 backdrop-blur-sm shadow-xl shadow-black/10">
          <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2 mb-4">
            <svg className="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            Start Prompting Agent
          </h2>

          {error && (
            <div className="mb-4 p-3 bg-red-950/30 border border-red-900/40 rounded-xl text-red-300 text-xs">
              {error}
            </div>
          )}

          <form onSubmit={handleCreateChat} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
                First Directive / Prompt
              </label>
              <textarea
                required
                rows={4}
                placeholder="Tell Gemini what 3D objects or layout to initialize in this empty scene... (e.g. 'Add a round oak table at the center with a modern chair next to it')"
                value={newChatPrompt}
                onChange={(e) => setNewChatPrompt(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 placeholder-slate-600 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition-all resize-none leading-relaxed"
              />
              <span className="text-[10px] text-slate-500 mt-1.5 block leading-normal">
                This triggers the Gemini AI agent loop. It will load, plan, and execute tool calls in the background to set up your design database before establishing the chat workspace.
              </span>
            </div>
            <button
              type="submit"
              disabled={actionLoading}
              className="w-full bg-linear-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-semibold text-sm rounded-xl py-3 shadow-lg shadow-purple-600/10 hover:shadow-purple-600/20 active:scale-[0.98] transition-all disabled:opacity-50"
            >
              {actionLoading ? 'Creating Session & Prompting...' : 'Initialize Chat'}
            </button>
          </form>
        </div>

      </div>

      {/* RIGHT PANEL: CHATS LIST */}
      <div className="lg:col-span-2 flex flex-col gap-4">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-xl font-bold text-slate-200 m-0">Chat Sessions</h2>
            <p className="text-sm text-slate-400">Past agent sessions associated with this scene</p>
          </div>
          <button
            onClick={() => navigate('/')}
            className="text-xs text-slate-400 hover:text-slate-200"
          >
            &larr; All Scenes
          </button>
        </div>

        {chats.length === 0 ? (
          <div className="flex-1 flex flex-col items-center justify-center p-12 bg-slate-900/20 border border-dashed border-slate-800 rounded-2xl text-center">
            <div className="p-4 bg-slate-900/60 rounded-full mb-3 text-slate-500">
              <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <h3 className="text-base font-semibold text-slate-300">No active sessions found</h3>
            <p className="text-sm text-slate-500 max-w-sm mt-1">
              Describe what 3D layouts or components you want to add to this viewport scene in the prompt builder on the left!
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {chats.map((chat) => (
              <div
                key={chat.id}
                onClick={() => navigate(`/scenes/${sceneId}/chats/${chat.id}`)}
                className="group bg-slate-900/40 hover:bg-slate-900/80 border border-slate-800 hover:border-purple-500/50 rounded-xl p-4 cursor-pointer flex items-center justify-between gap-4 shadow-md transition-all duration-250"
              >
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-purple-500/10 border border-purple-500/30 rounded-lg text-purple-400">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                    </svg>
                  </div>
                  <div>
                    <h4 className="text-sm font-bold text-slate-200 group-hover:text-purple-400 transition-colors">
                      Session <code className="text-xs bg-slate-950 border border-slate-800 text-slate-400 px-1 py-0.5">{chat.id.substring(0, 8)}...</code>
                    </h4>
                    <p className="text-xs text-slate-500 mt-0.5">
                      Started on {new Date(chat.created_at).toLocaleString()}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={(e) => handleDeleteChat(chat.id, e)}
                    className="opacity-0 group-hover:opacity-100 p-1.5 hover:bg-red-950/50 border border-transparent hover:border-red-900/50 text-slate-500 hover:text-red-400 rounded-lg transition-all"
                    title="Delete session"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                  <span className="text-slate-500 group-hover:text-purple-400 group-hover:translate-x-1 transition-all text-sm font-medium">
                    Resume &rarr;
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
