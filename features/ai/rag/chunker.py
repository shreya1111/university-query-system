"""
Text Chunker — splits documents into overlapping chunks.
Swap splitter implementation for semantic chunking when ready.
"""
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

CHUNK_SIZE    = 1000
CHUNK_OVERLAP = 200


def split_documents(documents: list[Document]) -> list[Document]:
    """
    Split a list of Documents into smaller overlapping chunks.

    Args:
        documents: Raw LangChain Document objects from the loader.

    Returns:
        List of chunked Document objects.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_documents(documents)
