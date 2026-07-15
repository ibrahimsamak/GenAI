import os
import glob
import pdfplumber
from llama_index.core import Document, VectorStoreIndex
from llama_index.core import load_index_from_storage
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
from llama_index.core import StorageContext

class llamaIndex:
    def __init__(self, folder='data'):
        Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
        Settings.llm = HuggingFaceInferenceAPI(model_name="meta-llama/Llama-3.1-8B-Instruct", token=os.getenv("HF_KEY"), provider="auto")
        self.documents = self._load_documents(folder)
        self.index = VectorStoreIndex.from_documents(self.documents)

    def _load_documents(self, folder):
        # LlamaIndex's default PDF reader (pypdf) garbles this PDF's fonts, so extract
        # clean text with pdfplumber and wrap each file in a LlamaIndex Document.
        documents = []
        for path in glob.glob(os.path.join(folder, "*.pdf")):
            with pdfplumber.open(path) as pdf:
                text = "\n".join(page.extract_text() or "" for page in pdf.pages)
            documents.append(Document(text=text, metadata={"file_name": os.path.basename(path)}))
        return documents

    def save(self, persist_dir='./vectorstores/llamaindex'):
        self.index.storage_context.persist(persist_dir)
    
    def load(self, persist_dir='./vectorstores/llamaindex'):
        storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
        self.index = load_index_from_storage(storage_context)
    
    def search(self, query):
        query_engine = self.index.as_query_engine()
        result = query_engine.query(query)
        return result



if __name__ == "__main__":
    app = llamaIndex()
    app.save()
    res = app.search('what is the duration for the first course?')
    print(res)
