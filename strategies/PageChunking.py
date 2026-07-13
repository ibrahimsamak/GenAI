import fitz
from strategies.base import ChunkingStrategy

class PageChunking(ChunkingStrategy):
    """Treats each PDF page as a single chunk (operates on a file path, not text)."""

    def __init__(self, path):
        # Path to the PDF file to read pages from.
        self.path = path

    def chunk(self, text):
        # Open the PDF with PyMuPDF and return one chunk of text per page. `text` is ignored.
        pdfs = fitz.open(self.path)
        chunks = []
        for page in pdfs:
            chunks.append(page.get_text())
        return chunks