# 📚 Research Intelligence Backend

A backend system that ingests documents, generates embeddings, performs semantic search, and answers user questions using Retrieval-Augmented Generation (RAG).

Built with FastAPI, SQLAlchemy, and transformer-based embeddings.

---

## 🚀 Features

- Upload documents (PDF / text)
- Extract and store document content
- Generate embeddings for semantic understanding
- Store embeddings in a database
- Semantic search using cosine similarity
- Question Answering over uploaded documents (RAG)
- Clean, modular backend architecture

---

## 🧠 How It Works

1. **Document Upload**
   - User uploads a document
   - Text is extracted from the file
   - Embeddings are generated and stored

2. **Semantic Search**
   - User query is converted into an embedding
   - Query embedding is compared with stored embeddings
   - Most relevant documents are retrieved

3. **Question Answering**
   - Retrieved documents are used as context
   - An LLM generates a grounded answer

---

## 🏗️ Architecture

Client
    → FastAPI
    → SQLAlchemy (SQLite / PostgreSQL)
    → Embedding Service
    → Similarity Search
    → LLM
→ Response

---

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python
- **Database**: SQLite (can be swapped with PostgreSQL)
- **ORM**: SQLAlchemy
- **Embeddings**: Sentence Transformers / Gemini Embeddings
- **LLM**: Gemini / OpenAI (configurable)
- **Similarity**: Cosine similarity

---

## 📌 API Endpoints

### Upload Document

POST/documents/upload

### List Documents

GET/documents

### Semantic Search

GET/similarity_search?query=...

### Question Answering

GET/qa?query=....

---

## ⚙️ Running Locally

```bash
git clone https://github.com/your-username/research-intelligence-backend
cd research-intelligence-backend

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

fastapi dev main.py
```

VISIT:
    -> API Docs: http://127.0.0.1:8000/docs

