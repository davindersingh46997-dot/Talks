import os
from typing import Annotated, Literal

from langchain.tools import InjectedToolArg, tool


def _get_tavily_client():
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return None

    from tavily import TavilyClient

    return TavilyClient(api_key=api_key)


def fetch_webpage_content(url: str, timeout: float = 10.0) -> str:
    """Fetch webpage and convert HTML to markdown."""
    import httpx
    from markdownify import markdownify

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        response = httpx.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return markdownify(response.text)
    except Exception as e:
        return f"Error fetching {url}: {e!s}"


def search_web_documents(query: str, max_results: int = 4):
    """Return Tavily search snippets as LangChain documents when configured."""
    client = _get_tavily_client()
    if client is None:
        return []

    from langchain_core.documents import Document

    results = client.search(query, max_results=max_results, topic="general")
    documents = []
    for result in results.get("results", []):
        content = result.get("content", "").strip()
        title = result.get("title", "").strip()
        url = result.get("url", "")
        if content or title:
            documents.append(Document(
                page_content=f"{title}\n{content}".strip(),
                metadata={"source": url, "title": title},
            ))
    return documents


@tool(parse_docstring=True)
def tavily_search(
    query: str,
    max_results: Annotated[int, InjectedToolArg] = 1,
    topic: Annotated[
        Literal["general", "news", "finance"], InjectedToolArg
    ] = "general",
) -> str:
    """Search the web for information on a given query.

    Uses Tavily to discover relevant URLs, then fetches and returns full webpage content as markdown.

    Args:
        query: Search query to execute
        max_results: Maximum number of results to return (default: 1)
        topic: Topic filter - 'general', 'news', or 'finance' (default: 'general')

    Returns:
        Formatted search results with full webpage content
    """
    client = _get_tavily_client()
    if client is None:
        return "Web search unavailable: TAVILY_API_KEY is not configured."

    search_results = client.search(
        query,
        max_results=max_results,
        topic=topic,
    )
    
    result_texts = []
    for result in search_results.get("results", []):
        url = result["url"]
        title = result["title"]
        content = fetch_webpage_content(url)
        result_texts.append(f"## {title}\n**URL:** {url}\n\n{content}\n---")

    return f"Found {len(result_texts)} result(s) for '{query}':\n\n" + "\n".join(
        result_texts
    )

