from langchain_text_splitters import RecursiveCharacterTextSplitter
from strategies.base import ChunkingStrategy

class RecursiveChunking(ChunkingStrategy):
    def __init__(self,chunk_size, overlap):
        self.chunk_size = chunk_size
        self.overlap = overlap


    def chunk(self, text):
        spliter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.overlap)
        return spliter.split_text(text)