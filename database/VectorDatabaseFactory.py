from database.FaissDatabase import FaissDatabase
from database.ChromaDatabase import ChromaDatabase


class VectorDatabaseFactory:
    """Creates a VectorDatabase implementation from a backend name ("faiss" / "chroma")."""

    _backends = { "faiss": FaissDatabase, "chroma": ChromaDatabase}

    @staticmethod
    def create(name, embedding, **kwargs):
        # Look up the backend class by name and instantiate it with the embedding model.
        try:
            backend = VectorDatabaseFactory._backends[name.lower()]
        except KeyError:
            valid = ", ".join(VectorDatabaseFactory._backends)
            raise ValueError(f"Unknown vector database '{name}'. Choose one of: {valid}")
        return backend(embedding, **kwargs)
