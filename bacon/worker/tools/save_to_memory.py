from bacon.memory.vector_store import VectorStore
import uuid

def save_to_memory(document: str, metadata: dict = None):
    """
    Saves a document to the vector store.
    """
    vector_store = VectorStore()
    vector_store.add(
        documents=[document],
        metadatas=[metadata] if metadata else [{}],
        ids=[str(uuid.uuid4())]
    )
    return "Document saved to memory."
