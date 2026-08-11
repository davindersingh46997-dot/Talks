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
    load_chat_history,
    update_chat_title,
    remove_chat,
)

from backend.api.routes.auth import router as auth_router
from backend.api.dependencies import get_current_user
from backend.models.user import User
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add middleware immediately after creating the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers AFTER middleware
app.include_router(auth_router)

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
    current_user: User = Depends(get_current_user),
):

    chat = create_chat(
        db=db,
        user_id=current_user.id,
    )

    return {
        "chat_id": chat.id,
    }

@app.post("/chat/stream")
def chat_stream_endpoint(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    def generate():
        for chunk in chat_stream(
            request.message, 
            db=db, 
            user_id=current_user.id, 
            chat_id=request.chat_id
            ):
            yield chunk

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )

@app.get("/chats")
def get_chats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_chats(
        db=db,
        user_id=current_user.id,
    )


@app.get("/chats/{chat_id}")
def get_chat_endpoint(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if chat_id is None:
        raise HTTPException(
            status_code=400,
            detail="Chat ID is required",
        )

    chat = load_chat(
        db=db,
        chat_id=chat_id,
        user_id=current_user.id,
    )

    messages = load_chat_history(
        db=db,
        chat_id=chat_id,
        user_id=current_user.id,
    )

    return {
        "id": chat.id,
        "title": chat.title,
        "user_id": chat.user_id,
        "created_at": chat.created_at,
        "updated_at": chat.updated_at,
        "messages": [
            {
                "id": message.id,
                "chat_id": message.chat_id,
                "role": message.role,
                "content": message.content,
                "created_at": message.created_at,
            }
            for message in messages
        ],
    }

    
@app.delete("/chats/{chat_id}")
def delete_chat_endpoint(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    deleted = remove_chat(
        db=db,
        chat_id=chat_id,
        user_id=current_user.id
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
    current_user: User = Depends(get_current_user),
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
