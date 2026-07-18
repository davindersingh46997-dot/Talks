import type { Message } from "../types/chat";
import MessageBubble from "./MessageBubble";
import "../styles/ChatArea.css";
import { useEffect, useRef } from "react";
import "../styles/ChatArea.css";

interface ChatAreaProps {
  messages: Message[];
}

const ChatArea = ({ messages }: ChatAreaProps) => {

    const bottomRef = useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

  return (
    <div className="chat-area">
      {messages.map((message) => (
        <MessageBubble
          key={message.id}
          message={message}
        />
      ))}
      <div ref={bottomRef} />
    </div>
  );
};

export default ChatArea;