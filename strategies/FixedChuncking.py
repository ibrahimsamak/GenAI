from strategies.base import ChunkingStrategy


class FixedChuncking(ChunkingStrategy):
    def __init__(self, chunk_size):
        self.chunk_size = chunk_size

    def chunk(self, text):
        words = text.split()
        chunks = []
        for i in range(0, len(words), self.chunk_size):
            chunks.append(" ".join(words[i:i+self.chunk_size]))
        return chunks

    def fixed_with_overlap(self, text, overlap=50):
        words = text.split()
        chunks = []
        start = 0
        while start < len(words):
            end = start + self.chunk_size
            chunks.append(" ".join(words[start:end]))
            start += self.chunk_size - overlap

        return chunks