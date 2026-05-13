import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import ScenesPage from './pages/ScenesPage';
import ChatsPage from './pages/ChatsPage';
import ChatRoomPage from './pages/ChatRoomPage';
import RendersPage from './pages/RendersPage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          {/* Index path: show Scenes Dashboard */}
          <Route index element={<ScenesPage />} />
          
          {/* Scene specific routes */}
          <Route path="scenes/:sceneId/chats" element={<ChatsPage />} />
          <Route path="scenes/:sceneId/chats/:chatId" element={<ChatRoomPage />} />
          <Route path="scenes/:sceneId/renders" element={<RendersPage />} />
          
          {/* Fallback routing */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
