import { useEffect, useRef, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  getChatHistory,
  resumeChat,
} from '../lib/chat-api';
import {
  createRender,
  listRenders,
  getRenderFileUrl,
  type RenderResponse,
} from '../lib/renders-api';
import {
  getScene,
  type SceneFullResponse,
} from '../lib/scene-api';

interface Message {
  id: string;
  role: 'user' | 'model' | 'system';
  text: string;
  created_at?: string;
}

export default function ChatRoomPage() {
  const { sceneId, chatId } = useParams<{ sceneId: string; chatId: string }>();
  const navigate = useNavigate();

  const [selectedScene, setSelectedScene] = useState<SceneFullResponse | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [renders, setRenders] = useState<RenderResponse[]>([]);
  const [chatInput, setChatInput] = useState('');
  const [renderIsSketch, setRenderIsSketch] = useState(true);
  const [customCameraId, setCustomCameraId] = useState('');

  const [loading, setLoading] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);
  const [chatLoading, setChatLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'inspector' | 'renders'>('inspector');

  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (chatId && sceneId) {
      fetchInitialData();
    }
  }, [chatId, sceneId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, chatLoading]);

  const fetchInitialData = async () => {
    if (!chatId || !sceneId) return;
    setLoading(true);
    setError(null);
    try {
      // Load scene objects tree
      const sceneData = await getScene(sceneId);
      setSelectedScene(sceneData);

      // Load chat logs history
      const history = await getChatHistory(chatId);
      const formatted: Message[] = history.map((turn) => [
        { id: `${turn.id}-u`, role: 'user' as const, text: turn.user_prompt, created_at: turn.created_at },
        { id: `${turn.id}-m`, role: 'model' as const, text: turn.agent_response || '', created_at: turn.created_at }
      ]).flat();
      setMessages(formatted);

      // Load previous renders
      const rendersData = await listRenders(0, 15);
      setRenders(rendersData.items);
    } catch (err: any) {
      setError(err.message || 'Failed to sync workspace');
    } finally {
      setLoading(false);
    }
  };

  const fetchRenders = async () => {
    try {
      const data = await listRenders(0, 15);
      setRenders(data.items);
    } catch (err) {
      console.error('Failed to fetch renders', err);
    }
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!chatId || !chatInput.trim() || chatLoading) return;

    const userPrompt = chatInput;
    setChatInput('');
    setError(null);

    // Append user message immediately
    const userMsgId = Math.random().toString();
    setMessages((prev) => [...prev, { id: userMsgId, role: 'user', text: userPrompt }]);
    setChatLoading(true);

    try {
      const response = await resumeChat(chatId, { prompt: userPrompt });

      // Append model response
      setMessages((prev) => [
        ...prev,
        { id: response.turn_id, role: 'model', text: response.agent_response || '' }
      ]);

      // Sync active viewport scene states to update the Live State Inspector tree!
      if (sceneId) {
        const updatedScene = await getScene(sceneId);
        setSelectedScene(updatedScene);
      }
    } catch (err: any) {
      setError(err.message || 'Agent error');
      // Append fallback system logs
      setMessages((prev) => [
        ...prev,
        { id: Math.random().toString(), role: 'system', text: `ERROR: ${err.message || 'The Gemini agent failed to respond.'}` }
      ]);
    } finally {
      setChatLoading(false);
    }
  };

  const handleTriggerRender = async () => {
    if (!selectedScene) return;

    let camId = customCameraId.trim();
    if (!camId) {
      camId = '00000000-0000-0000-0000-000000000000';
    }

    setActionLoading(true);
    setError(null);
    try {
      await createRender({
        scene_id: selectedScene.id,
        camera_id: camId,
        is_sketch: renderIsSketch
      });
      alert('Render task completed successfully!');
      fetchRenders();
    } catch (err: any) {
      setError(err.message || 'Render pipeline failed.');
    } finally {
      setActionLoading(false);
    }
  };

  if (!chatId || !sceneId) return null;

  return (
    <div className="flex-1 flex flex-col lg:flex-row gap-6 min-h-[550px]">
      {loading && (
        <div className="absolute inset-0 bg-slate-950/60 backdrop-blur-sm z-50 flex flex-col items-center justify-center gap-3">
          <div className="w-12 h-12 border-4 border-purple-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-slate-400 font-medium">Synchronizing workspace...</p>
        </div>
      )}

      {/* LEFT: CONVERSATIONAL CHATBOT (60%) */}
      <div className="flex-1 lg:w-3/5 bg-slate-900/30 border border-slate-800 rounded-2xl flex flex-col h-[75vh]">
        
        {/* Chat info header */}
        <div className="p-4 border-b border-slate-800/80 bg-slate-900/40 rounded-t-2xl flex justify-between items-center">
          <div className="flex items-center gap-2">
            <div className="w-2.5 h-2.5 bg-green-500 rounded-full animate-ping"></div>
            <h3 className="text-sm font-bold text-slate-200">Gemini Agent Session</h3>
          </div>
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate(`/scenes/${sceneId}/renders`)}
              className="flex items-center gap-1.5 text-xs bg-purple-600/20 border border-purple-500/30 hover:bg-purple-600/30 hover:border-purple-500/50 text-purple-300 font-semibold px-3 py-1.5 rounded-xl transition-all"
            >
              <svg className="w-4 h-4 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16l4.586-4.586a2 2 0 012-2L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              View Renders Gallery
            </button>
            <span className="text-xs text-slate-500">
              Chat ID: <code className="bg-slate-950 border border-slate-800 px-1 py-0.5">{chatId.substring(0, 8)}</code>
            </span>
          </div>
        </div>

        {/* Message thread container */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {error && (
            <div className="p-3 bg-red-950/30 border border-red-900/40 rounded-xl text-red-300 text-xs">
              {error}
            </div>
          )}

          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[85%] rounded-2xl p-4 text-sm leading-relaxed ${
                  msg.role === 'user'
                    ? 'bg-linear-to-br from-purple-600 to-indigo-600 text-white rounded-br-none shadow-md shadow-purple-900/10'
                    : msg.role === 'system'
                      ? 'bg-red-950/20 border border-red-900/50 text-red-300 rounded-bl-none font-mono text-xs'
                      : 'bg-slate-900/90 border border-slate-800 text-slate-200 rounded-bl-none shadow-md'
                }`}
              >
                {/* Speaker title */}
                <span className="block text-[10px] font-bold uppercase tracking-wider mb-1 opacity-60">
                  {msg.role === 'user' ? 'You' : msg.role === 'system' ? 'System' : 'Gemini Agent'}
                </span>
                {msg.text}
              </div>
            </div>
          ))}

          {/* AI Loading bubble */}
          {chatLoading && (
            <div className="flex justify-start">
              <div className="bg-slate-900 border border-slate-800 rounded-2xl rounded-bl-none p-4 max-w-[80%] flex items-center gap-3">
                <div className="flex gap-1.5">
                  <span className="w-2 h-2 bg-purple-500 rounded-full animate-bounce [animation-delay:-0.3s]"></span>
                  <span className="w-2 h-2 bg-purple-500 rounded-full animate-bounce [animation-delay:-0.15s]"></span>
                  <span className="w-2 h-2 bg-purple-500 rounded-full animate-bounce"></span>
                </div>
                <span className="text-xs text-slate-500 font-medium">Agent is parsing and running tools...</span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Prompt Input Form */}
        <form onSubmit={handleSendMessage} className="p-4 border-t border-slate-800 bg-slate-900/40 rounded-b-2xl">
          <div className="flex gap-2">
            <input
              type="text"
              required
              disabled={chatLoading}
              placeholder="Ask Gemini to add, modify, delete or group 3D objects/lights..."
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              className="flex-1 bg-slate-950 border border-slate-800 focus:border-purple-500 rounded-xl px-4 py-3 text-sm placeholder-slate-600 focus:outline-none transition-all"
            />
            <button
              type="submit"
              disabled={chatLoading || !chatInput.trim()}
              className="bg-purple-600 hover:bg-purple-500 disabled:opacity-40 text-white font-bold text-sm px-5 py-3 rounded-xl transition-all shadow-lg shadow-purple-600/10 active:scale-95"
            >
              Send
            </button>
          </div>
        </form>
      </div>

      {/* RIGHT: VIEWPORT STATE INSPECTOR / RENDERS PANEL (40%) */}
      <div className="flex-1 lg:w-2/5 bg-slate-900/30 border border-slate-800 rounded-2xl flex flex-col h-[75vh]">
        
        {/* Navigation Tabs */}
        <div className="flex border-b border-slate-800 bg-slate-900/40 rounded-t-2xl overflow-hidden">
          <button
            onClick={() => setActiveTab('inspector')}
            className={`flex-1 py-3 text-sm font-semibold border-b-2 transition-all ${
              activeTab === 'inspector'
                ? 'border-purple-500 text-purple-400 bg-purple-500/5'
                : 'border-transparent text-slate-400 hover:text-slate-200 hover:bg-slate-800/20'
            }`}
          >
            Scene Inspector
          </button>
          <button
            onClick={() => { setActiveTab('renders'); fetchRenders(); }}
            className={`flex-1 py-3 text-sm font-semibold border-b-2 transition-all ${
              activeTab === 'renders'
                ? 'border-purple-500 text-purple-400 bg-purple-500/5'
                : 'border-transparent text-slate-400 hover:text-slate-200 hover:bg-slate-800/20'
            }`}
          >
            Studio Rendering
          </button>
        </div>

        {/* Tab 1: Live State Inspector View */}
        {activeTab === 'inspector' && (
          <div className="flex-1 overflow-y-auto p-4 space-y-5">
            <div>
              <h3 className="text-sm font-bold text-slate-200 m-0">Synchronized Viewport State</h3>
              <p className="text-[11px] text-slate-500 leading-normal mt-0.5">Real-time DB synchronization representing the active Blender structure.</p>
            </div>

            {/* Objects Hierarchy List */}
            <div className="space-y-4">
              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 border-b border-slate-800/60 pb-1.5 mb-2 flex justify-between items-center">
                  <span>3D Object Assets ({selectedScene?.state?.objects?.length || 0})</span>
                  <span className="text-[10px] bg-slate-950 px-1.5 py-0.5 rounded text-purple-400 border border-slate-800 font-mono">MESH</span>
                </h4>

                {!selectedScene?.state?.objects || selectedScene.state.objects.length === 0 ? (
                  <p className="text-xs text-slate-600 italic">No meshes registered in scene.</p>
                ) : (
                  <div className="space-y-2">
                    {selectedScene.state.objects.map((so) => (
                      <div key={so.id} className="bg-slate-950/40 border border-slate-800 p-3 rounded-xl hover:border-purple-500/30 transition-all">
                        <div className="flex justify-between items-start">
                          <span className="font-bold text-xs text-slate-200">{so.name || 'Unnamed Object'}</span>
                        </div>
                        {/* 3D Coordinates */}
                        <div className="mt-2.5 grid grid-cols-3 gap-1.5 text-[10px] font-mono">
                          <div className="bg-slate-950/60 border border-slate-800/40 p-1.5 rounded">
                            <span className="text-slate-500 font-bold block mb-0.5">POSITION</span>
                            <span className="text-slate-300">[{so.transform.pos.x?.toFixed(1)}, {so.transform.pos.y?.toFixed(1)}, {so.transform.pos.z?.toFixed(1)}]</span>
                          </div>
                          <div className="bg-slate-950/60 border border-slate-800/40 p-1.5 rounded">
                            <span className="text-slate-500 font-bold block mb-0.5">ROTATION</span>
                            <span className="text-slate-300">[{so.transform.rot.x?.toFixed(0)}°, {so.transform.rot.y?.toFixed(0)}°, {so.transform.rot.z?.toFixed(0)}°]</span>
                          </div>
                          <div className="bg-slate-950/60 border border-slate-800/40 p-1.5 rounded">
                            <span className="text-slate-500 font-bold block mb-0.5">SCALE</span>
                            <span className="text-slate-300">[{so.transform.scale.x?.toFixed(1)}, {so.transform.scale.y?.toFixed(1)}, {so.transform.scale.z?.toFixed(1)}]</span>
                          </div>
                        </div>
                        {so.group_object_id && (
                          <div className="mt-2 text-[10px] text-purple-400 font-mono">
                            ↳ Linked to Group Parent: <code className="bg-slate-950 border border-slate-800 px-1 py-0.5 text-[9px] rounded">{so.group_object_id.substring(0, 8)}...</code>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Lighting State Tree */}
              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 border-b border-slate-800/60 pb-1.5 mb-2 flex justify-between items-center">
                  <span>Light Sources ({selectedScene?.state?.lights?.length || 0})</span>
                  <span className="text-[10px] bg-slate-950 px-1.5 py-0.5 rounded text-amber-400 border border-slate-800 font-mono">LIGHT</span>
                </h4>

                {!selectedScene?.state?.lights || selectedScene.state.lights.length === 0 ? (
                  <p className="text-xs text-slate-600 italic">No viewport illuminations registered.</p>
                ) : (
                  <div className="space-y-2">
                    {selectedScene.state.lights.map((light) => (
                      <div key={light.id} className="bg-slate-950/40 border border-slate-800 p-3 rounded-xl hover:border-amber-500/30 transition-all">
                        <div className="flex justify-between items-start">
                          <div className="flex items-center gap-2">
                            <span className="w-2.5 h-2.5 rounded-full border border-slate-800/80" style={{ backgroundColor: light.color || '#fff' }}></span>
                            <span className="font-bold text-xs text-slate-200">Light Source</span>
                          </div>
                          <span className="text-[9px] uppercase tracking-wider bg-amber-500/10 border border-amber-500/20 text-amber-300 px-1.5 py-0.5 rounded font-bold">
                            {light.type || 'Point'}
                          </span>
                        </div>
                        <div className="mt-2.5 grid grid-cols-2 gap-2 text-[10px] font-mono">
                          <div className="bg-slate-950/60 border border-slate-800/40 p-1.5 rounded">
                            <span className="text-slate-500 font-bold block mb-0.5">COORDINATES (XYZ)</span>
                            <span className="text-slate-300">[{light.transform.pos.x?.toFixed(1)}, {light.transform.pos.y?.toFixed(1)}, {light.transform.pos.z?.toFixed(1)}]</span>
                          </div>
                          <div className="bg-slate-950/60 border border-slate-800/40 p-1.5 rounded">
                            <span className="text-slate-500 font-bold block mb-0.5">INTENSITY (WATTS)</span>
                            <span className="text-amber-300 font-bold">{light.intensity?.toFixed(0)} W</span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Logical Groupings */}
              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 border-b border-slate-800/60 pb-1.5 mb-2 flex justify-between items-center">
                  <span>Parent Group Aggregations ({selectedScene?.state?.groups?.length || 0})</span>
                  <span className="text-[10px] bg-slate-950 px-1.5 py-0.5 rounded text-blue-400 border border-slate-800 font-mono">GROUP</span>
                </h4>

                {!selectedScene?.state?.groups || selectedScene.state.groups.length === 0 ? (
                  <p className="text-xs text-slate-600 italic">No parent groupings declared in scene structure.</p>
                ) : (
                  <div className="space-y-1.5">
                    {selectedScene.state.groups.map((group) => (
                      <div key={group.id} className="bg-slate-950/40 border border-slate-800 px-3 py-2.5 rounded-xl hover:border-blue-500/30 transition-all">
                        <span className="font-bold text-xs text-slate-300">{group.name || 'Asset Group'}</span>
                        <span className="text-[10px] text-slate-500 mt-0.5 block">Group UUID: {group.id}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Tab 2: Studio Rendering & Cameras */}
        {activeTab === 'renders' && (
          <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-5">
            
            {/* Trigger Render Card */}
            <div className="bg-slate-950/50 border border-slate-800 rounded-xl p-4 space-y-3">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 m-0">Trigger Render Job</h4>

              <div className="grid grid-cols-2 gap-3 text-xs">
                <div>
                  <label className="block text-[10px] text-slate-500 uppercase tracking-wide font-semibold mb-1">Render Style</label>
                  <div className="flex bg-slate-950 border border-slate-800 rounded-lg p-0.5">
                    <button
                      type="button"
                      onClick={() => setRenderIsSketch(true)}
                      className={`flex-1 py-1 px-2 rounded-md font-medium text-center transition-all ${renderIsSketch ? 'bg-purple-600 text-white' : 'text-slate-400'}`}
                    >
                      Sketch
                    </button>
                    <button
                      type="button"
                      onClick={() => setRenderIsSketch(false)}
                      className={`flex-1 py-1 px-2 rounded-md font-medium text-center transition-all ${!renderIsSketch ? 'bg-purple-600 text-white' : 'text-slate-400'}`}
                    >
                      Hi-Fi
                    </button>
                  </div>
                </div>

                <div>
                  <label className="block text-[10px] text-slate-500 uppercase tracking-wide font-semibold mb-1">Camera ID (Optional)</label>
                  <input
                    type="text"
                    placeholder="Leave empty for default"
                    value={customCameraId}
                    onChange={(e) => setCustomCameraId(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-2.5 py-1 text-xs text-slate-200 placeholder-slate-600 focus:outline-none focus:border-purple-500"
                  />
                </div>
              </div>

              <button
                type="button"
                onClick={handleTriggerRender}
                disabled={actionLoading}
                className="w-full bg-purple-600/20 border border-purple-500/30 hover:bg-purple-600/30 text-purple-300 font-semibold text-xs py-2 rounded-lg transition-all"
              >
                {actionLoading ? 'Executing Render Job...' : 'Request Render Pipeline'}
              </button>
            </div>

            {/* Past Renders List */}
            <div className="flex-1 flex flex-col gap-2.5">
              <div className="flex justify-between items-center border-b border-slate-800/60 pb-1.5">
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 m-0">Render History ({renders.length})</h4>
                <button onClick={fetchRenders} className="text-xs text-purple-400 hover:text-purple-300">Refresh</button>
              </div>

              {renders.length === 0 ? (
                <div className="flex-1 flex flex-col items-center justify-center p-6 border border-dashed border-slate-800 rounded-xl text-slate-500 text-center">
                  <svg className="w-6 h-6 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                  </svg>
                  <p className="text-xs font-medium">No renders captured yet</p>
                </div>
              ) : (
                <div className="grid grid-cols-2 gap-3">
                  {renders.map((render) => (
                    <div key={render.id} className="bg-slate-950/60 border border-slate-800 rounded-lg p-2 flex flex-col gap-1.5 text-xs">
                      <div className="relative aspect-video rounded bg-slate-900 border border-slate-800 overflow-hidden group">
                        {render.image_url ? (
                          <img
                            src={getRenderFileUrl(render.id)}
                            alt="Blender Render Viewport"
                            className="w-full h-full object-cover group-hover:scale-105 transition-all duration-350"
                          />
                        ) : (
                          <div className="absolute inset-0 flex items-center justify-center text-slate-600 font-mono text-[10px]">
                            No Image URL
                          </div>
                        )}
                      </div>
                      <div className="flex items-center justify-between text-[10px] text-slate-500">
                        <span>Render: {render.id.substring(0, 6)}</span>
                        <span className="bg-slate-900 px-1 py-0.5 rounded border border-slate-800">
                          {new Date(render.created_at).toLocaleTimeString()}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

          </div>
        )}

      </div>
    </div>
  );
}
