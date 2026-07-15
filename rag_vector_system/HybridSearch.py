from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever

from embeddings.EmbeddingModel import EmbeddingModel
from database.VectorDatabaseFactory import VectorDatabaseFactory
from rag_vector_system.HybridSearchBase import HybridSearchBase

from rag_vector_system.ReRanker import ReRanker

class HybridSearch(HybridSearchBase):
    """Database-agnostic hybrid search: fuses BM25 (keyword) and vector retrieval.

    Works with any VectorDatabase (FAISS, Chroma, ...) because it only relies on
    the shared `get_documents()` and `as_retriever()` interface.
    """

    def __init__(self, vector_db, k=2, weights=(0.5, 0.5)):
        # Build a BM25 keyword retriever from the documents stored in the vector db.
        bm25 = BM25Retriever.from_documents(vector_db.get_documents())
        bm25.k = k

        # Wrap the vector store itself as a semantic retriever.
        vector = vector_db.as_retriever(search_kwargs={"k": k})

        # Fuse the two with reciprocal-rank fusion, weighted per retriever.
        self.ensemble = EnsembleRetriever(
            retrievers=[bm25, vector],
            weights=list(weights),
        )

    def search(self, query):
        # Return the merged, re-ranked list of documents for the query.
        return self.ensemble.invoke(query)


if __name__ == "__main__":
    emb = EmbeddingModel()

    # Swap "faiss" for "chroma" here and nothing else changes.
    db = VectorDatabaseFactory.create("faiss", emb)
    db.load()
    hybrid = HybridSearch(db, k=2)
    result = hybrid.search("What is AI?")
    reranked = ReRanker()
    res = reranked.rerank(query="What is AI?", documents=[doc.page_content for doc in result], top_k=3)
    print(res)
    # for doc in res:
    #     print(doc.page_content)
