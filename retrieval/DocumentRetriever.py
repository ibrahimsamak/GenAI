 
from embeddings.EmbeddingModel import EmbeddingModel
from database.ChromaDatabase import ChromaDatabase


class DocumentRetriever:
    def __init__(self, vector_db, k=3):
         self.retriever = vector_db.db.as_retriever(search_kwargs={"k":k})
        
    def retrieve(self, query):
         return self.retriever.invoke(query)

# if __name__ == "__main__":
#     texts = ["Python is used for AI."]
#     embd = EmbeddingModel()
#     db = ChromaDatabase(embd) 
#     db.load()
#     app = DocumentRetriever(vector_db=db,k=3)
#     result = app.retrieve('Artificial Intelligence')
#     print(result)
#     # db.create(texts)
#     # result = db.similarity_search('Artificial Intelligence')
#     # print(result)