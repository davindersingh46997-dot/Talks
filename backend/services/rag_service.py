from backend.rag import (
    embedding,
    loader,
    retreiver,
    splitter,
    vector_store
)

def Rag_service(file_path: str):

    document = loader(file_path)

    splitted_docs = splitter.split_text(document)

    embeds = embedding.Embeddings(splitted_docs)

    store = vector_store.add_documents(embeds)


def get_content():

    retrival_text = retreiver.get_retriever(k : int = 128)

    return retrival_text

