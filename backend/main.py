from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from backend.core.database import get_db

from backend.services.chat_service import chat, chat_stream
from backend.services.history_service import (
    create_chat,
    list_chats,
    load_chat,
    update_chat_title,
    remove_chat,
)

from backend.api.routes.auth import router as auth_router


app = FastAPI()

app.include_router(auth_router)

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
    chat_id: int | None = None

class RenameRequest(BaseModel):
    title: str

@app.get("/")
def home():
    return {"message": "Backend is running!"}

@app.post("/chat/new")
def new_chat(
    db: Session = Depends(get_db),
):

    chat = create_chat(db=db)  # Replace with actual user ID

    return {
        "chat_id": chat.id,
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

@app.get("/chats")
def get_chats(
    db: Session = Depends(get_db),
):

    return list_chats(db=db)


@app.get("/chats/{chat_id}")
def get_chat_endpoint(
    chat_id: int,
    db: Session = Depends(get_db),
):

    chat = load_chat(
        db=db,
        chat_id=chat_id,
    )

    if chat is None:
        raise HTTPException(
            status_code=404,
            detail="Chat not found",
        )

    return chat

    
@app.delete("/chats/{chat_id}")
def delete_chat_endpoint(
    chat_id: int,
    db: Session = Depends(get_db),
):

    deleted = remove_chat(
        db=db,
        chat_id=chat_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Chat not found",
        )

    return {
        "message": "Chat deleted successfully"
    }


@app.patch("/chats/{chat_id}/rename")
def rename_chat(
    chat_id: int,
    request: RenameRequest,
    db: Session = Depends(get_db),
):

    chat = update_chat_title(
        db=db,
        chat_id=chat_id,
        new_title=request.title,
    )

    if chat is None:
        raise HTTPException(
            status_code=404,
            detail="Chat not found",
        )

    return {
        "message": "Chat renamed successfully"
    }


