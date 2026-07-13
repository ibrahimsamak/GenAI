
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
     app = Main("test.pdf")
     text = app.readFile()
     
    #  processor = ChunkProcessor(FixedChuncking(500))
    #  chunks = processor.process(text)
    #  print(chunks)
     
    #  processor.set_strategy(SentenceChunking(2,5))
    #  print(processor.process(text))

     fixed_chunking = FixedChuncking(500)
     #chunks = fixed_chunking.chunk(text);
     #chunks = fixed_chunking.fixed_with_overlap(text, overlap=10);
     
     sentence_chunking = SentenceChunking(2,5)
     #chunks = sentence_chunking.chunk(text)
     #chunks = sentence_chunking.chunk_with_regix(text)

     paragraf_chunking = ParagraphChuncking(500)
     #chunks =  paragraf_chunking.chunk(text);

     sliding_window_chunking = SlidingWindowChunking(100, 50)
     #chunks = sliding_window_chunking.chunk(text)

     page_chunking = PageChunking("test.pdf")
     #chunks = page_chunking.chunk("")

     recursive_chunking = RecursiveChunking(500, 50)
     #chunks = recursive_chunking.chunk(text)

     # semantic_chunking = SemanticChunking()
     #chunks = semantic_chunking.chunk(text)

     table_chunking = TableChunking()
     chunks = table_chunking.chunk_tables("test.pdf")

     print(chunks)
