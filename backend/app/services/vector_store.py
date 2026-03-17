# FAISS vector store – placeholder
class VectorStore:
    def add(self, embedding: list, metadata: dict):
        raise NotImplementedError

    def search(self, query_embedding: list, top_k: int = 5) -> list:
        raise NotImplementedError
