from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bot import chat
from fastapi.responses import StreamingResponse
from bot import chat_stream
from history import create_chat, list_chats, load_chat, chat_path

app = FastAPI()

# Allow React frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    chat_id: str | None = None

class RenameRequest(BaseModel):
    title: str

@app.get("/")
def home():
    return {"message": "Backend is running!"}

@app.post("/chat")
def chat_endpoint(request: ChatRequest):

    print("Request received:", request.message, "Chat ID:", request.chat_id)

    response = chat(request.message, chat_id=request.chat_id)

    print("Response generated:", response)

    return {
        "response": response
    }

@app.post("/chat/stream")
def chat_stream_endpoint(request: ChatRequest):

    def generate():
        for chunk in chat_stream(request.message, chat_id=request.chat_id):
            yield chunk

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )

@app.post("/chat/new")
def new_chat():

    chat_id = create_chat()

    return {
        "chat_id": chat_id
    }

@app.get("/chats")
def get_chats():

    chats = list_chats()

    sidebar = []

    for chat in chats:

        sidebar.append(
            {
                "id": chat["id"],
                "title": chat["title"],
                "updated_at": chat["updated_at"]
            }
        )

    return sidebar

@app.get("/chats/{chat_id}")
def get_chat_endpoint(chat_id: str):
    try:
        chat_data = load_chat(chat_id)
        return chat_data
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Chat not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/chats/{chat_id}")
def delete_chat_endpoint(chat_id: str):
    import os
    try:
        path = chat_path(chat_id)
        if path.exists():
            os.remove(path)
            return {"message": "Chat deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Chat not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chats/{chat_id}/rename")
def rename_chat_endpoint(chat_id: str, request: RenameRequest):
    try:
        from history import save_chat
        chat_data = load_chat(chat_id)
        chat_data["title"] = request.title
        save_chat(chat_data)
        return {"message": "Chat renamed successfully"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Chat not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



