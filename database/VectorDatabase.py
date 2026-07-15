from abc import ABC, abstractmethod


class VectorDatabase(ABC):
    """Common interface every vector database (FAISS, Chroma, ...) must implement.

    Subclasses wrap an underlying LangChain vector store in `self.db`, so the
    concrete `as_retriever()` here works for all of them.
    """

    @abstractmethod
    def create(self, texts):
        # Build the vector store from a list of raw text strings.
        pass

    @abstractmethod
    def load(self):
        # Load a previously persisted vector store from disk into self.db.
        pass

    @abstractmethod
    def similarity_search(self, query, k=3):
        # Return the k most similar documents to `query`.
        pass

    @abstractmethod
    def get_documents(self):
        # Return all stored documents as LangChain Document objects (used to seed BM25).
        pass

    def as_retriever(self, **kwargs):
        # Expose the underlying store as a LangChain retriever (shared by all backends).
        return self.db.as_retriever(**kwargs)
