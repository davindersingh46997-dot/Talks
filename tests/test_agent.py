from langchain_openai import ChatOpenAI
from langchain_protocol import TypedDict
from langgraph.graph import StateGraph,START,END
from pydantic import BaseModel, Field

from dotenv import load_dotenv
from tavily import TavilyClient
import os
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

def web_search(query: str) -> str:
    """
    Perform a web search using Tavily API and return the results.
    """
    if os.get_environ("TAVILY_API_KEY") is None:
        raise ValueError("TAVILY_API_KEY is not set in the environment variables.")

    tavily_client = TavilyClient(api_key=os.get_environ("TAVILY_API_KEY"))
    response = tavily_client.search(query)

    return response


class AgentState(TypedDict):

    query: str

    results: list[dict]

    answer: str

    next_search_query: str

    iteration: int

    finished: bool


llm = ChatOpenAI(
    model=os.getenv(
        "OPENROUTER_MODEL",
        "nvidia/nemotron-3.5-embed-1b:free"
    ),
    temperature=0,
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    max_retries=2,
    timeout=60
)


class AgentDecision(BaseModel):
    action: str = Field(..., description="The action to take: 'search', 'answer', or 'finish'.")
    search_query: str = Field(None, description="The query to use for the next web search, if action is 'search'.")
    answer: str = Field(None, description="The answer to return, if action is 'answer'.")


decision_llm = llm.with_structured_output(AgentDecision)


def agent_node(state: AgentState) -> AgentState:
    """
    The agent node that decides the next action based on the current state.
    """

    print("\n========== AGENT THINKING ==========")

    response = decision_llm.invoke([
         SystemMessage(content="""
        You are an autonomous web research agent.

        Your responsibility is to research the user's question.

        Examine the available search results.

        Decide whether:

        1. SEARCH:
           More information is required.
           Generate a specific and useful search query.

        2. FINISH:
           Enough information has been collected.
           Generate a clear and accurate final answer.

        Rules:
        - Use the collected evidence.
        - Never invent facts.
        - Prefer relevant and credible sources.
        - Include source URLs in the final answer.
        - Do not repeat previous searches unnecessarily.
        """),

        HumanMessage(content=f"""
        Research question:
        {state['query']}

        Search results:
        {state['results']}

        Current iteration:
        {state['iteration']}
        """)
    ])

    print("Agent Decision:", response.action)

    if response.action.upper() == "SEARCH":
        state['next_search_query'] = response.search_query
        state['finished'] = False

    elif response.action.upper() == "ANSWER":
        state['answer'] = response.answer
        state['finished'] = True

    elif response.action.upper() == "FINISH":
        state['finished'] = True   

    else:
        raise ValueError(f"Invalid action: {response.action}")


def search_node(state: AgentState):

    print("\n========== SEARCH NODE ==========")

    query = (
        state["next_search_query"]
        or state["query"]
    )

    results = web_search(query)

    return {
        "results": state["results"] + results,
        "iteration": state["iteration"] + 1,
        "next_search_query": ""
    }


MAX_ITERATIONS = 5

def route_agent(state: AgentState):

    if state["finished"]:
        return "end"

    if state["iteration"] >= MAX_ITERATIONS:

        print("\nMaximum search iterations reached.")

        return "end"

    return "search"


graph = StateGraph(AgentState)

graph.add_node("agent", agent_node)

graph.add_node("search", search_node)


graph.add_edge(START, "search")

graph.add_edge("search", "agent")

graph.add_conditional_edges(
    "agent",
    route_agent,
    {
        "search": "search",
        "end": END
    }
)

research_agent = graph.compile()

def run_agent(query: str) -> str:
    """
    Run the research agent with the given query and return the final answer.
    """

    return research_agent.invoke(
        {
            "query": query,
            "results": [],
            "answer": "",
            "next_search_query": "",
            "iteration": 0,
            "finished": False
        }
    )