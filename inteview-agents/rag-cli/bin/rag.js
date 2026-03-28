#!/usr/bin/env node
/**
 * =============================================================
 * PROBLEM 6 — RAG CLI (Node.js / npm)
 * =============================================================
 *
 * ROLE: AI Engineer @ JPMorgan Chase
 * DIFFICULTY: Medium
 *
 * ----- PROBLEM STATEMENT -----
 * Build a command-line RAG (Retrieval-Augmented Generation) tool
 * that answers questions using two microservices:
 *   - Service 4 (port 8004): sentence-transformer → embed query + docs
 *   - Service 5 (port 8005): HuggingFace → classify or summarize context
 *
 * Usage:
 *   node bin/rag.js "What is machine learning?"
 *   node bin/rag.js --top-k 3 "How does PyTorch work?"
 *
 * PIPELINE (what you must implement):
 *   1. Parse argv for the question (and optional --top-k flag)
 *   2. Load documents from lib/documents.json
 *   3. Embed ALL documents via POST /embed (service 4)
 *   4. Embed the user QUERY via POST /embed (service 4)
 *   5. Find top-k documents via cosineSimilarity (lib/retrieve.js)
 *   6. Build a context string: join top-k doc texts
 *   7. Call POST /summarize with context on service 5
 *   8. Print: question, retrieved docs (with scores), and the summary
 *
 * EXPECTED OUTPUT (formatted with chalk):
 *   ❓ Question: What is machine learning?
 *
 *   📄 Retrieved Context (top 2):
 *     [0.91] Machine learning is a subset of AI…
 *     [0.82] Neural networks learn hierarchical…
 *
 *   🤖 RAG Answer:
 *     Machine learning enables systems to learn from data and …
 *
 * ----- CONCEPTS COVERED (20%) -----
 *   ✅  CLI arg parsing skeleton
 *   ✅  Spinner (ora) usage example
 *   ✅  CLASSIFY_URL + SUMMARIZE_URL constants
 *   ✅  printBanner() helper (provided)
 *
 * ----- YOUR TASK (80%) -----
 *   ❌  parseArgs()      — extract question and --top-k from process.argv
 *   ❌  main()           — orchestrate the full RAG pipeline (steps 1-8)
 *   ❌  lib/embed.js     — embedTexts() and embedQuery()
 *   ❌  lib/retrieve.js  — cosineSimilarity() and retrieveTopK()
 *   ❌  Bonus: add --mode classify to call /classify instead of /summarize
 *   ❌  Bonus: add --port flags so the user can override default ports
 *
 * ----- RUN -----
 *   # Start services 4 and 5 first, then:
 *   cd rag-cli && npm install
 *   node bin/rag.js "What is PyTorch?"
 *
 * ----- HINTS -----
 *   Hint 1: process.argv.slice(2) gives cli args; question is the last non-flag
 *   Hint 2: const spinner = ora("Embedding...").start(); ... spinner.succeed("Done");
 *   Hint 3: POST /summarize body: { texts: [contextString], max_new_tokens: 80 }
 *   Hint 4: result.results[0].summary gives the summary text from service 5
 * =============================================================
 */

import chalk from "chalk";
import ora from "ora";
import fetch from "node-fetch";
import { embedTexts, embedQuery } from "../lib/embed.js";
import { loadDocuments, retrieveTopK } from "../lib/retrieve.js";

const EMBED_URL      = "http://localhost:8004";
const CLASSIFY_URL   = "http://localhost:8005/classify";
const SUMMARIZE_URL  = "http://localhost:8005/summarize";

// --------------- Provided: banner ---------------
function printBanner() {
  console.log(chalk.cyan.bold("\n╔══════════════════════════════════╗"));
  console.log(chalk.cyan.bold("║  🧠  RAG CLI  —  Interview Prep  ║"));
  console.log(chalk.cyan.bold("╚══════════════════════════════════╝\n"));
}

// --------------- Parse CLI args ---------------
function parseArgs() {
  /**
   * process.argv = ["node", "bin/rag.js", "--top-k", "3", "What is ML?"]
   *   slice(2) removes the first two entries (executables).
   * We scan for --top-k <n>, then treat the remaining strings as the question.
   */
  const args = process.argv.slice(2);
  let topK = 2;
  const questionParts = [];

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--top-k" && args[i + 1]) {
      topK = parseInt(args[i + 1], 10);
      i++;                          // skip the number token
    } else {
      questionParts.push(args[i]);  // collect non-flag tokens
    }
  }

  const question = questionParts.join(" ").trim();
  if (!question) {
    console.error(chalk.red('Usage: node bin/rag.js [--top-k <n>] "Your question here"'));
    process.exit(1);
  }

  return { question, topK };
}

// --------------- Main RAG pipeline ---------------
async function main() {
  printBanner();

  // 1. Parse args
  const { question, topK } = parseArgs();
  console.log(chalk.yellow(`❓ Question: ${question}\n`));

  // 2. Load documents from JSON file
  const docs = loadDocuments();  // [{ id, text }, ...]

  // 3. Embed all documents
  //    We do this every run for simplicity; in production you'd persist these vectors.
  const docSpinner = ora("Embedding documents...").start();
  const docTexts   = docs.map(d => d.text);
  const docVecs    = await embedTexts(docTexts);      // number[][], shape (N, 384)
  docSpinner.succeed(`Embedded ${docs.length} documents.`);

  // 4. Embed the user query
  const querySpinner = ora("Embedding query...").start();
  const queryVec     = await embedQuery(question);    // number[], shape (384,)
  querySpinner.succeed("Query embedded.");

  // 5. Retrieve top-k most similar documents
  const topDocs = retrieveTopK(queryVec, docVecs, docs, topK);

  // 6. Print retrieved context with similarity scores
  console.log(chalk.bold(`\n📄 Retrieved Context (top ${topK}):`));
  topDocs.forEach(r => {
    const scoreStr = chalk.green(`[${r.score.toFixed(4)}]`);
    console.log(`  ${scoreStr} ${r.doc.text}`);
  });

  // 7. Build context string for the summarizer
  const context = topDocs.map(r => r.doc.text).join(" ");

  // 8. Call /summarize on the HuggingFace service with the context
  const ragSpinner = ora("Generating RAG answer via summarization...").start();
  const response   = await fetch(SUMMARIZE_URL, {
    method:  "POST",
    headers: { "Content-Type": "application/json" },
    body:    JSON.stringify({ texts: [context], max_new_tokens: 80, num_beams: 4 }),
  });

  if (!response.ok) {
    ragSpinner.fail("Summarization service error.");
    const err = await response.text();
    throw new Error(err);
  }

  const result  = await response.json();
  const summary = result.results[0].summary;
  ragSpinner.succeed("Answer ready.");

  // 9. Print the final RAG answer
  console.log(chalk.bold("\n🤖 RAG Answer:"));
  console.log(chalk.greenBright(`  ${summary}\n`));
}

main().catch(err => {
  console.error(chalk.red("Error:"), err.message);
  process.exit(1);
});
