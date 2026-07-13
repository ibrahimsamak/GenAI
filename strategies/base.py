from abc import ABC, abstractmethod

class ChunkingStrategy(ABC):

    @abstractmethod
    def chunk(self, text):
        pass;

    