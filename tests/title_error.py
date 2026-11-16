
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
import os

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY is missing!")

chat_model = ChatOpenAI(
    model="nvidia/nemotron-3.5-lightning:free",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0.2,
    max_tokens=2048,
    max_retries=2,
    timeout=120
)

response = chat_model.invoke([
    HumanMessage(content=" Hello, AI agent!")
])

print("CONTENT:", repr(response.content))
print("METADATA:", response.response_metadata)
print("USAGE:", response.usage_metadata)
