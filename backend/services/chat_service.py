from langchain_core.messages import HumanMessage, AIMessage
from core.graph import graph

from core.llm import chat_model

from typing import Iterator

from memory.short_term import ShortTermMemory

memory = ShortTermMemory(max_messages=20)

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
