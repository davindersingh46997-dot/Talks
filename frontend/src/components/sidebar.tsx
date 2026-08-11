import { useState, useEffect } from "react";
import "../styles/Sidebar.css";
import type { Chat } from "../types/chat";
import { 
  FiPlus, 
  FiTrash2, 
  FiSidebar, 
  FiMessageSquare, 
  FiEdit2, 
  FiSearch, 
  FiSettings, 
  FiBookmark, 
  FiCpu, 
  FiX, 
  FiDatabase,
  FiSlash,
} from "react-icons/fi";

interface SidebarProps {
    chats: Chat[];
    activeChatId: number | null;
    onSelectChat: (chatId: number) => void;
    onCreateChat: () => void;
    onDeleteChat: (chatId: number) => void;
    onRenameChat: (chatId: number, newTitle: string) => void;
    isCollapsed: boolean;
    onToggleCollapse: () => void;
    pinnedChatIds: number[];
    onTogglePinChat: (chatId: number) => void;
    activeModel: string;
    onChangeModel: (model: string) => void;
    onClearAllChats: () => void;
}

// Grouping chats by date periods and pinning state
const getGroupForChat = (updatedAtStr: string, isPinned: boolean): string => {
  if (isPinned) return "Pinned";

  try {
    const updatedAt = new Date(updatedAtStr);
    const now = new Date();
    
    // Reset hours to compare calendar days
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    
    const sevenDaysAgo = new Date(today);
    sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);

    const thirtyDaysAgo = new Date(today);
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
    
    if (updatedAt >= today) {
      return "Today";
    } else if (updatedAt >= yesterday) {
      return "Yesterday";
    } else if (updatedAt >= sevenDaysAgo) {
      return "Previous 7 Days";
    } else if (updatedAt >= thirtyDaysAgo) {
      return "Previous 30 Days";
    } else {
      return "Older";
    }
  } catch (err) {
    return "Older";
  }
};

const Sidebar = ({
  chats,
  activeChatId,
  onSelectChat,
  onCreateChat,
  onDeleteChat,
  onRenameChat,
  isCollapsed,
  onToggleCollapse,
  pinnedChatIds,
  onTogglePinChat,
  activeModel,
  onChangeModel,
  onClearAllChats,
}: SidebarProps) => {
  const [searchQuery, setSearchQuery] = useState("");
  const [editingChatId, setEditingChatId] = useState<number | null>(null);
  const [editTitle, setEditTitle] = useState("");
  const [showSettingsModal, setShowSettingsModal] = useState(false);
  const [showModelDropdown, setShowModelDropdown] = useState(false);

  const handleStartRename = (chat: Chat, e: React.MouseEvent) => {
    e.stopPropagation();
    setEditingChatId(chat.id);
    setEditTitle(chat.title);
  };

  const handleSaveRename = (chatId: number) => {
    if (editTitle.trim()) {
      onRenameChat(chatId, editTitle.trim());
    }
    setEditingChatId(null);
    setEditTitle("");
  };

  const handleCancelRename = () => {
    setEditingChatId(null);
    setEditTitle("");
  };

  // Format timestamp relative text
  const getRelativeTime = (isoString: string) => {
    try {
      const date = new Date(isoString);
      const now = new Date();
      const diffMs = now.getTime() - date.getTime();
      
      const diffMins = Math.floor(diffMs / 60000);
      const diffHours = Math.floor(diffMs / 3600000);
      const diffDays = Math.floor(diffMs / 86400000);

      if (diffMins < 1) return "Just now";
      if (diffMins < 60) return `${diffMins}m ago`;
      if (diffHours < 24) return `${diffHours}h ago`;
      if (diffDays === 1) return "Yesterday";
      if (diffDays < 7) return `${diffDays}d ago`;
      
      return date.toLocaleDateString(undefined, { month: "short", day: "numeric" });
    } catch {
      return "";
    }
  };

  // Filter chats by search query
  const filteredChats = chats.filter((chat) =>
    chat.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Initialize grouping dictionary
  const groups: { [key: string]: Chat[] } = {
    Pinned: [],
    Today: [],
    Yesterday: [],
    "Previous 7 Days": [],
    "Previous 30 Days": [],
    Older: [],
  };

  // Distribute chats into lists
  filteredChats.forEach((chat) => {
    const isPinned = pinnedChatIds.includes(chat.id);
    const group = getGroupForChat(chat.updated_at, isPinned);
    groups[group].push(chat);
  });

  const groupOrder = ["Pinned", "Today", "Yesterday", "Previous 7 Days", "Previous 30 Days", "Older"];

  const models = ["Qwen 2.5 Coder", "Claude 3.5 Sonnet", "DeepSeek V3", "GPT-5"];

  return (
    <div className="sidebar-container">
      {/* Floating Toggle Button when collapsed */}
      {isCollapsed && (
        <button
          className="floating-toggle-btn"
          title="Show sidebar"
          onClick={onToggleCollapse}
        >
          <FiSidebar size={18} />
        </button>
      )}

      <div className={`sidebar ${isCollapsed ? "collapsed" : ""}`}>
        {/* Brand Header */}
        <div className="sidebar-header">
          <div className="sidebar-brand">
            <span className="brand-icon">✦</span>
            <span className="brand-name">Antigravity</span>
            <span className="version-badge">PRO</span>
          </div>
          <button
            className="sidebar-toggle-btn"
            title="Collapse sidebar"
            onClick={onToggleCollapse}
          >
            <FiSidebar size={17} />
          </button>
        </div>

        {/* New Chat Area */}
        <div className="new-chat-container">
          <button className="new-chat-btn" onClick={onCreateChat}>
            <div className="new-chat-btn-left">
              <FiPlus size={16} />
              <span>New chat</span>
            </div>
            <kbd className="kbd-shortcut">Ctrl+N</kbd>
          </button>
        </div>

        {/* Search Field */}
        <div className="sidebar-search-container">
          <div className="search-input-wrapper">
            <FiSearch size={14} className="search-icon-inside" />
            <input
              type="text"
              className="sidebar-search-input"
              placeholder="Search conversations..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
        </div>

        {/* Chat History List */}
        <div className="chat-history">
          {filteredChats.length === 0 ? (
            <div style={{ padding: "30px 20px", color: "var(--text-secondary)", fontSize: "13px", textAlign: "center", opacity: 0.7 }}>
              <FiSlash size={20} style={{ marginBottom: "8px", opacity: 0.5 }} />
              <div>{searchQuery ? "No results found" : "No history yet"}</div>
            </div>
          ) : (
            groupOrder.map((groupName) => {
              const groupChats = groups[groupName];
              if (groupChats.length === 0) return null;

              return (
                <div key={groupName} style={{ display: "flex", flexDirection: "column" }}>
                  <div className="sidebar-group-header">{groupName}</div>
                  
                  {groupChats.map((chat) => {
                    const isPinned = pinnedChatIds.includes(chat.id);
                    return (
                      <div
                        key={chat.id}
                        className={`chat-card ${chat.id === activeChatId ? "active" : ""}`}
                        onClick={() => {
                          if (editingChatId !== chat.id) {
                            onSelectChat(chat.id);
                          }
                        }}
                      >
                        {editingChatId === chat.id ? (
                          <input
                            type="text"
                            className="chat-card-rename-input"
                            value={editTitle}
                            onChange={(e) => setEditTitle(e.target.value)}
                            onKeyDown={(e) => {
                              if (e.key === "Enter") handleSaveRename(chat.id);
                              if (e.key === "Escape") handleCancelRename();
                            }}
                            onBlur={() => handleSaveRename(chat.id)}
                            autoFocus
                            onClick={(e) => e.stopPropagation()}
                          />
                        ) : (
                          <>
                            <div className="chat-card-main-info">
                              <FiMessageSquare size={15} style={{ flexShrink: 0, opacity: 0.7, color: chat.id === activeChatId ? "var(--accent-color)" : "inherit" }} />
                              <div className="chat-card-text-container">
                                <div className="chat-title-container" title={chat.title}>
                                  {chat.title}
                                </div>
                                <span className="chat-card-meta">{getRelativeTime(chat.updated_at)}</span>
                              </div>
                            </div>

                            {/* Pin icon (visible if pinned, otherwise on hover action bar) */}
                            {isPinned && !editingChatId && (
                              <FiBookmark size={12} className="pin-indicator-icon" />
                            )}

                            {/* Hover Actions Menu */}
                            <div className="chat-actions-container">
                              <button
                                className={`chat-action-btn ${isPinned ? "active-pin" : ""}`}
                                title={isPinned ? "Unpin chat" : "Pin chat"}
                                onClick={(e) => {
                                  e.stopPropagation();
                                  onTogglePinChat(chat.id);
                                }}
                              >
                                <FiBookmark size={13} />
                              </button>
                              <button
                                className="chat-action-btn"
                                title="Rename chat"
                                onClick={(e) => handleStartRename(chat, e)}
                              >
                                <FiEdit2 size={13} />
                              </button>
                              <button
                                className="chat-action-btn delete"
                                title="Delete chat"
                                onClick={(e) => {
                                  e.stopPropagation();
                                  onDeleteChat(chat.id);
                                }}
                              >
                                <FiTrash2 size={13} />
                              </button>
                            </div>
                          </>
                        )}
                      </div>
                    );
                  })}
                </div>
              );
            })
          )}
        </div>

        {/* Footer Container */}
        <div className="sidebar-footer-container">
          {/* Active Model Indicator */}
          <div className="model-indicator-row">
            <div 
              className="model-indicator-badge"
              onClick={() => setShowModelDropdown(!showModelDropdown)}
            >
              <FiCpu size={13} />
              <span>{activeModel}</span>
            </div>
            
            {showModelDropdown && (
              <div 
                className="input-model-dropdown" 
                style={{ bottom: "90px", left: "16px" }}
              >
                {models.map((m) => (
                  <button
                    key={m}
                    className={`input-model-dropdown-item ${m === activeModel ? "active" : ""}`}
                    onClick={() => {
                      onChangeModel(m);
                      setShowModelDropdown(false);
                    }}
                  >
                    {m}
                  </button>
                ))}
              </div>
            )}

            <button 
              className="footer-action-icon-btn" 
              title="Settings"
              onClick={() => setShowSettingsModal(true)}
            >
              <FiSettings size={15} />
            </button>
          </div>

          {/* Storage Indicator */}
          <div className="storage-indicator-container">
            <div className="storage-labels">
              <span style={{ display: "flex", alignItems: "center", gap: "4px" }}>
                <FiDatabase size={10} />
                <span>Storage</span>
              </span>
              <span>1.2 GB of 10 GB</span>
            </div>
            <div className="storage-bar-bg">
              <div className="storage-bar-fill" style={{ width: "12%" }}></div>
            </div>
          </div>

          {/* Profile Card */}
          <div className="sidebar-footer">
            <div className="user-profile">
              <div className="user-avatar">U</div>
              <div className="user-info-text">
                <span className="user-name">User Account</span>
                <span className="plan-badge">Pro Account</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Settings Modal (Overlay) */}
      {showSettingsModal && (
        <div 
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100vw",
            height: "100vh",
            backgroundColor: "rgba(0,0,0,0.6)",
            backdropFilter: "blur(4px)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 9999,
          }}
          onClick={() => setShowSettingsModal(false)}
        >
          <div 
            style={{
              background: "#1e1e20",
              border: "1px solid var(--border-color)",
              borderRadius: "16px",
              padding: "24px",
              width: "100%",
              maxWidth: "400px",
              boxShadow: "0 20px 25px -5px rgba(0, 0, 0, 0.5)",
              color: "var(--text-primary)",
              display: "flex",
              flexDirection: "column",
              gap: "20px",
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <h3 style={{ margin: 0, fontFamily: "var(--heading)", fontSize: "18px" }}>Settings</h3>
              <button 
                style={{ background: "transparent", border: "none", color: "var(--text-secondary)", cursor: "pointer" }}
                onClick={() => setShowSettingsModal(false)}
              >
                <FiX size={18} />
              </button>
            </div>

            <div style={{ display: "flex", flexDirection: "column", gap: "12px", fontSize: "14px" }}>
              <div style={{ display: "flex", justifyContent: "space-between", paddingBottom: "10px", borderBottom: "1px solid var(--border-color)" }}>
                <span style={{ color: "var(--text-secondary)" }}>Theme</span>
                <span style={{ fontWeight: 600 }}>Dark Theme (Active)</span>
              </div>
              <div style={{ display: "flex", justifyContent: "space-between", paddingBottom: "10px", borderBottom: "1px solid var(--border-color)" }}>
                <span style={{ color: "var(--text-secondary)" }}>Plan Details</span>
                <span style={{ fontWeight: 600, color: "var(--accent-color)" }}>Premium Pro</span>
              </div>
              <div style={{ display: "flex", justifyContent: "space-between", paddingBottom: "10px", borderBottom: "1px solid var(--border-color)" }}>
                <span style={{ color: "var(--text-secondary)" }}>Version</span>
                <span>v1.2.0</span>
              </div>
            </div>

            <div style={{ borderTop: "1px solid var(--border-color)", paddingTop: "16px", display: "flex", flexDirection: "column", gap: "10px" }}>
              <span style={{ fontSize: "12px", color: "var(--text-secondary)", fontWeight: 600, textTransform: "uppercase" }}>Danger Zone</span>
              <button 
                style={{
                  width: "100%",
                  padding: "10px",
                  borderRadius: "8px",
                  background: "rgba(239, 68, 68, 0.1)",
                  border: "1px solid rgba(239, 68, 68, 0.2)",
                  color: "var(--danger-color)",
                  fontWeight: 600,
                  fontSize: "13.5px",
                  cursor: "pointer",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  gap: "8px",
                }}
                onClick={() => {
                  if (confirm("Are you sure you want to delete ALL chats? This action is permanent.")) {
                    onClearAllChats();
                    setShowSettingsModal(false);
                  }
                }}
              >
                <FiTrash2 size={14} />
                <span>Delete all conversations</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Sidebar;