from strategies.base import ChunkingStrategy


class SlidingWindowChunking(ChunkingStrategy):
    """Produces overlapping word windows so context is retained across chunk edges."""

    def __init__(self, chunk_size, overlap):
        # chunk_size: words per window; overlap: words shared between adjacent windows.
        self.chunk_size = chunk_size
        self.overlap = overlap


    def chunk(self, text):
        # Slide a window of `chunk_size` words forward by (chunk_size - overlap) each step.
        words = text.split()
        chunks = []
        step = self.chunk_size - self.overlap
        for i in range(0, len(words), step):
            chunk = words[i:i+self.chunk_size]
            if chunk:  # skip empty trailing slices
                chunks.append(" ".join(chunk))

        return chunks

    