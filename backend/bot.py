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

def chat(question: str):

    inputs = {
        "messages": [
            HumanMessage(
                content=question
            )
        ]
    }

    result = graph.invoke(inputs)

    return result["messages"][-1].content


def chat_stream(question: str) -> Iterator[str]:
    """
    Stream the response token-by-token (or chunk-by-chunk),
    depending on what the model wrapper provides.
    """

    messages = [
        HumanMessage(content=question)
    ]

    for chunk in chat_model.stream(messages):

        if hasattr(chunk, "content") and chunk.content:
            yield chunk.content
