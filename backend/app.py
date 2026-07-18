from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bot import chat
from fastapi.responses import StreamingResponse
from bot import chat_stream

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

@app.get("/")
def home():
    return {"message": "Backend is running!"}

@app.post("/chat")
def chat_endpoint(request: ChatRequest):

    print("Request received:", request.message)

    response = chat(request.message)

    print("Response generated:", response)

    return {
        "response": response
    }

@app.post("/chat/stream")
def chat_stream_endpoint(request: ChatRequest):

    def generate():
        for chunk in chat_stream(request.message):
            yield chunk

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )
