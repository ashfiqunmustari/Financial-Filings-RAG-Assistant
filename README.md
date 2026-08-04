# Financial Filings Q&A System (RAG)

A question-answering system over SEC 10-K filings. Ask a question in plain English and get an answer drawn from the actual filing, with the source sections shown. It retrieves the relevant passages with semantic search, then has an LLM generate the answer from only those passages, so the response stays grounded in the document rather than the model's general knowledge.

> **Current implementation:** Microsoft 2026 SEC 10-K filing

## Demo

**Example question**
> What products does Microsoft offer?

**Example answer**
- Windows
- Azure
- Microsoft 365
- Surface devices
- Xbox hardware and services
- Bing
- Copilot
- SQL Server
- Visual Studio
- ...and more

The answer is generated only from the retrieved filing content, and the relevant source sections are shown alongside it.

[Live demo](https://financial-filings-rag-assistant.streamlit.app/)

## How it works

The system has an offline stage (build the knowledge base once) and an online stage (answer questions).

**Offline — building the index:**
- Download the 10-K from SEC EDGAR
- Clean the raw filing from ~8.5M characters of HTML down to ~271K of usable text, removing XBRL tags and table-fragment noise
- Split into 98 section-aware chunks with overlap, each tagged with its filing section (Item 1, Item 1A, etc.)
- Embed the chunks with Sentence Transformers and store them in a FAISS index

**Online — answering a question:**
- Embed the question and search FAISS for the closest chunks
- Drop chunks that are too far off to be relevant (distance threshold of 1.5, chosen by profiling relevant vs. off-topic queries — relevant ones clustered under ~1.15, off-topic never came closer than ~1.80)
- If nothing clears the threshold, the system says it couldn't find the answer instead of guessing
- Send the retrieved chunks to the LLM and return the answer with its sources

## Stack

- **Retrieval:** Sentence Transformers (`all-MiniLM-L6-v2`), FAISS
- **Generation:** Llama-3.1-8B-Instruct via the Hugging Face Inference API
- **Backend:** FastAPI (`/ask`, `/health`)
- **Frontend:** Streamlit
- **Data:** SEC EDGAR

## Architecture
SEC EDGAR
        │
        ▼
Download 10-K Filing
        │
        ▼
Text Extraction
        │
        ▼
Data Cleaning
        │
        ▼
Semantic Chunking
        │
        ▼
Sentence Embeddings
        │
        ▼
FAISS Index
        │
User Q──┘
        │
        ▼
Semantic Retrieval
        │
        ▼
Retrieved Chunks
        │
        ▼
LLM (HF API)
        │
        ▼
Grounded Response
        │
        ▼
Streamlit UI

## Tech Stack

### Backend

- Python
- FastAPI
- FAISS
- Sentence Transformers
- Hugging Face Inference API

### Frontend

- Streamlit

### NLP & AI

- all-MiniLM-L6-v2
- Llama 3.1 8B Instruct
- Retrieval-Augmented Generation (RAG)

### Data Processing

- Trafilatura
- BeautifulSoup
- NumPy
- Requests

---

## Project Structure

```
financial-filings-rag/

├── app/
│   ├── api.py
│   ├── llm.py
│   ├── rag.py
│   └── retrieval.py
│
├── frontend/
│   └── app.py
│
├── ingestion/
│   ├── download_sec.py
│   ├── clean_text.py
│   ├── chunking.py
│   └── build_index.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── faiss/
│
├── requirements.txt
├── .env
└── README.md
```
## Future Improvements

- Multi-company support (Apple, NVIDIA, Meta, Alphabet, Amazon)
- Multiple filing years
