# GenAI — A RAG Pipeline, Built Block by Block

A hands-on learning project that assembles a Retrieval-Augmented Generation (RAG) pipeline from scratch,
one module at a time — with a strong focus on clean, object-oriented design. It walks through every layer:

**PDF chunking → embeddings → vector databases → retrieval → hybrid search + re-ranking → a Gradio chat app**,
plus a parallel **LlamaIndex** implementation of the same idea.

Each layer is a small, self-contained module with its own runnable `__main__` demo, so you can study any
piece in isolation — and `Main.py` ties them together into a working end-to-end app (chunk a PDF, index
it, and chat with it in the browser).

---

## Demo

![The Gradio chat app: a conversation about the indexed PDF on the left, with the retrieved source chunks shown in the "Relevant Context" panel on the right.](img/image.png)

_The end-to-end app (`python3 Main.py`): ask questions on the left, see the retrieved context that grounds each answer on the right._

---

## Pipeline at a glance

```
 PDF ──► Chunking ──► Embeddings ──► Vector DB ──► Retrieval ──► Hybrid Search ──► Re-Ranking ──► Chat UI
        strategies/   embeddings/   database/     retrieval/    rag_vector_system/  rag_vector_system/  chat/
                                    (FAISS/Chroma)               (BM25 + vector)     (CrossEncoder)   (Gradio+OpenAI)

 Main.py orchestrates:  chunk a PDF in data/ ──► build FAISS ──► launch Gradio chat
 Alternative path:      rag_llamaindex/  (LlamaIndex + Hugging Face embeddings & LLM)
```

## Modules

| Layer              | Location                                 | What it does                                                                                          |
| ------------------ | ---------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| **Chunking**       | `strategies/`, `Processor.py`, `Main.py` | 8 interchangeable PDF chunking strategies behind a common interface                                   |
| **Embeddings**     | `embeddings/EmbeddingModel.py`           | Wraps Hugging Face `all-MiniLM-L6-v2` sentence embeddings                                             |
| **Vector DBs**     | `database/`                              | `FaissDatabase` & `ChromaDatabase` behind a shared `VectorDatabase` abstraction, chosen via a factory |
| **Retrieval**      | `retrieval/DocumentRetriever.py`         | Exposes a vector store as a LangChain retriever                                                       |
| **Hybrid search**  | `rag_vector_system/HybridSearch.py`      | Fuses BM25 (keyword) + vector search via `EnsembleRetriever`                                          |
| **Re-ranking**     | `rag_vector_system/ReRanker.py`          | Re-scores results with a CrossEncoder (`ms-marco-MiniLM-L-6-v2`)                                      |
| **Chat app**       | `chat/ChatEngine.py`, `chat/ChatUI.py`   | RAG chat: `ChatEngine` (retrieve + OpenAI LLM) behind a `ChatUI` (Gradio)                             |
| **Orchestrator**   | `Main.py`                                | Chunk → index → launch the chat over the input PDF                                                    |
| **LlamaIndex RAG** | `rag_llamaindex/llamaIndex.py`           | End-to-end RAG with HF embeddings + a HF-hosted LLM                                                   |

## Object-oriented design

The project is a working showcase of the four pillars of OOP, applied through the **Strategy** and
**Factory** patterns.

- **Abstraction** — `ChunkingStrategy`, `VectorDatabase`, and `HybridSearchBase` are abstract base
  classes that define _what_ their implementations must do, not _how_.
- **Inheritance** — every chunker subclasses `ChunkingStrategy`; `FaissDatabase`/`ChromaDatabase`
  subclass `VectorDatabase`; `HybridSearch` subclasses `HybridSearchBase`.
- **Polymorphism** — `HybridSearch` works with _any_ `VectorDatabase`. It never mentions FAISS or Chroma;
  it only relies on the shared `get_documents()` / `as_retriever()` interface, so switching backends is a
  one-line change.
- **Encapsulation** — each class owns its own configuration and hides its internals behind a small public
  interface (e.g. FAISS persistence details live inside `FaissDatabase`).

### The payoff: swap the whole backend with one string

```python
from embeddings.EmbeddingModel import EmbeddingModel
from database.VectorDatabaseFactory import VectorDatabaseFactory
from rag_vector_system.HybridSearch import HybridSearch

emb = EmbeddingModel()
db  = VectorDatabaseFactory.create("faiss", emb)   # ← change to "chroma"; nothing else changes
db.load()

results = HybridSearch(db, k=2).search("What is AI?")
```

## Getting started

### Requirements

- Python 3.12+
- There is no `requirements.txt` — install what each layer needs:

```bash
# core RAG stack
pip install pdfplumber PyMuPDF nltk \
            langchain-community langchain-classic langchain-chroma \
            langchain-huggingface langchain-text-splitters \
            faiss-cpu chromadb rank_bm25 sentence-transformers python-dotenv

# chat app (Main.py)
pip install gradio langchain-openai

# LlamaIndex path
pip install llama-index llama-index-embeddings-huggingface llama-index-llms-huggingface-api
```

The sentence chunker needs NLTK's `punkt` model (`python -c "import nltk; nltk.download('punkt')"`).

### Configuration

Create a `.env` file (already gitignored) with your API keys:

```
HF_KEY=hf_xxxxxxxxxxxxxxxxxxxxx
OPEN_AI_KEy=sk-xxxxxxxxxxxxxxxxx      # used by the Gradio chat app (gpt-4.1-nano)
```

The `HF_KEY` token must have the **"Make calls to Inference Providers"** permission for the LlamaIndex LLM
step. The chat app reads `OPENAI_API_KEY` first and falls back to `OPEN_AI_KEy`, so you can use the standard
name instead if you prefer.

### Running

Run every module as a **package from the project root** (not by file path — see the note below):

```bash
python3 Main.py                              # full app: chunk PDF → FAISS → launch Gradio chat
python3 -m database.FaissDatabase            # build & persist a FAISS store
python3 -m rag_vector_system.HybridSearch    # hybrid search + re-ranking
python3 -m rag_llamaindex.llamaIndex         # LlamaIndex RAG (needs HF_KEY exported)
```

`Main.py` opens the browser chat automatically. It needs both `.env` keys exported (see below) and a valid
OpenAI key for `gpt-4.1-nano`.

> ⚠️ **Always use `python3 -m package.Module` from the repo root.** Running `python3 database/FaissDatabase.py`
> directly puts the file's folder on `sys.path` instead of the project root, which breaks cross-package
> imports (`ModuleNotFoundError: No module named 'embeddings'`).

To load `.env` for a run:

```bash
set -a; . ./.env; set +a; python3 -m rag_llamaindex.llamaIndex
```

## Chunking strategies

| Strategy       | File                                  | Splits by                                            |
| -------------- | ------------------------------------- | ---------------------------------------------------- |
| Fixed          | `strategies/FixedChuncking.py`        | Fixed word count (with optional overlap)             |
| Sentence       | `strategies/SentenceChunking.py`      | Groups of `n` sentences (NLTK or regex)              |
| Paragraph      | `strategies/ParagraphChuncking.py`    | Blank lines                                          |
| Sliding Window | `strategies/SlidingWindowChunking.py` | Overlapping word windows                             |
| Recursive      | `strategies/RecursiveChunking.py`     | LangChain recursive separators                       |
| Page           | `strategies/PageChunking.py`          | One chunk per PDF page (PyMuPDF)                     |
| Table          | `strategies/TableChunking.py`         | Extracted tables (pdfplumber)                        |
| Semantic       | `strategies/SemanticChunking.py`      | Embedding similarity _(disabled — needs OpenAI key)_ |

## Notes & gotchas

- **FAISS is not auto-persisted** — call `save()`, then `load()` later. Chroma persists automatically and
  _appends_ on each `create()`, so delete `vectorstores/chroma_store` to avoid duplicate documents.
- **LlamaIndex + `test.pdf`:** the default PDF reader garbles this file's fonts, so `llamaIndex` extracts
  text with `pdfplumber` instead.
- **HF LLM models must have a live inference provider.** `Qwen/Qwen2.5-7B-Instruct` works out of the box;
  some models (e.g. old Mistral builds) have no live provider and return 404.
- **Gradio 6:** `gr.Chatbot` no longer takes `type="messages"` (it's the default now), and `theme` is passed
  to `launch()` rather than `gr.Blocks()`. Don't name a file `gradio.py` — it shadows the library on import.
- A harmless `RLock … _recursion_count` traceback may print at exit on Python 3.12 (from the `multiprocess`
  package) — it fires _after_ the program finishes and can be ignored.
- Several chunking class/file names contain intentional spellings (`FixedChuncking`, `ParagraphChuncking`,
  `chunk_with_regix`). Reference them exactly to avoid breaking imports.
