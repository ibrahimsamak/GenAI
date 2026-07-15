from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from database.VectorDatabase import VectorDatabase

class FaissDatabase(VectorDatabase):
    def __init__(self, embedding, persist_directory="vectorstores/faiss_store"):
        self.embedding = embedding
        self.persist_directory = persist_directory
        self.db = None

    def create(self, texts):
        docs = [Document(page_content=t) for t in texts]
        self.db = FAISS.from_documents(docs, self.embedding.embedding)

    def save(self):
        # Persist the in-memory FAISS index to disk (creates the folder if needed).
        self.db.save_local(self.persist_directory)

    def load(self):
        # Rebuild the FAISS index from the saved files in persist_directory.
        self.db = FAISS.load_local(self.persist_directory, self.embedding.embedding, allow_dangerous_deserialization=True)

    def similarity_search(self, query, k=3):
        return self.db.similarity_search(query, k=k)

    def get_documents(self):
        # FAISS keeps its documents in an in-memory docstore keyed by id.
        return list(self.db.docstore._dict.values())



# if __name__ == "__main__":
#     texts = ["Python is used for AI."]
#     app = EmbeddingModel()
#     db = FaissDatabase(app)
#     db.create(texts)
#     db.save()                       # writes vectorstores/faiss_store/{index.faiss,index.pkl}
#     results = db.similarity_search("Python")
#     print(results)
