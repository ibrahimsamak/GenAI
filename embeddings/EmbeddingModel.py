from langchain_huggingface import HuggingFaceEmbeddings

class EmbeddingModel:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.embedding = HuggingFaceEmbeddings(model_name=model_name)

    def embed_document(self, document):
        return self.embedding.embed_documents(document)
    
    def embed_query(self,text):
        return self.embedding.embed_query(text)
    
