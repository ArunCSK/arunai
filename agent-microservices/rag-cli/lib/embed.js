/**
 * embed.js — calls the Sentence-Transformer service (port 8004)
 *
 * PROBLEM 6 — RAG CLI (Node.js)
 *
 * CONCEPTS COVERED (20%):
 *   ✅ fetch wrapper skeleton
 *   ✅ EMBED_URL constant
 *
 * YOUR TASK (80%):
 *   ❌ embedTexts(texts)  — POST /embed, return array of float32 vectors
 *   ❌ embedQuery(query)  — convenience: embed a single string, return vector
 *
 * HINTS:
 *   Hint 1: const res = await fetch(EMBED_URL, { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify({texts}) })
 *   Hint 2: const data = await res.json(); return data.embeddings;
 */

const EMBED_URL = "http://localhost:8004/embed";

/**
 * Embed an array of texts by calling the sentence-transformer microservice.
 *
 * fetch() is the browser/Node HTTP client.
 * We POST JSON to /embed and read back { embeddings: [[...], [...]], dim: 384 }.
 *
 * @param {string[]} texts
 * @returns {Promise<number[][]>} array of 384-dim float vectors
 */
export async function embedTexts(texts) {
  const res = await fetch(EMBED_URL, {
    method:  "POST",
    headers: { "Content-Type": "application/json" },
    body:    JSON.stringify({ texts }),          // {"texts": ["..."]}
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Embed service error ${res.status}: ${err}`);
  }

  const data = await res.json();
  return data.embeddings;   // number[][], shape (N, 384)
}

/**
 * Convenience: embed a single query string.
 * Calls embedTexts with a one-element array and unpacks the first vector.
 *
 * @param {string} query
 * @returns {Promise<number[]>} a single 384-dim float vector
 */
export async function embedQuery(query) {
  const embs = await embedTexts([query]);
  return embs[0];   // unwrap the first (and only) embedding
}

