import re

from backend.services.rag_service import rag_service, get_content


# 1. Add the PDF to the vector database
rag_service(
    r"C:\Users\Rohit Sharma\Downloads\1406.2661v1.pdf"
)


# 2. Ask a question
text = get_content("what is the GANs?")


# 3. Clean the RAG output
def format_rag_output(text):

    # Remove leading/trailing whitespace
    text = text.strip()

    # Convert multiple newlines into a temporary separator
    text = re.sub(r'\n+', '\n', text)

    # Remove excessive spaces
    text = re.sub(r'[ \t]+', ' ', text)

    # Remove spaces before punctuation
    text = re.sub(r'\s+([,.!?;:])', r'\1', text)

    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # Group sentences into paragraphs
    paragraphs = []

    current_paragraph = []

    for sentence in sentences:

        current_paragraph.append(sentence)

        # Create a paragraph after ~4 sentences
        if len(current_paragraph) >= 4:
            paragraphs.append(" ".join(current_paragraph))
            current_paragraph = []

    # Add remaining sentences
    if current_paragraph:
        paragraphs.append(" ".join(current_paragraph))

    return "\n\n".join(paragraphs)


formatted_text = format_rag_output(text)

print("\n" + "=" * 80)
print("RAG ANSWER")
print("=" * 80)

print(formatted_text)

print("=" * 80)