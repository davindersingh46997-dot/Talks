import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import LoginPage from "./pages/login_page";
import ChatPage from "./pages/chat_page";
import Sign_in from "./pages/sign_in";
import Sign_up from "./pages/sign_up";
import { useEffect, useState } from "react";

function App() {

  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

    useEffect(() => {
      const token = localStorage.getItem("access_token");

      if (token) {
          setIsAuthenticated(true);
      } else {
          setIsAuthenticated(false);
      }
  }, []);

  if (isAuthenticated === null) {
    return <div>Loading...</div>;
  }

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