"""
rag_store.py  ── Simple in-memory RAG engine
──────────────────────────────────────────────
Uses sentence-transformers to embed text chunks and FAISS for ANN search.
No cloud services needed; everything runs locally.
"""

from __future__ import annotations

import textwrap
from dataclasses import dataclass, field
from typing import List

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# ── Model Config ──────────────────────────────────────────────────────────────
# "all-MiniLM-L6-v2" is tiny (~80 MB) and fast; swap for a bigger model anytime.
EMBED_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE = 300        # characters per chunk
CHUNK_OVERLAP = 50      # overlapping characters between chunks
TOP_K = 3               # passages returned per query


@dataclass
class Chunk:
    text: str
    source: str = "unknown"


class RAGStore:
    """Lightweight in-memory vector store for RAG."""

    def __init__(self):
        self._model = SentenceTransformer(EMBED_MODEL)
        self._dim: int | None = None
        self._index: faiss.IndexFlatIP | None = None
        self._chunks: List[Chunk] = []

    # ── Ingestion ─────────────────────────────────────────────────────────────

    def add_text(self, text: str, source: str = "manual") -> int:
        """Chunk `text`, embed, and add to the store. Returns # chunks added."""
        chunks = self._chunk_text(text, source)
        if not chunks:
            return 0
        embeddings = self._embed([c.text for c in chunks])
        self._ensure_index(embeddings.shape[1])
        self._index.add(embeddings)          # type: ignore[union-attr]
        self._chunks.extend(chunks)
        return len(chunks)

    def add_documents(self, docs: List[dict]) -> int:
        """Add multiple docs. Each doc: {"text": str, "source": str}"""
        total = 0
        for doc in docs:
            total += self.add_text(doc["text"], doc.get("source", "unknown"))
        return total

    # ── Retrieval ─────────────────────────────────────────────────────────────

    def retrieve(self, query: str, top_k: int = TOP_K) -> List[Chunk]:
        """Return the top-k most relevant chunks for `query`."""
        if not self._chunks:
            return []
        q_emb = self._embed([query])
        k = min(top_k, len(self._chunks))
        _, indices = self._index.search(q_emb, k)  # type: ignore[union-attr]
        return [self._chunks[i] for i in indices[0] if i >= 0]

    def retrieve_as_context(self, query: str, top_k: int = TOP_K) -> str:
        """Convenience: return retrieved chunks formatted as a single string."""
        chunks = self.retrieve(query, top_k)
        if not chunks:
            return "No relevant context found."
        parts = []
        for i, c in enumerate(chunks, 1):
            parts.append(f"[Source {i}: {c.source}]\n{c.text}")
        return "\n\n".join(parts)

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _chunk_text(self, text: str, source: str) -> List[Chunk]:
        text = text.strip()
        if not text:
            return []
        chunks = []
        start = 0
        while start < len(text):
            end = start + CHUNK_SIZE
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append(Chunk(text=chunk_text, source=source))
            start += CHUNK_SIZE - CHUNK_OVERLAP
        return chunks

    def _embed(self, texts: List[str]) -> np.ndarray:
        emb = self._model.encode(texts, normalize_embeddings=True)
        return emb.astype("float32")

    def _ensure_index(self, dim: int):
        if self._index is None:
            self._dim = dim
            # Inner-product on normalized vectors ≡ cosine similarity
            self._index = faiss.IndexFlatIP(dim)
