import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings

# Load .env from project root if needed
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

hf_token = os.getenv("HF_TOKEN")

embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={"device": "cpu", "token": hf_token} if hf_token else {"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)


def get_embedding_model():
    return embedding_model