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