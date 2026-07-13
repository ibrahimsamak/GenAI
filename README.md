# PDF Chunking Strategies

A hands-on playground for comparing text-**chunking** strategies used in RAG and LLM pipelines. It reads a PDF, extracts its text (or tables/pages), and splits the content using one of several interchangeable algorithms — all built around a clean, extensible object-oriented design.

Chunking is the step that decides *how* a document is broken into pieces before embedding or feeding it to a model. The chunk boundaries you pick have a large impact on retrieval quality, so this project makes it easy to swap strategies and see the difference.

## Chunking Strategies

| Strategy | File | Splits by | Notes |
|---|---|---|---|
| **Fixed** | `FixedChuncking.py` | Fixed number of words | Also supports fixed-size chunks with overlap |
| **Sentence** | `SentenceChunking.py` | Groups of `n` sentences | Uses NLTK; regex-based variant included |
| **Paragraph** | `ParagraphChuncking.py` | Blank lines (`\n\n`) | Preserves natural paragraph breaks |
| **Sliding Window** | `SlidingWindowChunking.py` | Overlapping word windows | Retains context across chunk edges |
| **Recursive** | `RecursiveChunking.py` | Recursive separators | Wraps LangChain's `RecursiveCharacterTextSplitter` |
| **Page** | `PageChunking.py` | One chunk per PDF page | Uses PyMuPDF (`fitz`) |
| **Table** | `TableChunking.py` | Extracted tables | Uses `pdfplumber.extract_tables` |
| **Semantic** | `SemanticChunking.py` | Embedding similarity | Currently disabled — requires an OpenAI API key |

## Architecture

The project is a textbook demonstration of the four pillars of object-oriented programming, applied through the **Strategy** design pattern.

### 🧩 Abstraction — a common interface

`ChunkingStrategy` (in `strategies/base.py`) is an abstract base class that defines *what* every chunker must do, without saying *how*:

```python
from abc import ABC, abstractmethod

class ChunkingStrategy(ABC):
    @abstractmethod
    def chunk(self, text):
        pass
```

Callers only need to know that a strategy has a `chunk()` method — the details are abstracted away.

### 🧬 Inheritance — each strategy extends the base

Every concrete strategy inherits from `ChunkingStrategy` and reuses the shared contract:

```python
class FixedChuncking(ChunkingStrategy):
    def __init__(self, chunk_size):
        self.chunk_size = chunk_size

    def chunk(self, text):
        ...
```

### 🔀 Polymorphism — one processor, any strategy

`ChunkProcessor` (in `Processor.py`) works with *any* chunking strategy without modification. Swap the strategy at runtime and the processor behaves accordingly:

```python
processor = ChunkProcessor(FixedChuncking(500))
print(processor.process(text))

processor.set_strategy(SentenceChunking(2, 5))
print(processor.process(text))   # same call, different behavior
```

`ChunkProcessor` never needs to change when new strategies are added — it depends on the abstraction, not the implementations.

### 🔒 Encapsulation — each strategy owns its logic and parameters

Each strategy stores its own configuration (chunk size, overlap, sentence count, …) and hides its splitting logic behind the `chunk()` method. Internal details stay private to the strategy; the rest of the system doesn't need to know them.

```
┌──────────────────┐        uses        ┌─────────────────────┐
│  ChunkProcessor  │ ─────────────────▶ │  ChunkingStrategy   │  (abstract)
└──────────────────┘                    └─────────────────────┘
                                                   ▲
                    ┌──────────────┬───────────────┼───────────────┬─────────────┐
              FixedChuncking  SentenceChunking  ParagraphChuncking  ...       TableChunking
```

## Project Structure

```
.
├── Main.py                 # Entry point: reads test.pdf and runs a chosen strategy
├── Processor.py            # ChunkProcessor — the Strategy-pattern context
├── strategies/
│   ├── base.py             # ChunkingStrategy abstract base class
│   ├── FixedChuncking.py
│   ├── SentenceChunking.py
│   ├── ParagraphChuncking.py
│   ├── SlidingWindowChunking.py
│   ├── RecursiveChunking.py
│   ├── PageChunking.py
│   ├── TableChunking.py
│   └── SemanticChunking.py
└── test.pdf                # Sample input document
```

## Getting Started

### Requirements

- Python 3.12+
- Install the dependencies:

```bash
pip install pdfplumber PyMuPDF nltk langchain-text-splitters
```

The sentence strategy needs NLTK's `punkt` model. If `sent_tokenize` fails, download it once:

```python
import nltk
nltk.download('punkt')
```

> The **Semantic** strategy additionally requires `langchain-experimental`, `langchain-openai`, and an OpenAI API key. It is commented out by default.

### Running

```bash
python3 Main.py
```

`Main.py` reads `test.pdf` and runs a selected strategy. To try a different one, comment/uncomment the relevant lines in the `__main__` block. For example:

```python
fixed_chunking = FixedChuncking(500)
chunks = fixed_chunking.chunk(text)

sentence_chunking = SentenceChunking(2, 5)
chunks = sentence_chunking.chunk(text)

print(chunks)
```

## Adding a New Strategy

1. Create a file in `strategies/` with a class that subclasses `ChunkingStrategy`.
2. Implement the `chunk(self, text)` method.
3. Import it in `Main.py` (or pass it to `ChunkProcessor`) — no other code needs to change.

That last point is the payoff of the design: the system is **open for extension, closed for modification**.

## Notes

- Some class and file names contain intentional-looking spellings (`FixedChuncking`, `ParagraphChuncking`, `chunk_with_regix`). Reference them exactly as written to avoid breaking imports.
- `PageChunking` and `TableChunking` operate on a **file path** rather than pre-extracted text, since page and table structure is lost once a PDF is flattened to plain text.
