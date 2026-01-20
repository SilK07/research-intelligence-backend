from fastapi import FastAPI, Depends, UploadFile, File
from sqlalchemy.orm import Session
from db.session import get_db, engine
from db.base import Base
from db import models
from pypdf import PdfReader
from services.embeddings import get_embedding
from utils.similarity import cosine_similarity
from services.chunking import chunk_text
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
Base.metadata.create_all(bind=engine)

GEMENI_API_KEY = os.environ["GEMINI_API_KEY"]
client = genai.Client(api_key=GEMENI_API_KEY)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    return {"db": "connected"}

@app.get("/documents")
def get_all_documents(db: Session = Depends(get_db)):
    docs = db.query(models.documents).all()
    return docs

@app.get("/documents/{doc_id}")
def get_documents(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(models.documents).filter(models.documents.id == doc_id).first()
    return doc

@app.delete("/delete_document/{doc_id}")
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(models.documents).filter(models.documents.id == doc_id).first()
    if doc is None:
        return {"error": "Document not found"}
    
    db.delete(doc)
    db.commit()
    return {"message": "Document deleted"}

@app.post("/documents/upload")
def upload_document(title: str, file: UploadFile = File(...), db: Session = Depends(get_db)):

    reader = PdfReader(file.file)
    text = ""
    
    for page in reader.pages:
        text += page.extract_text() or ""
    
    text = text[:4000]

    embedding = get_embedding(text)
    document = models.documents(
        title=title,
        content=text,
        embedding=embedding
    )    

    db.add(document)
    db.commit()
    db.refresh(document)
    

    return {"id": document.id, "title": document.title, "pages": len(reader.pages)}

@app.get("/search")
def search_documents(query: str, db: Session = Depends(get_db)):
    query_embedding = get_embedding(query)

    documents = db.query(models.documents).all()

    scored_docs = []

    for doc in documents:
        if doc is None or doc.embedding is None:
            continue

        score = cosine_similarity(query_embedding, doc.embedding)
        scored_docs.append((score, doc))

    scored_docs.sort(key=lambda x: x[0], reverse=True)

    results = [
        {"id": doc.id, "title": doc.title, "score": score}
        for score, doc in scored_docs
    ]

    return results

@app.post("/qa")
def qa_system(query: str, db: Session = Depends(get_db)):
    query_embedding = get_embedding(query)

    documents = db.query(models.documents).all()

    scored_docs = []

    for doc in documents:
        if doc is None or doc.embedding is None:
            continue

        score = cosine_similarity(query_embedding, doc.embedding)
        scored_docs.append((score, doc))
    scored_docs.sort(key=lambda x: x[0], reverse=True)

    top_docs = scored_docs[:3]

    context = "\n\n".join(f"Document Title: {doc.title}\n{doc.content}" for _, doc in top_docs)

    prompt = f"""
    You are an assistant that provides answers based on the provided context below ONLY
    Context: {context}
    Question: {query}
    If the answer is not contained within the context, respond with "I don't know.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    answer = response.text

    return {
        "answer": answer,
        "sources": [
            {"id": doc.id, "title": doc.title} for _, doc in top_docs
        ]
    }
