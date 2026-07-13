import fitz
from strategies.base import ChunkingStrategy

class PageChunking(ChunkingStrategy):
    def __init__(self, path):
        self.path = path

    def chunk(self, text):
        pdfs = fitz.open(self.path)
        chunks = []
        for page in pdfs:
            chunks.append(page.get_text())
        return chunks