

class ChunkProcessor:
    """Strategy-pattern context: holds a chunking strategy and delegates work to it."""

    def __init__(self, strategy):
        # Store the chunking strategy to use (any ChunkingStrategy subclass).
        self.strategy = strategy

    def set_strategy(self, strategy):
        # Swap the active chunking strategy at runtime.
        self.strategy = strategy

    def process(self, text):
        # Delegate chunking to the current strategy and return its chunks.
        return self.strategy.chunk(text)
