from dotenv import load_dotenv
import os

from langchain_huggingface import (
    ChatHuggingFace,
    HuggingFaceEndpoint,
)

from memory.short_term import ShortTermMemory

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

llm = HuggingFaceEndpoint(

    repo_id="Qwen/Qwen2.5-Coder-32B-Instruct",

    task="text-generation",

    max_new_tokens=2048,

    temperature=0.2,

    huggingfacehub_api_token=HF_TOKEN
)

chat_model = ChatHuggingFace(
    llm=llm
)