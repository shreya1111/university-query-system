"""
Retriever — fetches top-k relevant chunks from ChromaDB.
Change k or search_type here to tune retrieval behaviour.
"""
from langchain_core.documents import Document
from features.ai.rag.vectorstore import load_vectorstore

TOP_K = 5


def retrieve_documents(query: str) -> list[Document]:
    """
    Retrieve the most relevant document chunks for a query.

    Args:
        query: User question string.

    Returns:
        List of up to TOP_K relevant Document chunks.
    """
    vs = load_vectorstore()
    retriever = vs.as_retriever(
        search_type="similarity",
        search_kwargs={"k": TOP_K},
    )
    return retriever.invoke(query)
