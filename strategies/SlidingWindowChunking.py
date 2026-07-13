from strategies.base import ChunkingStrategy


class SlidingWindowChunking(ChunkingStrategy):
    
    def __init__(self, chunk_size, overlap):
        self.chunk_size = chunk_size
        self.overlap = overlap


    def chunk(self, text):
        words = text.split()
        chunks = []
        step = self.chunk_size - self.overlap
        for i in range(0, len(words), step):
            chunk = words[i:i+self.chunk_size]
            if chunk:
                chunks.append(" ".join(chunk))

        return chunks

    