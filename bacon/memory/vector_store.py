import chromadb
from chromadb.utils import embedding_functions

class VectorStore:
    def __init__(self, collection_name: str = "bacon_memory"):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=embedding_functions.DefaultEmbeddingFunction()
        )

    def add(self, documents: list, metadatas: list, ids: list):
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def query(self, query_texts: list, n_results: int = 5):
        return self.collection.query(
            query_texts=query_texts,
            n_results=n_results
        )
