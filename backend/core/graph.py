from langgraph.graph import StateGraph
from langgraph.graph import START, END
from langgraph.graph.message import add_messages

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
)

from typing import TypedDict, Annotated, Iterator

from backend.core.llm import chat_model
from backend.services.rag_service import get_content, format_documents

class ChatState(TypedDict):

    messages: Annotated[
        list,
        add_messages
    ]
    context: str


def retrieve_node(state: ChatState) -> dict:
    """
    RAG retrieval node: extracts the latest query and retrieves relevant context.
    """
    # If context is already provided and non-empty, retain it
    existing_context = state.get("context", "")
    if existing_context and isinstance(existing_context, str) and existing_context.strip():
        return {"context": existing_context}

    messages = state.get("messages", [])
    if not messages:
        return {"context": ""}

    # Extract latest user message
    last_message = messages[-1]
    query = ""
    if hasattr(last_message, "content"):
        query = str(last_message.content)
    elif isinstance(last_message, dict) and "content" in last_message:
        query = str(last_message["content"])
    else:
        query = str(last_message)

    if not query.strip():
        return {"context": ""}

    retrieved_context = get_content(query.strip())
    return {"context": retrieved_context}


def chatbot_node(state: ChatState) -> dict:
    """
    LLM node: injects retrieved context into system prompt and calls chat model.
    """
    raw_context = state.get("context", "")

    # Normalize context if passed as documents list
    if isinstance(raw_context, list):
        context = format_documents(raw_context)
    elif isinstance(raw_context, str):
        context = raw_context.strip()
    else:
        context = str(raw_context).strip()

    if context:
        system_content = f"""You are a helpful AI assistant.

Use the following retrieved context to answer the user's question accurately.

Retrieved Context:
{context}

Instructions:
- Use the retrieved context when it contains relevant information.
- Do not invent facts that are not supported by the context.
- If the context does not contain the answer, answer helpfully based on your general knowledge while noting that the answer was not found in the uploaded documents.
"""
    else:
        system_content = "You are a helpful, knowledgeable AI assistant. Provide clear, accurate, and concise answers."

    system_message = SystemMessage(content=system_content)

    messages = [
        system_message,
        *state["messages"]
    ]

    response = chat_model.invoke(messages)

    return {
        "messages": [response],
        "context": context,
    }


graph_builder = StateGraph(ChatState)

graph_builder.add_node("retrieve", retrieve_node)
graph_builder.add_node("chatbot", chatbot_node)

graph_builder.add_edge(START, "retrieve")
graph_builder.add_edge("retrieve", "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()