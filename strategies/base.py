from abc import ABC, abstractmethod

class ChunkingStrategy(ABC):
    """Abstract base class defining the common interface every chunking strategy must implement."""
    
    @abstractmethod
    def chunk(self, text):
        # Split `text` into a list of chunks. Must be implemented by each subclass.
        pass;

    