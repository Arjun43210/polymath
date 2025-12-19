# backend/src/app/ingest.py
import re
from typing import List, Dict
from PyPDF2 import PdfReader

def extract_pages(pdf_path: str) -> List[Dict]:
    reader = PdfReader(pdf_path)
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        text = re.sub(r"\s+", " ", text).strip()
        pages.append({"page": i + 1, "text": text})
    return pages

def chunk_pages(pages: List[Dict], chunk_size_words: int = 400, overlap: int = 80):
    chunks = []
    for p in pages:
        words = p["text"].split()
        if not words:
            continue
        step = chunk_size_words - overlap
        for i in range(0, max(1, len(words)), step):
            chunk_words = words[i:i + chunk_size_words]
            chunk_text = " ".join(chunk_words)
            chunks.append({"page": p["page"], "text": chunk_text})
            if i + chunk_size_words >= len(words):
                break
    return chunks
