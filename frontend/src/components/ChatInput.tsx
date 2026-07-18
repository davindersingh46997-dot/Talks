import "../styles/ChatInput.css";
import { FiPaperclip, FiMic, FiSend } from "react-icons/fi";
import { useState } from "react";
import type { Message } from "../types/chat";

interface ChatInputProps {
  messages: Message[];
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>;
}

const ChatInput = ({ messages, setMessages }: ChatInputProps) => {
  const [question, setQuestion] = useState("");

  const sendMessage = async () => {

    if (!question.trim()) return;

    const userMessage = {
        id: Date.now(),
        role: "user" as const,
        text: question,
    };

    setMessages((prev) => [
        ...prev,
        userMessage,
    ]);

    const currentQuestion = question;

    setQuestion("");

    // <-- We'll add streaming code here next
    const aiMessageId = Date.now() + 1;

    setMessages((prev) => [
      ...prev,
      {
        id: aiMessageId,
        role: "assistant",
        text: "",
      },
    ]);

    try {
  // fetch()

  const response = await fetch("http://127.0.0.1:8000/chat/stream", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    message: currentQuestion,
  }),
});

  // reader

  const reader = response.body?.getReader();

if (!reader) {
  throw new Error("Unable to read response stream.");
}

const decoder = new TextDecoder();

let aiResponse = "";

  // while loop

  while (true) {
  const { done, value } = await reader.read();

  if (done) {
    break;
  }

  const chunk = decoder.decode(value, { stream: true });

  aiResponse += chunk;

  setMessages((prev) =>
    prev.map((msg) =>
      msg.id === aiMessageId
        ? {
            ...msg,
            text: aiResponse,
          }
        : msg
    )
  );
}

} catch (error) {
  console.error(error);

  setMessages((prev) =>
    prev.map((msg) =>
      msg.id === aiMessageId
        ? {
            ...msg,
            text: "⚠️ Error generating response.",
          }
        : msg
    )
  );
}

};

  return (
    <div className="chat-input-container">
      <button className="icon-btn" aria-label="Upload file">
        <FiPaperclip size={20} />
      </button>

      <textarea
        placeholder="Ask me anything..."
        rows={1}
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
          }
        }}
      />

      <button className="icon-btn" aria-label="Voice input">
        <FiMic size={20} />
      </button>

      <button
        className="send-btn"
        aria-label="Send message"
        onClick={sendMessage}
      >
        <FiSend size={18} />
      </button>
    </div>
  );
};

export default ChatInput;