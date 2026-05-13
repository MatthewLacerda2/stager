import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  getRenderFileUrl,
  listRenders,
  type RenderResponse,
} from '../lib/renders-api';

export default function RendersPage() {
  const navigate = useNavigate();
  const [renders, setRenders] = useState<RenderResponse[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchRenders();
  }, []);

  const fetchRenders = async () => {
    setLoading(true);
    try {
      const data = await listRenders(0, 30);
      setRenders(data.items);
    } catch (err) {
      console.error('Failed to fetch renders', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-1 flex flex-col gap-6">
      {loading && (
        <div className="absolute inset-0 bg-slate-950/60 backdrop-blur-sm z-50 flex flex-col items-center justify-center gap-3">
          <div className="w-12 h-12 border-4 border-purple-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-slate-400 font-medium">Loading gallery...</p>
        </div>
      )}

      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h2 className="text-xl font-bold text-slate-100 m-0">🎬 Captured Renders Gallery</h2>
          <p className="text-sm text-slate-400 font-medium">Click on any render thumbnail below to download the original high-resolution PNG file.</p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={fetchRenders}
            className="px-3 py-1.5 bg-slate-900 border border-slate-800 rounded-xl hover:bg-slate-800 text-slate-300 text-xs transition-all"
          >
            Refresh Gallery
          </button>
          <button
            onClick={() => navigate(-1)}
            className="px-3 py-1.5 bg-purple-600 hover:bg-purple-500 text-white font-semibold text-xs rounded-xl shadow-lg shadow-purple-600/15 transition-all"
          >
            &larr; Back
          </button>
        </div>
      </div>

      {renders.length === 0 ? (
        <div className="flex-1 flex flex-col items-center justify-center p-12 bg-slate-900/20 border border-dashed border-slate-800 rounded-2xl text-center">
          <div className="p-4 bg-slate-900/60 rounded-full mb-3 text-slate-500">
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
            </svg>
          </div>
          <h3 className="text-base font-semibold text-slate-300">No renders found</h3>
          <p className="text-sm text-slate-500 max-w-sm mt-1">
            You haven't requested any rendering jobs for this workspace yet. Switch to "Studio Rendering" in the chat room to capture one!
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {renders.map((render) => (
            <div
              key={render.id}
              onClick={() => {
                const downloadUrl = getRenderFileUrl(render.id);
                const link = document.createElement('a');
                link.href = downloadUrl;
                link.setAttribute('download', `render_${render.id}.png`);
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
              }}
              className="group bg-slate-900/40 hover:bg-slate-900/80 border border-slate-800 hover:border-purple-500/50 rounded-2xl p-4 cursor-pointer shadow-lg hover:shadow-xl hover:shadow-purple-500/5 hover:-translate-y-1 transition-all duration-300"
              title="Click to download image"
            >
              <div className="relative aspect-video rounded-xl bg-slate-950 border border-slate-800 overflow-hidden">
                {render.image_url ? (
                  <img
                    src={getRenderFileUrl(render.id)}
                    alt="Render Thumbnail"
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  />
                ) : (
                  <div className="absolute inset-0 flex items-center justify-center text-slate-600 text-xs font-mono">
                    Generating...
                  </div>
                )}

                {/* Hover Overlay */}
                <div className="absolute inset-0 bg-slate-950/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                  <div className="p-3 bg-purple-600 text-white rounded-full shadow-lg transform translate-y-2 group-hover:translate-y-0 transition-transform">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                  </div>
                </div>
              </div>

              <div className="mt-3">
                <div className="flex justify-between items-start">
                  <span className="font-bold text-xs text-slate-300 block truncate max-w-[150px]">
                    Render: {render.id.substring(0, 8)}
                  </span>
                  <span className="text-[9px] uppercase tracking-wider bg-purple-500/10 border border-purple-500/20 text-purple-300 px-1.5 py-0.5 rounded">
                    {render.is_sketch ? 'Sketch' : 'Hi-Fi'}
                  </span>
                </div>
                <p className="text-[10px] text-slate-500 mt-1 font-medium">
                  Captured {new Date(render.created_at).toLocaleString()}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
