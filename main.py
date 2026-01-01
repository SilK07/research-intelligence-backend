from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from db.session import get_db, engine
from db.base import Base
from db import models


app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    return {"db": "connected"}

@app.post("/documents")
def create_document(title: str, content:str, db: Session = Depends(get_db)):
    doc = models.documents(title=title, content=content)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc 

@app.get("/documents")
def get_documents(db: Session = Depends(get_db)):
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
