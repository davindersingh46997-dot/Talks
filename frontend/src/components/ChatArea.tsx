import type { Message } from "../types/chat";
import MessageBubble from "./MessageBubble";
import "../styles/chatArea.css";
import { useEffect, useRef } from "react";

interface ChatAreaProps {
  messages: Message[];
  onSelectSuggestion: (suggestionText: string) => void;
  isGenerating?: boolean;
}

const ChatArea = ({
  messages,
  onSelectSuggestion,
  isGenerating = false,
}: ChatAreaProps) => {
  const bottomRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const suggestions = [
    {
      header: "Explain quantum computing",
      sub: "Explain it in simple terms for a beginner",
      prompt: "Explain quantum computing in simple terms for a beginner."
    },
    {
      header: "Draft a project email",
      sub: "Write a professional update for stakeholders",
      prompt: "Draft a professional email updating stakeholders on our project progress."
    },
    {
      header: "Brainstorm startup names",
      sub: "Generate creative names for a new coffee brand",
      prompt: "Help me brainstorm 10 creative names for a specialty coffee shop brand."
    },
    {
      header: "Solve a coding problem",
      sub: "Write a clean function in TypeScript",
      prompt: "Show me a clean TypeScript function to debounce an event handler with explanation."
    }
  ];

  if (messages.length === 0) {
    return (
      <div className="chat-area">
        <div className="empty-state">
          <div className="welcome-logo">✦</div>
          <h2>What can I help with today?</h2>
          <div className="suggestions-grid">
            {suggestions.map((s, idx) => (
              <button
                key={idx}
                className="suggestion-card"
                onClick={() => onSelectSuggestion(s.prompt)}
              >
                <span className="suggestion-card-header">{s.header}</span>
                <span className="suggestion-card-sub">{s.sub}</span>
              </button>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-area">
      <div className="chat-area-container">
        {messages.map((message, idx) => (
          <MessageBubble
            key={message.id}
            message={message}
            isStreaming={isGenerating && idx === messages.length - 1}
          />
        ))}
        <div ref={bottomRef} style={{ height: "1px" }} />
      </div>
    </div>
  );
};

export default ChatArea;