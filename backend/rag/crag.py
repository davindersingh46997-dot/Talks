from collections.abc import Callable, Sequence
from typing import Any


Document = Any
Retriever = Callable[[str], Sequence[Document]]
Grader = Callable[[str, Document], bool]
Rewriter = Callable[[str], str]
WebSearch = Callable[[str], Sequence[Document]]


def _document_text(document: Document) -> str:
    if isinstance(document, str):
        return document.strip()
    return str(getattr(document, "page_content", "")).strip()


def _model_text(response: Any) -> str:
    content = getattr(response, "content", response)
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        return " ".join(
            item.get("text", "") if isinstance(item, dict) else str(item)
            for item in content
        ).strip()
    return str(content).strip()


def _invoke_model(system_prompt: str, user_prompt: str) -> str:
    from langchain_core.messages import HumanMessage, SystemMessage

    from backend.core.llm import chat_model

    response = chat_model.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ])
    return _model_text(response)


def grade_document(query: str, document: Document) -> bool:
    text = _document_text(document)
    if not text:
        return False

    answer = _invoke_model(
        "You are a relevance grader. Decide whether the evidence directly helps answer the question. "
        "Reply with only YES or NO.",
        f"Question:\n{query}\n\nEvidence:\n{text[:5000]}",
    )
    return answer.upper().strip(" .!\n\t") == "YES"


def rewrite_query(query: str) -> str:
    rewritten = _invoke_model(
        "Rewrite the user's question as one concise search query that is likely to find direct evidence. "
        "Return only the rewritten query.",
        query,
    )
    return rewritten or query


def _default_retriever(k: int) -> Retriever:
    from backend.rag.retreiver import get_retriever

    retriever = get_retriever(k=k)
    return retriever.invoke


def _default_web_search(query: str) -> Sequence[Document]:
    from backend.core.research import search_web_documents

    return search_web_documents(query)


def retrieve_with_correction(
    query: str,
    k: int = 4,
    *,
    retrieve: Retriever | None = None,
    grade: Grader | None = None,
    rewrite: Rewriter | None = None,
    web_search: WebSearch | None = None,
) -> list[Document]:
    """Retrieve relevant local evidence, retry once, then fall back to web search."""
    query = query.strip()
    if not query:
        return []

    if retrieve is None:
        try:
            retrieve = _default_retriever(k)
        except Exception:
            retrieve = lambda _: []
    grade = grade or grade_document
    rewrite = rewrite or rewrite_query
    web_search = web_search or _default_web_search

    def relevant_documents(search_query: str, documents: Sequence[Document]) -> list[Document]:
        relevant = []
        for document in documents or []:
            try:
                if grade(search_query, document):
                    relevant.append(document)
            except Exception:
                continue
        return relevant

    try:
        local_documents = list(retrieve(query) or [])
    except Exception:
        local_documents = []

    accepted = relevant_documents(query, local_documents)
    if accepted:
        return accepted

    try:
        rewritten_query = rewrite(query).strip() or query
    except Exception:
        rewritten_query = query

    try:
        retry_documents = list(retrieve(rewritten_query) or [])
    except Exception:
        retry_documents = []

    accepted = relevant_documents(query, retry_documents)
    if accepted:
        return accepted

    try:
        web_documents = list(web_search(rewritten_query) or [])
    except Exception:
        return []

    return relevant_documents(query, web_documents)