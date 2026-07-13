import nltk
import ssl
import re
from nltk.tokenize import sent_tokenize
from strategies.base import ChunkingStrategy

class SentenceChunking(ChunkingStrategy):
    def __init__(self, chunk_size, n):
        self.chunk_size = chunk_size
        self.n = n
        # try:
        #     _create_unverified_https_context = ssl._create_unverified_context
        # except AttributeError:
        #     pass
        # else:
        #     ssl._create_default_https_context = _create_unverified_https_context
        # nltk.download('punkt') 

    def chunk(self, text):
        sentences = sent_tokenize(text)
        chunks = []
        for i in range(0, len(sentences), self.n):
            chunks.append(" ".join(sentences[i:i+self.n]))
        
        return chunks

    def chunk_with_regix(self, text):
        sentences = re.split(r'(?<=[.!?])\s+', text)
        # chunks = []
        # for i in sentences:
        #     chunks.append(i)
        return sentences

