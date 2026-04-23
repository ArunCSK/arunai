#!/usr/bin/env node
/**
 * demo.js  ──  Automated demo of the ADK RAG agent
 * ───────────────────────────────────────────────────
 * Run:  node demo.js
 * (the ADK api_server must already be running on port 8000)
 */

import chalk from "chalk";
import { createAdkClient } from "./adkClient.js";

const DEMO_QUESTIONS = [
  "What is the Google Agent Development Kit?",
  "How does the ADK API server work and what endpoints does it expose?",
  "How do I connect a Node.js app to an ADK agent?",
  "Explain the RAG pattern used in ADK agents.",
  "What is the ADK multi-agent architecture?",
  "Please add this to the knowledge base: 'ADK supports LangChain tools via the LangchainTool wrapper, enabling reuse of the entire LangChain ecosystem.'",
  "What do you know about LangChain tools in ADK?",
];

const SEPARATOR = chalk.dim("─".repeat(70));

async function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

function printBanner() {
  console.log(chalk.bold.cyan("\n╔══════════════════════════════════════════════════════════════════════╗"));
  console.log(chalk.bold.cyan("║         [ADK]  Google ADK 2.0 RAG Agent -- Node.js Demo             ║"));
  console.log(chalk.bold.cyan("╚══════════════════════════════════════════════════════════════════════╝\n"));
}

async function runDemo() {
  printBanner();

  const client = createAdkClient();

  console.log(chalk.yellow("[>>]  Creating session with ADK server..."));
  try {
    await client.createSession();
    console.log(chalk.green(`[OK]  Session ready`));
    console.log(chalk.dim(`    user_id    : ${client.userId}`));
    console.log(chalk.dim(`    session_id : ${client.sessionId}\n`));
  } catch (err) {
    console.error(chalk.red("[ERR]  Could not connect to ADK server."));
    console.error(chalk.red("    Make sure `adk api_server` is running in the rag_agent directory.\n"));
    console.error(err.message);
    process.exit(1);
  }

  for (let i = 0; i < DEMO_QUESTIONS.length; i++) {
    const question = DEMO_QUESTIONS[i];
    console.log(SEPARATOR);
    console.log(chalk.bold.blue(`\n[${i + 1}/${DEMO_QUESTIONS.length}] You: `) + question);
    console.log();

    try {
      process.stdout.write(chalk.bold.green("Agent: "));

      // Use streaming for real-time token output
      await client.runStream(question, (chunk) => {
        process.stdout.write(chalk.white(chunk));
      });

      console.log("\n");
    } catch (err) {
      console.error(chalk.red(`\n[WARN]  Error: ${err.message}\n`));
    }

    // Small pause between questions so it's easy to read
    if (i < DEMO_QUESTIONS.length - 1) {
      await sleep(800);
    }
  }

  console.log(SEPARATOR);
  console.log(chalk.bold.cyan("\n[DONE]  Demo complete!\n"));
}

runDemo().catch((err) => {
  console.error(chalk.red("Fatal error:"), err);
  process.exit(1);
});
