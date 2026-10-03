from pathlib import Path
from langchain_chroma import Chroma

from backend.rag.embedding import get_embedding_model

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_DIRECTORY = str(BASE_DIR / "vector_db")

embedding_model = get_embedding_model()


def get_vector_store():
    """
    Open or create the Chroma database.
    """

    return Chroma(
        persist_directory=DB_DIRECTORY,
        embedding_function=embedding_model
    )


def add_documents(chunks):
    """
    Add chunks to the vector database.
    """

    db = get_vector_store()

    db.add_documents(chunks)

    return db