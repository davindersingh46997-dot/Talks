from langchain_core.messages import HumanMessage, AIMessage
from requests import Session
from backend.api.dependencies import get_current_user
from backend.core.graph import graph

from backend.core.llm import chat_model

from backend.core.database import SessionLocal

from typing import Iterator

from backend.memory.short_term import ShortTermMemory

from backend.api.dependencies import get_current_user

from backend.services.history_service import (
    load_chat,
    load_chat_history,
    save_user_message,
    save_ai_message,
    generate_ai_title,
    update_chat_title,
)


memory = ShortTermMemory(max_messages=5)

SESSION_ID = "default"

db = SessionLocal()

def chat(question: str, db : Session, user_id: int, chat_id: str | None = None):

    if chat_id:
        from backend.services.history_service import load_chat
        try:
            chat_data = load_chat(db=db, chat_id=chat_id, user_id=user_id)
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
        from backend.services.history_service import (
            load_chat,
            save_chat,
            generate_ai_title,
        )

    try:
        chat_data = load_chat(
            db=db,
            chat_id=chat_id,
            user_id=user_id,
        )

        print("CHAT DATA BEFORE TITLE:", chat_data)
        print("CURRENT TITLE:", chat_data.get("title"))

        chat_data["messages"].append({
            "role": "user",
            "content": question,
        })

        chat_data["messages"].append({
            "role": "assistant",
            "content": response.content,
        })

        if chat_data.get("title") == "New Chat":
            print("Generating AI title...")

            try:
                new_title = generate_ai_title(question)

                print("RAW GENERATED TITLE:", repr(new_title))

                if new_title:
                    new_title = new_title.strip().strip("\"'")

                    print("CLEAN TITLE:", repr(new_title))

                    chat_data["title"] = new_title

            except Exception as ex:
                print(f"Error generating AI title: {ex}")

        print("CHAT DATA BEFORE SAVE:", chat_data)

        save_chat(db, chat_id, chat_data, user_id)

        print("Chat saved successfully.")

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


def chat_stream(
    question: str,
    db: Session,
    user_id: int,
    chat_id: int | None = None,
):
    print("\n========== CHAT STREAM ==========")
    print("USER ID:", user_id)
    print("CHAT ID:", chat_id)
    print("QUESTION:", question)

    history = []

    # ---------------------------------
    # Make sure we have a real chat
    # ---------------------------------

    if chat_id is None:
        print("⚠️ No chat_id received!")
        raise ValueError("chat_id is required for database chat")

    # ---------------------------------
    # Load previous chat history
    # ---------------------------------

    try:
        messages = load_chat_history(
            db=db,
            chat_id=chat_id,
            user_id=user_id,
        )

        print("Previous messages:", len(messages))

        for msg in messages:
            if msg.role == "user":
                history.append(
                    HumanMessage(content=msg.content)
                )

            elif msg.role == "assistant":
                history.append(
                    AIMessage(content=msg.content)
                )

    except Exception as e:
        print(f"❌ Error loading chat history: {e}")
        raise

    # ---------------------------------
    # Add current user message
    # ---------------------------------

    history.append(
        HumanMessage(content=question)
    )

    # ---------------------------------
    # Save user message
    # ---------------------------------

    try:
        save_user_message(
            db=db,
            chat_id=chat_id,
            content=question,
        )

        print("✅ User message saved")

    except Exception as e:
        print(f"❌ Error saving user message: {e}")
        raise

    # ---------------------------------
    # Generate AI response
    # ---------------------------------

    full_response = ""

    try:
        for chunk in chat_model.stream(history):

            if hasattr(chunk, "content") and chunk.content:

                full_response += chunk.content

                yield chunk.content

    except Exception as e:
        print(f"❌ Model streaming error: {e}")
        raise

    print("AI RESPONSE:", full_response)

    # ---------------------------------
    # Save assistant response
    # ---------------------------------

    try:
        save_ai_message(
            db=db,
            chat_id=chat_id,
            content=full_response,
        )

        print("✅ AI message saved")

    except Exception as e:
        print(f"❌ Error saving AI message: {e}")
        raise

    # ---------------------------------
    # Generate title
    # ---------------------------------

    try:
        chat = load_chat(
            db=db,
            chat_id=chat_id,
            user_id=user_id,
        )

        if chat is None:
            print("❌ Chat not found:", chat_id)
            return

        print("CURRENT TITLE:", chat.title)

        if chat.title == "New Chat":

            print("🤖 Generating AI title...")

            new_title = generate_ai_title(question)

            new_title = new_title.strip().strip('"').strip("'")

            print("GENERATED TITLE:", new_title)

            if new_title:

                update_chat_title(
                    db=db,
                    chat_id=chat_id,
                    user_id=user_id,
                    new_title=new_title,
                )

                print("✅ Chat title updated")

    except Exception as e:
        print(f"❌ Title generation error: {e}")

