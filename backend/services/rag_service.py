from backend.rag import (
    loader,
    splitter,
    vector_store
)
from backend.rag.crag import retrieve_with_correction

def rag_service(file_path: str):

    documents = loader.load_document(file_path)

    splitted_docs = splitter.split_documents(documents)

    vector_store.add_documents(splitted_docs)

    return {
        "message": "Document processed successfully",
        "filename": file_path
    }


def get_documents(query: str, k: int = 4):
    """
    Retrieve and correct raw document results for a given query.
    """
    return retrieve_with_correction(query, k=k)


def format_documents(documents) -> str:
    """
    Format a list of documents into clean context text.
    """
    if not documents:
        return ""

    formatted_parts = []
    for doc in documents:
        if hasattr(doc, "page_content") and doc.page_content:
            content = doc.page_content.strip()
            source = ""
            if hasattr(doc, "metadata") and isinstance(doc.metadata, dict):
                source = doc.metadata.get("source", "")
            if source:
                formatted_parts.append(f"[Source: {source}]\n{content}")
            else:
                formatted_parts.append(content)
        elif isinstance(doc, str) and doc.strip():
            formatted_parts.append(doc.strip())

    return "\n\n".join(formatted_parts)


def get_content(query: str, k: int = 4) -> str:
    """
    Retrieve and format relevant context as clean text for the LLM.
    """
    documents = get_documents(query, k=k)
    return format_documents(documents)