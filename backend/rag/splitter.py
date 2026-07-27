from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    separators=["\n\n", "\n", " ", ""]
)


def split_text(text: str) -> list[str]:
    """
    Splits the input text into chunks using the RecursiveCharacterTextSplitter.

    Args:
        text (str): The input text to be split.

    Returns:
        list[str]: A list of text chunks.
    """
    return text_splitter.split_text(text)

