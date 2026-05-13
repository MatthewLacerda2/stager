import { Outlet } from 'react-router-dom';

export default function Layout() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-purple-500/30 selection:text-purple-200">
      {/* MAIN CONTAINER */}
      <main className="flex-1 flex flex-col relative">
        <Outlet />
      </main>
    </div>
  );
}
