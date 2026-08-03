from langgraph.graph import StateGraph
from langgraph.graph import START, END
from langgraph.graph.message import add_messages

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
)

from typing import TypedDict,Annotated,Iterator

from backend.core.llm import chat_model

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