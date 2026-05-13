import { Link, Outlet, useParams, useLocation } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { getScene } from '../lib/scene-api';

export default function Layout() {
  const { sceneId, chatId } = useParams<{ sceneId: string; chatId: string }>();
  const location = useLocation();
  const [sceneName, setSceneName] = useState<string>('');

  useEffect(() => {
    if (sceneId) {
      getScene(sceneId)
        .then((scene) => setSceneName(scene.name || ''))
        .catch((err) => console.error('Failed to load scene name in breadcrumbs', err));
    } else {
      setSceneName('');
    }
  }, [sceneId]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-purple-500/30 selection:text-purple-200">
      {/* HEADER / NAVIGATION */}
      <header className="sticky top-0 z-30 bg-slate-900/80 backdrop-blur-md border-b border-slate-800 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-linear-to-br from-purple-500 to-indigo-600 rounded-xl shadow-lg shadow-purple-500/20">
            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
          </div>
          <div>
            <Link to="/" className="hover:opacity-90 transition-opacity">
              <h1 className="text-xl font-bold tracking-tight bg-linear-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent m-0">
                Stager AI Studio
              </h1>
              <p className="text-xs text-slate-500">FastAPI & Blender 3D Prototype</p>
            </Link>
          </div>
        </div>

        {/* BREADCRUMB ROUTER */}
        <nav className="flex items-center gap-2 text-sm text-slate-400">
          <Link
            to="/"
            className={`hover:text-purple-400 transition-colors font-medium ${location.pathname === '/' ? 'text-purple-400' : ''}`}
          >
            Scenes
          </Link>

          {sceneId && (
            <>
              <span className="text-slate-600">/</span>
              <Link
                to={`/scenes/${sceneId}/chats`}
                className={`hover:text-purple-400 transition-colors max-w-[120px] truncate font-medium ${location.pathname.endsWith('/chats') ? 'text-purple-400' : ''}`}
                title={sceneName || 'Unnamed Scene'}
              >
                {sceneName || 'Scene'}
              </Link>
            </>
          )}

          {chatId && (
            <>
              <span className="text-slate-600">/</span>
              <Link
                to={`/scenes/${sceneId}/chats/${chatId}`}
                className={`hover:text-purple-400 transition-colors truncate max-w-[120px] font-medium ${location.pathname.includes('/chats/') && !location.pathname.endsWith('/renders') ? 'text-purple-400' : ''}`}
              >
                Chat session
              </Link>
            </>
          )}

          {location.pathname.endsWith('/renders') && (
            <>
              <span className="text-slate-600">/</span>
              <span className="text-purple-400 font-medium truncate max-w-[120px]">
                Renders Gallery
              </span>
            </>
          )}
        </nav>
      </header>

      {/* MAIN CONTAINER */}
      <main className="flex-1 p-6 flex flex-col relative">
        <Outlet />
      </main>

      {/* FOOTER */}
      <footer className="mt-auto border-t border-slate-800/60 bg-slate-950/40 px-6 py-4 flex items-center justify-between text-xs text-slate-500">
        <p>&copy; {new Date().getFullYear()} Stager AI Workspace. All rights reserved.</p>
        <div className="flex items-center gap-4">
          <span className="flex items-center gap-1.5 text-slate-400">
            <span className="w-2 h-2 bg-green-500 rounded-full"></span>
            Database Synced
          </span>
          <span className="text-slate-600">|</span>
          <span className="flex items-center gap-1.5 text-slate-400">
            <span className="w-2 h-2 bg-purple-500 rounded-full animate-pulse"></span>
            Blender Connected
          </span>
        </div>
      </footer>
    </div>
  );
}
