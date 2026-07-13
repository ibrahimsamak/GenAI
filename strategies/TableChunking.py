import pdfplumber
from strategies.base import ChunkingStrategy

class TableChunking(ChunkingStrategy):
    """Extracts tabular data from a PDF; real work happens in chunk_tables()."""

    def __init__(self):
        # No configuration needed for table extraction.
        pass;

    def chunk(self,text):
        # No-op: this strategy works on a file path via chunk_tables(), not on raw text.
        pass;

    def chunk_tables(self, path):
        # Open the PDF and collect tables (as row/cell lists) from its pages.
        tables = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()

        return tables;
