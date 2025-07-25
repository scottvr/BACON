from bacon.memory.vector_store import VectorStore

def retriever(query: str):
    """
    Retrieves information from the vector store.
    """
    vector_store = VectorStore()
    results = vector_store.query(query_texts=[query])
    return {"retriever_results": results}
