
import pdfplumber
from strategies.FixedChuncking import FixedChuncking
from strategies.SentenceChunking import SentenceChunking
from strategies.ParagraphChuncking import ParagraphChuncking
from strategies.SlidingWindowChunking import SlidingWindowChunking
from strategies.PageChunking import PageChunking
from strategies.RecursiveChunking import RecursiveChunking
# from strategies.SemanticChunking import SemanticChunking
from strategies.TableChunking import TableChunking
from Processor import ChunkProcessor
from database.ChromaDatabase import ChromaDatabase
from database.FaissDatabase import FaissDatabase
from embeddings.EmbeddingModel import EmbeddingModel
from retrieval.DocumentRetriever import DocumentRetriever
from chat.ChatEngine import ChatEngine
from chat.ChatUI import ChatUI


class Main:
    """Application entry point: loads a PDF and runs the selected chunking strategy."""

    def __init__(self, path):
        # Store the path to the PDF file to be processed.
        self.path = path


    def readFile(self):
        # Open the PDF and concatenate the extracted text of every page into one string.
        text = ""
        with pdfplumber.open(self.path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"

        return text


if __name__ == "__main__":
    app = Main("data/page.pdf")
    text = app.readFile()

    #  processor = ChunkProcessor(FixedChuncking(200))
    #  chunks = processor.process(text)
    #  print(chunks)

    #  processor.set_strategy(SentenceChunking(2,5))
    #  print(processor.process(text))

    fixed_chunking = FixedChuncking(200)
    #  chunks = fixed_chunking.chunk(text);
    chunks = fixed_chunking.fixed_with_overlap(text, overlap=10);
    # print(chunks)


    embed = EmbeddingModel()
    db = FaissDatabase(embed)
    db.create(chunks)
    db.save()
    # retriever = DocumentRetriever(db)
    # result = retriever.retrieve('what is python')
    # print(result[0])

    # After chunking + indexing, launch the chat UI over the FAISS store just built.
    ChatUI(ChatEngine("faiss")).launch()


    #  sentence_chunking = SentenceChunking(2,5)
    #  #chunks = sentence_chunking.chunk(text)
    #  #chunks = sentence_chunking.chunk_with_regix(text)

    #  paragraf_chunking = ParagraphChuncking(500)
    #  #chunks =  paragraf_chunking.chunk(text);

    #  sliding_window_chunking = SlidingWindowChunking(100, 50)
    #  #chunks = sliding_window_chunking.chunk(text)

    #  page_chunking = PageChunking("test.pdf")
    #  #chunks = page_chunking.chunk("")

    #  recursive_chunking = RecursiveChunking(500, 50)
    #  #chunks = recursive_chunking.chunk(text)

    #  # semantic_chunking = SemanticChunking()
    #  #chunks = semantic_chunking.chunk(text)

    #  table_chunking = TableChunking()
    #  chunks = table_chunking.chunk_tables("data/test.pdf")

    #  print(chunks)
