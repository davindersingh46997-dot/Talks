# 🤖 AI Chatbot Assistant

A modern AI chatbot built with **React + TypeScript** on the frontend and **FastAPI + LangGraph + LangChain** on the backend.

The chatbot supports:

- 💬 Real-time chat interface
- ⚡ Streaming AI responses
- 🧠 Short-term conversation memory
- 📁 File upload support (UI ready)
- 🎤 Voice input support (UI ready)
- 🔌 FastAPI REST API
- 🤖 Hugging Face LLM Integration
- 🔄 LangGraph workflow
- 📜 Chat history management

---

# Project Structure

```
Agents/
│
├── frontend/
│   │
│   ├── src/
│   │   ├── components/
│   │   │     ChatInput.tsx
│   │   │     MessageBubble.tsx
│   │   │
│   │   ├── services/
│   │   │     api.ts
│   │   │
│   │   ├── styles/
│   │   │     ChatInput.css
│   │   │     MessageBubble.css
│   │   │
│   │   ├── types/
│   │   │     chat.ts
│   │   │
│   │   ├── App.tsx
│   │   └── main.tsx
│   │
│   ├── package.json
│   └── vite.config.ts
│
├── backend/
│   │
│   ├── app.py
│   ├── bot.py
│   ├── short_term.py
│   ├── requirements.txt
│   ├── .env
│   └── .env.example
│
├── environment/
│
├── .gitignore
└── README.md
```

---

# Tech Stack

## Frontend

- React
- TypeScript
- Vite
- CSS
- React Icons

---

## Backend

- Python 3.10+
- FastAPI
- Uvicorn
- LangChain
- LangGraph
- HuggingFace Hub
- Python Dotenv

---

# AI Model

Current model

```
Qwen/Qwen2.5-Coder-32B-Instruct
```

using

```
HuggingFaceEndpoint
```

---

# Environment Setup

Create

```
backend/.env
```

Example

```env
HF_TOKEN=your_huggingface_api_key
```

Never push this file to GitHub.

---

Create

```
backend/.env.example
```

```env
HF_TOKEN=your_huggingface_api_key
```

---

# Python Environment

Create virtual environment

```bash
python -m venv environment
```

Activate

### Windows

```bash
environment\Scripts\activate
```

---

Install dependencies

```bash
pip install -r requirements.txt
```

or

```bash
pip install fastapi
pip install uvicorn
pip install langchain
pip install langgraph
pip install langchain-huggingface
pip install python-dotenv
pip install huggingface_hub
```

---

# Frontend Setup

Move into frontend

```bash
cd frontend
```

Install packages

```bash
npm install
```

Start React

```bash
npm run dev
```

Runs on

```
http://localhost:5173
```

---

# Backend Setup

Move into backend

```bash
cd backend
```

Run FastAPI

```bash
uvicorn app:app --reload
```

Runs on

```
http://127.0.0.1:8000
```

Swagger

```
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## Health Check

```
GET /
```

Response

```json
{
    "message":"Backend is running!"
}
```

---

## Chat

```
POST /chat
```

Request

```json
{
    "message":"Hello"
}
```

Response

```json
{
    "response":"Hello! How can I help?"
}
```

---

## Streaming Chat

```
POST /chat/stream
```

Streams the response token by token.

---

# Project Workflow

```
User
      │
      ▼
React UI
      │
      ▼
ChatInput.tsx
      │
      ▼
FastAPI
      │
      ▼
app.py
      │
      ▼
bot.py
      │
      ▼
Short-Term Memory
      │
      ▼
LangGraph
      │
      ▼
LangChain
      │
      ▼
HuggingFace Model
      │
      ▼
Generated Response
      │
      ▼
FastAPI
      │
      ▼
React UI
      │
      ▼
MessageBubble
```

---

# Streaming Flow

```
User

↓

React fetch()

↓

FastAPI Streaming Endpoint

↓

chat_stream()

↓

HuggingFace stream()

↓

token

↓

token

↓

token

↓

React updates state

↓

Message grows live
```

---

# Current Features

- Chat UI
- AI Responses
- Streaming Output
- FastAPI Backend
- LangGraph Workflow
- Hugging Face Integration
- Short-Term Memory
- Automatic Scroll
- Message Bubbles
- Responsive Chat Input

---

# Planned Features

- Long-Term Memory
- RAG
- PDF Upload
- Image Understanding
- Voice Input
- Text-to-Speech
- Avatar Animation
- Multi-chat Sessions
- Authentication
- Database Storage
- Docker Deployment

---

# Git Ignore

```
environment/
venv/
node_modules/
dist/

__pycache__/
*.pyc

.env

.vscode/
.idea/
```

---

# Running the Project

Start backend

```bash
cd backend

uvicorn app:app --reload
```

Start frontend

```bash
cd frontend

npm run dev
```

Open

```
http://localhost:5173
```

---

# Future Architecture

```
                User
                  │
                  ▼
            React Frontend
                  │
                  ▼
            FastAPI Backend
                  │
        ┌─────────┴──────────┐
        │                    │
        ▼                    ▼
   Short Memory         Long Memory
        │                    │
        └─────────┬──────────┘
                  ▼
              LangGraph
                  ▼
             Agent Router
                  ▼
          Tool Calling Layer
                  ▼
          HuggingFace LLM
                  ▼
            Final Response
```

---

# Author

Developed by **Davinder Singh**

Project: AI Chatbot Assistant
