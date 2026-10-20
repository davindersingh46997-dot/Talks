import "../styles/chatInput.css";
import {
  FiPaperclip,
  FiSend,
  FiCheckCircle,
  FiUploadCloud,
  FiX,
  FiAlertCircle,
  FiLoader,
} from "react-icons/fi";
import { useState, useRef, useEffect } from "react";
import axios from "axios";

interface ChatInputProps {
  onSendMessage: (text: string) => void;
  isGenerating: boolean;
}

interface UploadedFileInfo {
  name: string;
  size: number;
  progress: number;
  status: "uploading" | "processing" | "success" | "error";
  errorMessage?: string;
}

const formatFileSize = (bytes: number): string => {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
};

const ChatInput = ({ onSendMessage, isGenerating }: ChatInputProps) => {
  const [question, setQuestion] = useState("");
  const [fileInfo, setFileInfo] = useState<UploadedFileInfo | null>(null);

  const textareaRef = useRef<HTMLTextAreaElement | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const isBusy = fileInfo?.status === "uploading" || fileInfo?.status === "processing";

  const handleSend = () => {
    if (!question.trim() || isGenerating) return;

    onSendMessage(question.trim());
    setQuestion("");

    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }
  };

  const handleFileUpload = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // Reset the input value so user can upload the same file again if desired
    event.target.value = "";

    setFileInfo({
      name: file.name,
      size: file.size,
      progress: 0,
      status: "uploading",
    });

    const formData = new FormData();
    formData.append("file", file);

    try {
      await axios.post(
        "http://127.0.0.1:8000/rag/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          onUploadProgress: (progressEvent) => {
            const total = progressEvent.total || file.size;
            if (total > 0) {
              const percent = Math.min(
                Math.round((progressEvent.loaded * 100) / total),
                99
              );
              setFileInfo((prev) =>
                prev ? { ...prev, progress: percent } : null
              );
              if (percent >= 99) {
                setFileInfo((prev) =>
                  prev ? { ...prev, progress: 100, status: "processing" } : null
                );
              }
            }
          },
        }
      );

      setFileInfo((prev) =>
        prev
          ? {
              ...prev,
              progress: 100,
              status: "success",
            }
          : null
      );
    } catch (err: unknown) {
      console.error("Upload error:", err);
      let errorMsg = "File upload failed";
      if (axios.isAxiosError(err) && err.response?.data?.detail) {
        errorMsg = err.response.data.detail;
      }
      setFileInfo((prev) =>
        prev
          ? {
              ...prev,
              status: "error",
              errorMessage: errorMsg,
            }
          : null
      );
    }
  };

  const handleInputChange = (
    e: React.ChangeEvent<HTMLTextAreaElement>
  ) => {
    setQuestion(e.target.value);
  };

  const handleKeydown = (
    e: React.KeyboardEvent<HTMLTextAreaElement>
  ) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height =
        `${textareaRef.current.scrollHeight}px`;
    }
  }, [question]);

  return (
    <div className="chat-input-wrapper">
      <div className="chat-input-container">

        {/* Dynamic File Upload Preview Card */}
        {fileInfo && (
          <div className={`file-upload-card status-${fileInfo.status}`}>
            <div className="file-upload-header">
              <div className="file-upload-icon-box">
                {fileInfo.status === "uploading" && (
                  <FiUploadCloud className="file-upload-icon uploading-pulse" size={18} />
                )}
                {fileInfo.status === "processing" && (
                  <FiLoader className="file-upload-icon spin-animation" size={18} />
                )}
                {fileInfo.status === "success" && (
                  <FiCheckCircle className="file-upload-icon success-icon" size={18} />
                )}
                {fileInfo.status === "error" && (
                  <FiAlertCircle className="file-upload-icon error-icon" size={18} />
                )}
              </div>

              <div className="file-upload-details">
                <div className="file-upload-name-row">
                  <span className="file-upload-name" title={fileInfo.name}>
                    {fileInfo.name}
                  </span>
                  <span className="file-upload-size">
                    ({formatFileSize(fileInfo.size)})
                  </span>
                </div>

                <div className="file-upload-status-text">
                  {fileInfo.status === "uploading" && (
                    <span>
                      Uploading... <strong>{fileInfo.progress}%</strong>
                    </span>
                  )}
                  {fileInfo.status === "processing" && (
                    <span>Processing & indexing into RAG knowledge base...</span>
                  )}
                  {fileInfo.status === "success" && (
                    <span className="success-text">Document indexed & ready for RAG</span>
                  )}
                  {fileInfo.status === "error" && (
                    <span className="error-text">
                      {fileInfo.errorMessage || "Upload failed. Please try again."}
                    </span>
                  )}
                </div>
              </div>

              <div className="file-upload-actions">
                {fileInfo.status === "uploading" && (
                  <span className="file-upload-badge">{fileInfo.progress}%</span>
                )}
                {fileInfo.status === "processing" && (
                  <span className="file-upload-badge processing">Indexing...</span>
                )}
                {fileInfo.status === "success" && (
                  <span className="file-upload-badge success">Ready</span>
                )}
                <button
                  type="button"
                  className="file-upload-close-btn"
                  onClick={() => setFileInfo(null)}
                  title="Dismiss"
                  aria-label="Dismiss uploaded file"
                >
                  <FiX size={15} />
                </button>
              </div>
            </div>

            {/* Dynamic Progress Bar */}
            {(fileInfo.status === "uploading" || fileInfo.status === "processing") && (
              <div className="file-upload-progress-track">
                <div
                  className={`file-upload-progress-fill ${
                    fileInfo.status === "processing" ? "shimmer" : ""
                  }`}
                  style={{ width: `${fileInfo.progress}%` }}
                />
              </div>
            )}
          </div>
        )}

        {/* Text & Controls Row */}
        <div className="chat-input-text-row">
          {/* File Upload Button */}
          <button
            className={`chat-input-action-btn ${isBusy ? "disabled" : ""}`}
            aria-label="Attach file"
            type="button"
            onClick={() => fileInputRef.current?.click()}
            disabled={isBusy}
            title="Attach document (.pdf, .docx, .txt, .csv)"
          >
            <FiPaperclip size={18} />
          </button>

          {/* Hidden File Input */}
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.doc,.docx,.txt,.csv"
            style={{ display: "none" }}
            onChange={handleFileUpload}
            disabled={isBusy}
          />

          {/* Textarea */}
          <textarea
            ref={textareaRef}
            placeholder="Message Antigravity..."
            rows={1}
            value={question}
            onChange={handleInputChange}
            onKeyDown={handleKeydown}
            disabled={isGenerating}
          />

          {/* Send Button */}
          <button
            className={`chat-send-btn ${
              question.trim() && !isGenerating ? "active" : ""
            }`}
            aria-label="Send message"
            disabled={!question.trim() || isGenerating}
            type="button"
            onClick={handleSend}
          >
            <FiSend size={16} />
          </button>
        </div>

      </div>

      <div className="chat-disclaimer">
        Antigravity can make mistakes. Verify important info.
      </div>
    </div>
  );
};

export default ChatInput;