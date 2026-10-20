from backend.rag.vector_store import get_vector_store

def get_retriever(k: int = 4):
    """
    Returns a retriever that fetches the top-k most relevant chunks.
    """
    db = get_vector_store()
    
    return db.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": k
        }
    )