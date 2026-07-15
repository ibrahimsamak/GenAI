import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from embeddings.EmbeddingModel import EmbeddingModel
from database.VectorDatabaseFactory import VectorDatabaseFactory

SYSTEM_PROMPT_TEMPLATE = """
Given the following Context and a Input question, Answer question from the context only if you don't no say this is out of my scope (PDF).
Context:
{context}
Input: 
{question}
"""


class ChatEngine:
    """Pure retrieval-augmented chat logic (no UI).

    Loads the chosen vector database once at construction, then answers questions
    by retrieving relevant chunks and asking the LLM to respond using them.
    """

    def __init__(self, backend="faiss", model="gpt-4.1-nano", k=3):
        load_dotenv(override=True)

        # Build the vector store once (embedding model + factory + load from disk).
        db = VectorDatabaseFactory.create(backend, EmbeddingModel())
        db.load()
        self.retriever = db.as_retriever(search_kwargs={"k": k})

        # Prefer the standard OPENAI_API_KEY, fall back to the legacy .env name.
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPEN_AI_KEy")
        self.llm = ChatOpenAI(temperature=0, model=model, api_key=api_key)

    def answer(self, question):
        # Retrieve context, prompt the LLM, and return (answer_text, retrieved_docs).
        docs = self.retriever.invoke(question)
        context = "\n\n".join(doc.page_content for doc in docs)
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(context=context, question=question)
        response = self.llm.invoke(
            [SystemMessage(content=system_prompt), HumanMessage(content=question)]
        )
        return response.content, docs
