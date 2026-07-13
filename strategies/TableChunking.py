import pdfplumber
from strategies.base import ChunkingStrategy

class TableChunking(ChunkingStrategy):
    def __init__(self):
        pass;

    def chunk(self,text):
        pass;

    def chunk_tables(self, path):
        tables = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()

        return tables;
