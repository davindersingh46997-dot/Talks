import Sidebar from "../components/sidebar";
import ChatArea from "../components/ChatArea";
import ChatInput from "../components/ChatInput";
import type { Chat, Message } from "../types/chat";
import "../App.css";
import { useState,useEffect } from "react";

interface BackendMessage {
  role: "user" | "assistant";
  content: string;
}

interface BackendChatDetail {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
  messages: BackendMessage[];
}

function ChatPage() {
  const [chats, setChats] = useState<Chat[]>([]);
  const [activeChatId, setActiveChatId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);

  // Fetch all chats for sidebar
  const fetchChats = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/chats");
      if (res.ok) {
        const data = await res.json();
        setChats(data);
        return data as Chat[];
      }
    } catch (err) {
      console.error("Error fetching chats:", err);
    }
    return [];
  };

  useEffect(() => {
    fetchChats();
  }, []);

  // Fetch messages for a specific chat
  const handleSelectChat = async (chatId: string) => {
    setActiveChatId(chatId);
    try {
      const res = await fetch(`http://127.0.0.1:8000/chats/${chatId}`);
      if (res.ok) {
        const data: BackendChatDetail = await res.json();
        const mapped: Message[] = data.messages.map((m, idx) => ({
          id: `${chatId}-${idx}`,
          role: m.role,
          text: m.content,
        }));
        setMessages(mapped);
      }
    } catch (err) {
      console.error(`Error loading chat ${chatId}:`, err);
    }
  };

  // Create a new chat session
  const handleCreateChat = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/chat/new", {
        method: "POST",
      });
      if (res.ok) {
        const data = await res.json();
        const newChatId = data.chat_id;
        await fetchChats();
        setActiveChatId(newChatId);
        setMessages([]);
        return newChatId as string;
      }
    } catch (err) {
      console.error("Error creating chat:", err);
    }
    return null;
  };

  // Delete a chat session
  const handleDeleteChat = async (chatId: string) => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/chats/${chatId}`, {
        method: "DELETE",
      });
      if (res.ok) {
        const updatedList = await fetchChats();
        
        // If we deleted the active chat, select another one
        if (activeChatId === chatId) {
          if (updatedList && updatedList.length > 0) {
            handleSelectChat(updatedList[0].id);
          } else {
            setActiveChatId(null);
            setMessages([]);
          }
        }
      }
    } catch (err) {
      console.error(`Error deleting chat ${chatId}:`, err);
    }
  };

  // Rename a chat session
  const handleRenameChat = async (chatId: string, newTitle: string) => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/chats/${chatId}/rename`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          title: newTitle,
        }),
      });
      if (res.ok) {
        fetchChats();
      }
    } catch (err) {
      console.error(`Error renaming chat ${chatId}:`, err);
    }
  };

  // Send a message and stream the AI response
  const handleSendMessage = async (text: string) => {
    if (isGenerating) return;
    setIsGenerating(true);

    let currentChatId = activeChatId;

    // If there is no active chat, automatically create one first (like ChatGPT/Claude)
    if (!currentChatId) {
      const newId = await handleCreateChat();
      if (!newId) {
        setIsGenerating(false);
        return;
      }
      currentChatId = newId;
    }

    // Add user message to state
    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: "user",
      text: text,
    };
    
    // Setup placeholder for AI message
    const aiMessageId = `ai-${Date.now()}`;
    const aiMessagePlaceholder: Message = {
      id: aiMessageId,
      role: "assistant",
      text: "",
    };

    setMessages((prev) => [...prev, userMessage, aiMessagePlaceholder]);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat/stream", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: text,
          chat_id: currentChatId,
        }),
      });

      if (!response.body) {
        throw new Error("Unable to read stream body.");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let aiResponseText = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        aiResponseText += chunk;

        // Update active message in state
        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === aiMessageId ? { ...msg, text: aiResponseText } : msg
          )
        );
      }

      // Re-fetch chat list to get updated titles (AI title generation)
      await fetchChats();

    } catch (error) {
      console.error("Streaming error:", error);
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === aiMessageId
            ? { ...msg, text: "⚠️ Error generating response. Please try again." }
            : msg
        )
      );
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="app">
      <Sidebar
      chats={chats}
      activeChatId={activeChatId}
      onSelectChat={handleSelectChat}
      onCreateChat={handleCreateChat}
      onDeleteChat={handleDeleteChat}
      onRenameChat={handleRenameChat}
      isCollapsed={isSidebarCollapsed}
      onToggleCollapse={() => setIsSidebarCollapsed(!isSidebarCollapsed)}

      pinnedChatIds={[]}

      onTogglePinChat={(chatId) => {
        console.log("Toggle pin:", chatId);
      }}

      activeModel="Qwen 2.5"

      onChangeModel={(model) => {
        console.log("Model changed:", model);
      }}

      onClearAllChats={() => {
        console.log("Clear all chats");
      }}
    />

      <div className={`main-content ${isSidebarCollapsed ? "collapsed" : ""}`}>
        <ChatArea
          messages={messages}
          onSelectSuggestion={handleSendMessage}
        />

        <ChatInput
          onSendMessage={handleSendMessage}
          isGenerating={isGenerating}
        />
      </div>
    </div>
  );
}

export default ChatPage;