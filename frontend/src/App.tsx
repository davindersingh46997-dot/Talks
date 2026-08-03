import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import LoginPage from "./pages/login_page";
import ChatPage from "./pages/chat_page";
import Sign_in from "./pages/sign_in";
import Sign_up from "./pages/sign_up";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Login */}
        <Route path="/" element={<LoginPage />} />

        {/* Chat */}
        <Route path="/chat" element={<ChatPage />} />

        <Route path="/sign_in" element={<Sign_in />} />

        <Route path="/sign_up" element={<Sign_up />} />

        <Route path="/chat" element={<ChatPage />} />

        {/* Unknown Route */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;