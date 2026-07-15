from abc import ABC, abstractmethod


class HybridSearchBase(ABC):
    """Interface for hybrid (keyword + vector) search implementations."""

    @abstractmethod
    def search(self, query):
        # Return a ranked list of documents combining keyword and vector relevance.
        pass
