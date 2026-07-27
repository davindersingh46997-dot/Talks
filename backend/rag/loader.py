from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
    Docx2txtLoader,
)

SUPPORTED_EXTENSIONS = {
    ".pdf": PyPDFLoader,
    ".txt": TextLoader,
    ".csv": CSVLoader,
    ".docx": Docx2txtLoader,
}


def load_document(file_path: str):
    """
    Load a single document and return a list of LangChain Document objects.
    """

    path = Path(file_path)

    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {extension}")

    loader_class = SUPPORTED_EXTENSIONS[extension]

    loader = loader_class(str(path))

    return loader.load()