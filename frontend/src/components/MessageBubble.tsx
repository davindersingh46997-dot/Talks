import { useState } from "react";
import { FiCopy, FiCheck } from "react-icons/fi";
import type { Message } from "../types/chat";
import "../styles/MessageBubble.css";

interface MessageBubbleProps {
  message: Message;
}

// Subcomponent for Code Block with Copy functionality
const CodeBlock = ({ language, code }: { language: string; code: string }) => {
  const [copied, setCopied] = useState(false);

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error("Failed to copy code: ", err);
    }
  };

  return (
    <div className="code-block-container">
      <div className="code-block-header">
        <span className="code-block-lang">{language || "code"}</span>
        <button className="copy-code-btn" onClick={copyToClipboard}>
          {copied ? (
            <>
              <FiCheck size={12} />
              <span>Copied!</span>
            </>
          ) : (
            <>
              <FiCopy size={12} />
              <span>Copy code</span>
            </>
          )}
        </button>
      </div>
      <pre className="code-block-pre">
        <code className="code-block-code">{code}</code>
      </pre>
    </div>
  );
};

// Inline formatter for bold and inline-code
const renderInlineFormatting = (text: string) => {
  const codeParts = text.split("`");
  
  return codeParts.map((part, cIdx) => {
    // Odd indexes are inline code
    if (cIdx % 2 === 1) {
      return <code key={cIdx} className="message-inline-code">{part}</code>;
    }
    
    // Even indexes: parse bold **boldText**
    const boldParts = part.split("**");
    return boldParts.map((boldPart, bIdx) => {
      if (bIdx % 2 === 1) {
        return <strong key={bIdx} className="message-bold">{boldPart}</strong>;
      }
      return boldPart;
    });
  });
};

// Paragraph formatter that handles lists and inline styling
const renderTextParagraphs = (text: string) => {
  if (!text) return null;
  
  // Split by double newlines for paragraphs
  const paragraphs = text.split(/\n\n+/);

  return paragraphs.map((paragraph, pIdx) => {
    const lines = paragraph.split("\n");
    
    // Check if paragraph is actually a bullet list
    const isList = lines.every(
      (line) =>
        line.trim().startsWith("- ") ||
        line.trim().startsWith("* ") ||
        line.trim() === ""
    );
    
    if (isList && lines.some((line) => line.trim() !== "")) {
      return (
        <ul key={pIdx} className="message-list">
          {lines
            .filter((line) => line.trim() !== "")
            .map((line, lIdx) => {
              // Strip "- " or "* "
              const cleanLine = line.trim().substring(2);
              return (
                <li key={lIdx} className="message-list-item">
                  {renderInlineFormatting(cleanLine)}
                </li>
              );
            })}
        </ul>
      );
    }

    // Standard text paragraph
    return (
      <p key={pIdx} className="message-paragraph">
        {renderInlineFormatting(paragraph)}
      </p>
    );
  });
};

// Main formatted text renderer split by code blocks
const renderFormattedText = (text: string) => {
  const parts = text.split("```");
  if (parts.length === 1) {
    return renderTextParagraphs(text);
  }

  return parts.map((part, index) => {
    // Odd indexes are code blocks
    if (index % 2 === 1) {
      const lines = part.split("\n");
      const firstLine = lines[0].trim();
      const hasLanguage = firstLine && !firstLine.includes(" ") && firstLine.length < 15;
      
      const language = hasLanguage ? firstLine : "";
      const code = hasLanguage ? lines.slice(1).join("\n").trim() : part.trim();

      return <CodeBlock key={index} language={language} code={code} />;
    } else {
      // Even indexes are normal text paragraphs
      return <div key={index}>{renderTextParagraphs(part)}</div>;
    }
  });
};

const MessageBubble = ({ message }: MessageBubbleProps) => {
  const isUser = message.role === "user";

  return (
    <div className={`message-row ${isUser ? "user" : "assistant"}`}>
      {/* AI Avatar */}
      {!isUser && (
        <div className="message-avatar ai" aria-hidden="true">
          AI
        </div>
      )}
      
      <div className="message-content-wrapper">
        <div className={`message-bubble ${isUser ? "user-bubble" : "assistant-bubble"}`}>
          {isUser ? message.text : renderFormattedText(message.text)}
        </div>
      </div>
    </div>
  );
};

export default MessageBubble;