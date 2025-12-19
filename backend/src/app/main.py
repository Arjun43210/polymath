# backend/src/app/main.py
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import uuid
from .ingest import extract_pages, chunk_pages
from .embed import build_index, query_index, load_index
from .llm import answer_with_llm

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "data/uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="Textbook RAG Backend")

# allow requests from frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # only allow pdf for now
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF uploads supported in this demo.")
    file_id = str(uuid.uuid4())
    dest = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)
    # extract + chunk + build index
    pages = extract_pages(dest)
    chunks = chunk_pages(pages)
    build_index(chunks)
    return {"status": "ok", "file_id": file_id, "chunks": len(chunks)}

class QueryRequest:
    def __init__(self, question: str, top_k: int = 6):
        self.question = question
        self.top_k = top_k

from pydantic import BaseModel

class QueryModel(BaseModel):
    question: str
    top_k: int = 6

@app.post("/api/query")
def query(q: QueryModel):
    if not q.question:
        raise HTTPException(status_code=400, detail="Question is required")
    retrieved = query_index(q.question, top_k=q.top_k)
    if not retrieved:
        return {"answer": None, "retrieved": []}
    answer = answer_with_llm(q.question, retrieved)
    return {"answer": answer, "retrieved": retrieved}
