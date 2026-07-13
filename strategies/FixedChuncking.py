from strategies.base import ChunkingStrategy


class FixedChuncking(ChunkingStrategy):
    """Splits text into fixed-size chunks measured in number of words."""

    def __init__(self, chunk_size):
        # Number of words per chunk.
        self.chunk_size = chunk_size

    def chunk(self, text):
        # Split text into non-overlapping chunks of `chunk_size` words each.
        words = text.split()
        chunks = []
        for i in range(0, len(words), self.chunk_size):
            chunks.append(" ".join(words[i:i+self.chunk_size]))
        return chunks

    def fixed_with_overlap(self, text, overlap=50):
        # Like chunk(), but consecutive chunks share `overlap` words to preserve context.
        words = text.split()
        chunks = []
        start = 0
        while start < len(words):
            end = start + self.chunk_size
            chunks.append(" ".join(words[start:end]))
            # Advance by chunk_size minus the overlap so windows overlap by `overlap` words.
            start += self.chunk_size - overlap

        return chunks