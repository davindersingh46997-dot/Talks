from typing import TypedDict,Annotated,Iterator

from dotenv import load_dotenv
import os

from langgraph.graph import StateGraph
from langgraph.graph import START, END
from langgraph.graph.message import add_messages

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
)

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


class ChatState(TypedDict):

    messages: Annotated[
        list,
        add_messages
    ]


def chatbot_node(state: ChatState) -> ChatState:
    """
    Main chatbot node.
    Receives the conversation history and
    generates the assistant response.
    """

    response = chat_model.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }

graph_builder = StateGraph(ChatState)

graph_builder.add_node(
    "chatbot",
    chatbot_node
)

graph_builder.add_edge(
    START,
    "chatbot"
)

graph_builder.add_edge(
    "chatbot",
    END
)

graph = graph_builder.compile()

memory = ShortTermMemory()

SESSION_ID = "default"

def chat(question: str, chat_id: str | None = None):

    if chat_id:
        from history_service import load_chat
        try:
            chat_data = load_chat(chat_id)
            history = []
            for msg in chat_data.get("messages", []):
                if msg["role"] == "user":
                    history.append(HumanMessage(content=msg["content"]))
                else:
                    history.append(AIMessage(content=msg["content"]))
        except Exception as e:
            print(f"Error loading chat in chat(): {e}")
            history = []
    else:
        history = memory.get_messages(SESSION_ID)

    history.append(
        HumanMessage(content=question)
    )

    inputs = {
        "messages": history
    }

    result = graph.invoke(inputs)

    response = result["messages"][-1]

    if chat_id:
        from history_service import load_chat, save_chat, generate_ai_title
        try:
            chat_data = load_chat(chat_id)
            chat_data["messages"].append({"role": "user", "content": question})
            chat_data["messages"].append({"role": "assistant", "content": response.content})
            
            # If the title is "New Chat", generate a smart title
            if chat_data.get("title") == "New Chat":
                try:
                    new_title = generate_ai_title(question).strip('"\'')
                    if new_title:
                        chat_data["title"] = new_title
                except Exception as ex:
                    print(f"Error generating AI title: {ex}")
            
            save_chat(chat_data)
        except Exception as e:
            print(f"Error saving chat in chat(): {e}")
    else:
        memory.add_user_message(
            SESSION_ID,
            question
        )

        memory.add_ai_message(
            SESSION_ID,
            response.content
        )

    return response.content


def chat_stream(question: str, chat_id: str | None = None) -> Iterator[str]:

    if chat_id:
        from services.history_service import load_chat
        try:
            chat_data = load_chat(chat_id)
            history = []
            for msg in chat_data.get("messages", []):
                if msg["role"] == "user":
                    history.append(HumanMessage(content=msg["content"]))
                else:
                    history.append(AIMessage(content=msg["content"]))
        except Exception as e:
            print(f"Error loading chat in chat_stream(): {e}")
            history = []
    else:
        history = memory.get_messages(SESSION_ID)

    history.append(
        HumanMessage(content=question)
    )

    full_response = ""

    for chunk in chat_model.stream(history):

        if hasattr(chunk, "content") and chunk.content:

            full_response += chunk.content

            yield chunk.content

    if chat_id:
        from services.history_service import load_chat, save_chat, generate_ai_title
        try:
            chat_data = load_chat(chat_id)
            chat_data["messages"].append({"role": "user", "content": question})
            chat_data["messages"].append({"role": "assistant", "content": full_response})
            
            # If the title is "New Chat", generate a smart title
            if chat_data.get("title") == "New Chat":
                try:
                    new_title = generate_ai_title(question).strip('"\'')
                    if new_title:
                        chat_data["title"] = new_title
                except Exception as ex:
                    print(f"Error generating AI title in stream: {ex}")
            
            save_chat(chat_data)
        except Exception as e:
            print(f"Error saving chat in chat_stream(): {e}")
    else:
        memory.add_user_message(
            SESSION_ID,
            question
        )

        memory.add_ai_message(
            SESSION_ID,
            full_response
        )
