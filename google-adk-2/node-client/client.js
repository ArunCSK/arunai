#!/usr/bin/env node
/**
 * client.js  ──  Interactive CLI chat with the ADK RAG agent
 * ────────────────────────────────────────────────────────────
 * Run:  node client.js   OR   npm run chat
 *
 * Commands inside the chat:
 *   /exit       – quit
 *   /sources    – list knowledge base sources
 *   /add        – add text (prompts for source and text)
 *   /clear      – start a new session (clears conversation history)
 */

import chalk from "chalk";
import * as readline from "readline";
import { createAdkClient } from "./adkClient.js";

const BANNER = `
${chalk.bold.cyan("╔══════════════════════════════════════════════════════════════════╗")}
${chalk.bold.cyan("║   [ADK]  ADK 2.0 RAG Agent  --  Interactive Chat                ║")}
${chalk.bold.cyan("║   Commands: /exit  /sources  /add  /clear                       ║")}
${chalk.bold.cyan("╚══════════════════════════════════════════════════════════════════╝")}
`;

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

function ask(prompt) {
  return new Promise((resolve) => rl.question(prompt, resolve));
}

async function main() {
  console.log(BANNER);

  let client = createAdkClient();

  const connect = async () => {
    process.stdout.write(chalk.yellow("[>>]  Connecting to ADK server... "));
    try {
      await client.createSession();
      console.log(chalk.green("OK"));
      console.log(chalk.dim(`    Session: ${client.sessionId}\n`));
    } catch {
      console.log(chalk.red("FAILED"));
      console.log(chalk.red("    Is `adk api_server` running? (cd rag_agent && adk api_server)"));
      process.exit(1);
    }
  };

  await connect();

  console.log(chalk.dim("Type your question and press Enter. Type /exit to quit.\n"));

  while (true) {
    const input = (await ask(chalk.bold.blue("You: "))).trim();
    if (!input) continue;

    // ── Built-in commands ──────────────────────────────────────────────────
    if (input === "/exit") {
      console.log(chalk.cyan("\n[BYE]  Goodbye!\n"));
      rl.close();
      break;
    }

    if (input === "/clear") {
      client = createAdkClient();
      await connect();
      continue;
    }

    if (input === "/sources") {
      await sendAndPrint(client, "List all knowledge base sources for me.");
      continue;
    }

    if (input === "/add") {
      const source = (await ask(chalk.yellow("  Source label: "))).trim() || "user";
      const text = (await ask(chalk.yellow("  Text to add:  "))).trim();
      if (!text) {
        console.log(chalk.red("  (empty text, skipping)\n"));
        continue;
      }
      await sendAndPrint(
        client,
        `Add this text to the knowledge base with source "${source}": ${text}`
      );
      continue;
    }

    // ── Normal chat ────────────────────────────────────────────────────────
    await sendAndPrint(client, input);
  }
}

async function sendAndPrint(client, message) {
  process.stdout.write(chalk.bold.green("\nAgent: "));
  try {
    await client.runStream(message, (chunk) => {
      process.stdout.write(chalk.white(chunk));
    });
  } catch (err) {
    console.error(chalk.red(`\n[WARN]  ${err.message}`));
  }
  console.log("\n");
}

main().catch((err) => {
  console.error(chalk.red("Fatal:"), err);
  process.exit(1);
});
