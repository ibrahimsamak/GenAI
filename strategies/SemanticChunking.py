# from langchain_experimental.text_splitter import SemanticChunker
# from langchain_openai import OpenAIEmbeddings
# from strategies.base import ChunkingStrategy

# class SemanticChunking(ChunkingStrategy):
#     def __init__(self):
#         pass

#     def chunk(self, text):
#         splitter = SemanticChunker(OpenAIEmbeddings())
#         chunks = splitter.create_documents([text])
#         return chunks