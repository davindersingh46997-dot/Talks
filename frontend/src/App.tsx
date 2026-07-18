import { useState } from "react";
import ChatInput from "./components/ChatInput";
import ChatArea from "./components/ChatArea";
import type { Message } from "./types/chat";
import "./App.css";

function App() {

  const [messages, setMessages] = useState<Message[]>([]);

  return (
    <div className="app">

      <ChatArea messages={messages} />

      <ChatInput
        messages={messages}
        setMessages={setMessages}
      />

    </div>
  );
}

export default App;