
import pdfplumber
from strategies.FixedChuncking import FixedChuncking
from strategies.SentenceChunking import SentenceChunking
from strategies.ParagraphChuncking import ParagraphChuncking
from strategies.SlidingWindowChunking import SlidingWindowChunking
from strategies.PageChunking import PageChunking
from strategies.RecursiveChunking import RecursiveChunking
# from strategies.SemanticChunking import SemanticChunking
from strategies.TableChunking import TableChunking

class Main:
    def __init__(self, path):
        self.path = path
       

    def readFile(self):
        text = ""
        with pdfplumber.open(self.path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        
        return text


if __name__ == "__main__":
     app = Main("test.pdf")
     text = app.readFile()

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
