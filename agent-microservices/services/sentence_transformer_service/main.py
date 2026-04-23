"""
=============================================================
PROBLEM 4 — Sentence-Transformers Embedding Service (FastAPI)
=============================================================

ROLE: AI Engineer @ JPMorgan Chase
DIFFICULTY: Medium

----- PROBLEM STATEMENT -----
Build a semantic search microservice using sentence-transformers.

Endpoints:
  POST /embed          — embeds a list of texts, returns vectors
  POST /search         — finds the most similar document from the
                         in-memory knowledge base for a given query
  POST /similarity     — computes cosine similarity between two texts

EXPECTED INPUT  (/search):
  { "query": "What is machine learning?" }

EXPECTED OUTPUT (/search):
  {
    "query": "What is machine learning?",
    "best_match": "Machine learning is ...",
    "score": 0.87
  }

CONSTRAINTS:
  - Use "all-MiniLM-L6-v2" (fast, ~80MB).
  - Embeddings must be normalized (unit vectors) for cosine similarity.
  - Pre-encode the knowledge base at startup so /search is fast.
  - /embed must support batches of up to 64 texts.

----- CONCEPTS COVERED (20%) -----
  ✅  FastAPI skeleton
  ✅  Model loading at startup
  ✅  Knowledge base (sample documents provided)
  ✅  Normalisation helper

----- YOUR TASK (80%) -----
  ❌  /embed endpoint — encode batch, normalise, return as list-of-lists
  ❌  /search endpoint — embed query, cosine sim vs KB, return top match
  ❌  /similarity endpoint — embed two texts, return cosine sim score
  ❌  Bonus: return top-k results from /search (not just top-1)
  ❌  Bonus: add a POST /index endpoint to add new docs to the KB at runtime

----- RUN -----
  pip install -r requirements.txt
  uvicorn main:app --port 8004 --reload
  (first run downloads ~80MB model automatically)

----- HINTS -----
  Hint 1: model = SentenceTransformer("all-MiniLM-L6-v2")
  Hint 2: embeddings = model.encode(texts, normalize_embeddings=True)
  Hint 3: cosine_sim = np.dot(query_emb, doc_emb)  (works because both are unit vectors)
  Hint 4: best_idx = np.argmax(scores);  scores = kb_embeddings @ query_emb
=============================================================
"""

import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from typing import List
from contextlib import asynccontextmanager

# --------------- Knowledge base (PROVIDED — feel free to extend) ---------------
KNOWLEDGE_BASE = [
    "Machine learning is a subset of AI that enables systems to learn from data.",
    "PyTorch is a deep learning framework developed by Facebook AI Research.",
    "Transformers use self-attention mechanisms to process sequential data in parallel.",
    "RAG stands for Retrieval-Augmented Generation, combining search with LLMs.",
    "Scikit-learn provides simple tools for data mining and data analysis in Python.",
    "Sentence transformers create dense vector representations of text for semantic search.",
    "Neural networks consist of layers of interconnected nodes inspired by the brain.",
    "Gradient descent is an optimisation algorithm used to minimise a loss function.",
    "Cross-entropy loss measures the difference between predicted and true probability distributions.",
    "JPMorgan Chase uses AI to power fraud detection, customer service, and risk management.",
]

# Global state
model: SentenceTransformer = None
kb_embeddings: np.ndarray = None   # shape: (10, 384)

# --------------- Startup: load model + pre-encode KB (PROVIDED) ---------------
@asynccontextmanager
async def lifespan(app):
    global model, kb_embeddings
    print("Loading sentence-transformer model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    # Pre-encode all KB documents at startup (normalize=True so cosine_sim = dot product)
    # Shape: (10, 384) — 384 is the embedding dimension of all-MiniLM-L6-v2
    kb_embeddings = model.encode(KNOWLEDGE_BASE, normalize_embeddings=True)
    print(f"Knowledge base indexed: {kb_embeddings.shape}. Ready.")
    yield

app = FastAPI(title="Sentence-Transformers Embedding Service", version="1.0", lifespan=lifespan)

# --------------- Normalisation helper (PROVIDED) ---------------
def l2_normalize(vecs: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(vecs, axis=1, keepdims=True)
    return vecs / (norms + 1e-10)

# --------------- Request schemas ---------------
class EmbedRequest(BaseModel):
    texts: List[str]

class SearchRequest(BaseModel):
    query: str
    top_k: int = 1

class SimilarityRequest(BaseModel):
    text_a: str
    text_b: str

# --------------- Endpoints ---------------
@app.post("/embed")
def embed(req: EmbedRequest):
    """
    model.encode() runs the input through the transformer and mean-pools
    the token embeddings into a single 384-dim vector per sentence.
    normalize_embeddings=True makes each vector a unit vector → cosine_sim = dot product.
    We convert to Python lists for JSON serialisation.
    """
    embeddings = model.encode(req.texts, normalize_embeddings=True)
    return {
        "embeddings": embeddings.tolist(),  # list[list[float]], shape (N, 384)
        "dim": embeddings.shape[1],
        "count": len(req.texts),
    }

@app.post("/search")
def search(req: SearchRequest):
    """
    Semantic search: embed the query → compare to all KB vectors at once.
    Because both are normalised unit vectors:
        cosine_similarity(a, b) = dot(a, b)
    So:   scores = kb_embeddings @ query_vec   gives all similarities in one step.
    argsort gives indices sorted ascending; [::-1] reverses to descending.
    """
    query_vec = model.encode([req.query], normalize_embeddings=True)[0]  # (384,)
    # Matrix multiplication: (10, 384) @ (384,) → (10,) scores
    scores    = kb_embeddings @ query_vec

    # Top-k indices, sorted best-first
    top_indices = np.argsort(scores)[::-1][: req.top_k]

    results = [
        {"document": KNOWLEDGE_BASE[i], "score": round(float(scores[i]), 4)}
        for i in top_indices
    ]
    return {"query": req.query, "results": results}

@app.post("/similarity")
def similarity(req: SimilarityRequest):
    """
    Encode two texts as unit vectors.
    dot(a, b) = cos(θ) because |a| = |b| = 1.
    Value of 1.0 = identical direction, 0.0 = orthogonal, -1.0 = opposite.
    """
    embs = model.encode([req.text_a, req.text_b], normalize_embeddings=True)
    score = float(np.dot(embs[0], embs[1]))
    return {
        "text_a": req.text_a,
        "text_b": req.text_b,
        "cosine_similarity": round(score, 4),
    }
