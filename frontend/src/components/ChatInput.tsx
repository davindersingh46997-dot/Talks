import "../styles/chatInput.css";
import { FiPaperclip, FiSend } from "react-icons/fi";
import { useState, useRef, useEffect } from "react";

interface ChatInputProps {
  onSendMessage: (text: string) => void;
  isGenerating: boolean;
}

const ChatInput = ({ onSendMessage, isGenerating }: ChatInputProps) => {
  const [question, setQuestion] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);

  const handleSend = () => {
    if (!question.trim() || isGenerating) return;
    onSendMessage(question.trim());
    setQuestion("");
    
    // Reset textarea height
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setQuestion(e.target.value);
  };

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [question]);

  return (
    <div className="chat-input-wrapper">
      <div className="chat-input-container">
        <button className="chat-input-action-btn" aria-label="Attach file" type="button">
          <FiPaperclip size={18} />
        </button>

        <textarea
          ref={textareaRef}
          placeholder="Message Antigravity..."
          rows={1}
          value={question}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          disabled={isGenerating}
        />

        <button
          className={`chat-send-btn ${question.trim() && !isGenerating ? "active" : ""}`}
          aria-label="Send message"
          onClick={handleSend}
          disabled={!question.trim() || isGenerating}
          type="button"
        >
          <FiSend size={16} />
        </button>
      </div>
      <div className="chat-disclaimer">
        Antigravity can make mistakes. Verify important info.
      </div>
    </div>
  );
};

export default ChatInput;