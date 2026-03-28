/**
 * retrieve.js — cosine similarity retrieval over local document store
 *
 * PROBLEM 6 — RAG CLI (Node.js)
 *
 * CONCEPTS COVERED (20%):
 *   ✅ Document loading from JSON
 *   ✅ cosineSimilarity() signature
 *
 * YOUR TASK (80%):
 *   ❌ cosineSimilarity(vecA, vecB) — dot product / (|a| * |b|)
 *   ❌ retrieveTopK(queryVec, docVecs, docs, k) — rank docs by similarity
 *
 * HINTS:
 *   Hint 1: dot product = vecA.reduce((sum, a, i) => sum + a * vecB[i], 0)
 *   Hint 2: norm = Math.sqrt(vec.reduce((s, v) => s + v * v, 0))
 *   Hint 3: sort by score descending, slice to k
 */

import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const __dirname = dirname(fileURLToPath(import.meta.url));

/** Load document store from JSON (PROVIDED) */
export function loadDocuments() {
  const raw = readFileSync(join(__dirname, "documents.json"), "utf8");
  return JSON.parse(raw);  // [{ id, text }, ...]
}

/**
 * Compute cosine similarity between two vectors.
 *
 * Formula: cos(θ) = (A · B) / (|A| × |B|)
 *
 * Because our service returns NORMALIZED embeddings (unit vectors, |v|=1),
 * this simplifies to just the dot product. But we implement the full
 * formula here so it works even with non-normalized vectors.
 *
 * @param {number[]} vecA
 * @param {number[]} vecB
 * @returns {number} similarity in [-1, 1]
 */
export function cosineSimilarity(vecA, vecB) {
  // Dot product: sum of element-wise products
  const dot  = vecA.reduce((sum, a, i) => sum + a * vecB[i], 0);

  // L2 norms: sqrt(sum of squares)
  const normA = Math.sqrt(vecA.reduce((s, v) => s + v * v, 0));
  const normB = Math.sqrt(vecB.reduce((s, v) => s + v * v, 0));

  // Guard against zero-vectors (unlikely but safe)
  if (normA === 0 || normB === 0) return 0;

  return dot / (normA * normB);
}

/**
 * Retrieve the top-k most similar documents for a given query vector.
 *
 * Steps:
 *  1. Score every document with cosineSimilarity(queryVec, docVec)
 *  2. Sort descending by score
 *  3. Slice to top-k
 *
 * @param {number[]} queryVec    - embedded query (384-dim)
 * @param {number[][]} docVecs   - embedded docs (same order as docs)
 * @param {object[]} docs        - [{id, text}] from documents.json
 * @param {number} k             - number of results to return
 * @returns {{ doc: object, score: number }[]}
 */
export function retrieveTopK(queryVec, docVecs, docs, k = 3) {
  const scored = docs.map((doc, i) => ({
    doc,
    score: cosineSimilarity(queryVec, docVecs[i]),
  }));

  // Sort descending (highest similarity first)
  scored.sort((a, b) => b.score - a.score);

  return scored.slice(0, k);
}
