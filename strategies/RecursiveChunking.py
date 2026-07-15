from langchain_text_splitters import RecursiveCharacterTextSplitter
from strategies.base import ChunkingStrategy

class RecursiveChunking(ChunkingStrategy):
    """Wraps LangChain's RecursiveCharacterTextSplitter for character-based splitting."""

    def __init__(self, chunk_size, overlap):
        # chunk_size: max characters per chunk; overlap: characters shared between chunks.
        self.chunk_size = chunk_size
        self.overlap = overlap


    def chunk(self, text):
        # Recursively split on a hierarchy of separators to keep chunks near chunk_size.
        spliter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.overlap)
        return spliter.split_documents(text)