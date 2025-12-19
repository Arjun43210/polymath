# backend/src/app/embed.py
import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

EMBED_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
INDEX_PATH = os.getenv("VECTOR_DB_PATH", "data/faiss.index")
META_PATH = os.getenv("VECTOR_META_PATH", "data/meta.json")

def build_index(chunks, index_path=INDEX_PATH, meta_path=META_PATH):
    model = SentenceTransformer(EMBED_MODEL)
    texts = [c["text"] for c in chunks]
    vectors = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    vectors = vectors.astype("float32")
    faiss.normalize_L2(vectors)
    d = vectors.shape[1]
    index = faiss.IndexFlatIP(d)
    index.add(vectors)
    os.makedirs(os.path.dirname(index_path) or ".", exist_ok=True)
    faiss.write_index(index, index_path)
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False)

def load_index(index_path=INDEX_PATH, meta_path=META_PATH):
    if not os.path.exists(index_path) or not os.path.exists(meta_path):
        return None, None
    index = faiss.read_index(index_path)
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
    return index, meta

def query_index(question: str, top_k: int = 6):
    index, meta = load_index()
    if index is None:
        return []
    model = SentenceTransformer(EMBED_MODEL)
    qv = model.encode(question).astype("float32")
    faiss.normalize_L2(qv.reshape(1, -1))
    D, I = index.search(qv.reshape(1, -1), top_k)
    results = []
    for score, idx in zip(D[0], I[0]):
        item = meta[idx]
        results.append({"score": float(score), "page": item.get("page"), "text": item.get("text")})
    return results
