import re
from strategies.base import ChunkingStrategy
class ParagraphChuncking(ChunkingStrategy):
    """Splits text into paragraphs using blank-line boundaries."""

    def __init__(self, chunk_sise):
        # Reserved size hint (not used by the current split logic).
        self.chunk_sise = chunk_sise


    def chunk(self, text):
        # Split on blank lines so each paragraph becomes its own chunk.
        return text.split('\n\n')
    