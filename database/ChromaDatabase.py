from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from embeddings.EmbeddingModel import EmbeddingModel

class ChromaDatabase:
    def __init__(self, embedding, persist_directory="vectorstores/chroma_store"):
        self.embedding = embedding
        self.persist_directory = persist_directory
        self.db = None

    def create(self,texts):
        docs = [Document(page_content=t) for t in texts]
        self.db = Chroma.from_documents(docs, self.embedding.embedding,  persist_directory=self.persist_directory)
        
    def load(self):
        self.db = Chroma(persist_directory=self.persist_directory, embedding_function=self.embedding.embedding)
    
    def similarity_search(self, query, k=3):
        return self.db.similarity_search(query, k=k)
    
# if __name__ == "__main__":
#     texts = ["Python is used for AI."]
#     embd = EmbeddingModel()
#     db = ChromaDatabase(embd)
#     db.create(texts)
#     result = db.similarity_search('Artificial Intelligence')
#     print(result)