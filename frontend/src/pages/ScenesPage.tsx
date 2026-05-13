import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  listScenes,
  createScene,
  deleteScene,
  type SceneResponse,
} from '../lib/scene-api';

export default function ScenesPage() {
  const navigate = useNavigate();
  const [scenes, setScenes] = useState<SceneResponse[]>([]);
  const [newSceneName, setNewSceneName] = useState('');
  const [newSceneDesc, setNewSceneDesc] = useState('');
  const [loading, setLoading] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchScenes();
  }, []);

  const fetchScenes = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await listScenes();
      setScenes(data);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch scenes');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateScene = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newSceneName.trim()) return;
    setActionLoading(true);
    setError(null);
    try {
      await createScene({
        name: newSceneName,
        brief_description: newSceneDesc
      });
      setNewSceneName('');
      setNewSceneDesc('');
      await fetchScenes();
    } catch (err: any) {
      setError(err.message || 'Failed to create scene');
    } finally {
      setActionLoading(false);
    }
  };

  const handleDeleteScene = async (sceneId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!confirm('Are you sure you want to delete this scene and all its associated chats?')) return;
    setActionLoading(true);
    setError(null);
    try {
      await deleteScene(sceneId);
      await fetchScenes();
    } catch (err: any) {
      setError(err.message || 'Failed to delete scene');
    } finally {
      setActionLoading(false);
    }
  };

  return (
    <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-8">
      {loading && (
        <div className="absolute inset-0 bg-slate-950/60 backdrop-blur-sm z-50 flex flex-col items-center justify-center gap-3">
          <div className="w-12 h-12 border-4 border-purple-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-slate-400 font-medium">Synchronizing studio...</p>
        </div>
      )}

      {/* SCENE CREATION CARD */}
      <div className="lg:col-span-1 bg-slate-900/50 border border-slate-800/80 rounded-2xl p-6 h-fit backdrop-blur-sm shadow-xl shadow-black/10">
        <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2 mb-4">
          <svg className="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
          </svg>
          Create New Scene
        </h2>
        
        {error && (
          <div className="mb-4 p-3 bg-red-950/30 border border-red-900/40 rounded-xl text-red-300 text-xs">
            {error}
          </div>
        )}

        <form onSubmit={handleCreateScene} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
              Scene Name
            </label>
            <input
              type="text"
              required
              placeholder="e.g., Cozy Living Room Layout"
              value={newSceneName}
              onChange={(e) => setNewSceneName(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition-all"
            />
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
              Brief Description
            </label>
            <textarea
              rows={4}
              placeholder="Describe the overall theme or purpose..."
              value={newSceneDesc}
              onChange={(e) => setNewSceneDesc(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition-all resize-none"
            />
          </div>
          <button
            type="submit"
            disabled={actionLoading}
            className="w-full bg-linear-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-semibold text-sm rounded-xl py-3 shadow-lg shadow-purple-600/10 hover:shadow-purple-600/20 active:scale-[0.98] transition-all disabled:opacity-50 disabled:scale-100"
          >
            {actionLoading ? 'Initializing Scene...' : 'Create Empty Scene'}
          </button>
        </form>
      </div>

      {/* MAIN: SCENES LIST */}
      <div className="lg:col-span-2 flex flex-col gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-200 m-0">Studio Workspace Directory</h2>
          <p className="text-sm text-slate-400">Select an existing 3D viewport canvas or initialize a new scene on the left</p>
        </div>

        {scenes.length === 0 ? (
          <div className="flex-1 flex flex-col items-center justify-center p-12 bg-slate-900/20 border border-dashed border-slate-800 rounded-2xl text-center">
            <div className="p-4 bg-slate-900/60 rounded-full mb-3 text-slate-500">
              <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
            </div>
            <h3 className="text-base font-semibold text-slate-300">No active scenes found</h3>
            <p className="text-sm text-slate-500 max-w-sm mt-1">
              Start by creating a new scene using the controller on the left side of the dashboard.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {scenes.map((scene) => (
              <div
                key={scene.id}
                onClick={() => navigate(`/scenes/${scene.id}/chats`)}
                className="group bg-slate-900/40 hover:bg-slate-900/80 border border-slate-800 hover:border-purple-500/50 rounded-2xl p-5 cursor-pointer shadow-md hover:shadow-xl hover:shadow-purple-500/5 hover:-translate-y-0.5 transition-all duration-300 flex flex-col justify-between min-h-[160px]"
              >
                <div>
                  <div className="flex justify-between items-start">
                    <h3 className="text-base font-bold text-slate-200 group-hover:text-purple-400 transition-colors m-0 max-w-[80%] truncate">
                      {scene.name}
                    </h3>
                    <button
                      onClick={(e) => handleDeleteScene(scene.id, e)}
                      className="p-1.5 bg-slate-950 hover:bg-red-950/50 text-slate-500 hover:text-red-400 border border-slate-800 hover:border-red-900/50 rounded-lg opacity-0 group-hover:opacity-100 transition-all"
                      title="Delete Scene"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                  <p className="text-xs text-slate-400 mt-2 line-clamp-2 leading-relaxed">
                    {scene.brief_description || 'No description provided.'}
                  </p>
                </div>

                <div className="mt-4 pt-3 border-t border-slate-800/60 flex items-center justify-between text-[11px] text-slate-500">
                  <span className="font-mono text-slate-600">ID: {scene.id.substring(0, 8)}...</span>
                  <span className="font-medium group-hover:text-purple-400 transition-colors">
                    Open Canvas &rarr;
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
