import re
from strategies.base import ChunkingStrategy
class ParagraphChuncking(ChunkingStrategy):
    def __init__(self,chunk_sise):
        self.chunk_sise =chunk_sise


    def chunk(self, text):
        return text.split('\n\n')
    