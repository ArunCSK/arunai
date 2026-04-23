/**
 * adkClient.js  ──  Reusable ADK API Server client for Node.js
 * ─────────────────────────────────────────────────────────────
 * Wraps the ADK REST API (POST /run and POST /run_sse) in clean async helpers.
 */

import { v4 as uuidv4 } from "uuid";

const DEFAULT_BASE_URL = "http://localhost:8000";
const APP_NAME = "rag_agent"; // must match the folder name read by `adk api_server`

/**
 * Create a new ADK client bound to a specific user + session.
 *
 * @param {object} opts
 * @param {string} [opts.baseUrl]   ADK server URL  (default: http://localhost:8000)
 * @param {string} [opts.userId]    Persistent user ID (auto-generated if omitted)
 * @param {string} [opts.sessionId] Conversation session ID (auto-generated if omitted)
 * @param {string} [opts.appName]   ADK app/module name    (default: "rag_agent")
 */
export function createAdkClient({
  baseUrl = DEFAULT_BASE_URL,
  userId = `user-${uuidv4()}`,
  sessionId = `session-${uuidv4()}`,
  appName = APP_NAME,
} = {}) {
  // ── Session management ───────────────────────────────────────────────────

  async function createSession() {
    const url = `${baseUrl}/apps/${appName}/users/${userId}/sessions/${sessionId}`;
    const res = await fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: "{}" });
    if (!res.ok && res.status !== 409) {
      // 409 = session already exists, that's fine
      throw new Error(`Failed to create session: ${res.status} ${await res.text()}`);
    }
    return sessionId;
  }

  // ── Single-turn run ──────────────────────────────────────────────────────

  /**
   * Send a message and wait for the complete response.
   *
   * @param {string}  message  User's text input.
   * @returns {Promise<string>} The agent's final reply text.
   */
  async function run(message) {
    const res = await fetch(`${baseUrl}/run`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        app_name: appName,
        user_id: userId,
        session_id: sessionId,
        new_message: {
          role: "user",
          parts: [{ text: message }],
        },
      }),
    });

    if (!res.ok) {
      const body = await res.text();
      throw new Error(`ADK /run error ${res.status}: ${body}`);
    }

    const events = await res.json();
    return extractFinalText(events);
  }

  // ── Streaming run (SSE) ──────────────────────────────────────────────────

  /**
   * Send a message and stream the response token-by-token.
   *
   * @param {string}   message    User's text input.
   * @param {Function} onChunk    Called with each streamed text chunk.
   * @returns {Promise<string>}   Resolves with the full response when done.
   */
  async function runStream(message, onChunk = () => {}) {
    const res = await fetch(`${baseUrl}/run_sse`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "text/event-stream",
      },
      body: JSON.stringify({
        app_name: appName,
        user_id: userId,
        session_id: sessionId,
        new_message: {
          role: "user",
          parts: [{ text: message }],
        },
        streaming: true,
      }),
    });

    if (!res.ok) {
      throw new Error(`ADK /run_sse error ${res.status}: ${await res.text()}`);
    }

    let fullText = "";
    const reader = res.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const raw = decoder.decode(value);
      // SSE lines look like:  data: {...json...}
      for (const line of raw.split("\n")) {
        if (!line.startsWith("data:")) continue;
        const json = line.slice(5).trim();
        if (!json || json === "[DONE]") continue;
        try {
          const event = JSON.parse(json);
          const chunk = extractChunkText(event);
          if (chunk) {
            onChunk(chunk);
            fullText += chunk;
          }
        } catch {
          /* ignore malformed lines */
        }
      }
    }

    return fullText;
  }

  // ── Helpers ──────────────────────────────────────────────────────────────

  function extractFinalText(events) {
    // Walk events from the end – find the last model response
    for (let i = events.length - 1; i >= 0; i--) {
      const text = extractChunkText(events[i]);
      if (text) return text;
    }
    return "(no text response)";
  }

  function extractChunkText(event) {
    try {
      // ADK event structure: { content: { parts: [{text: "..."}], role: "model" }, ... }
      const parts = event?.content?.parts ?? [];
      const texts = parts.map((p) => p.text ?? "").filter(Boolean);
      return texts.join("") || null;
    } catch {
      return null;
    }
  }

  return {
    userId,
    sessionId,
    appName,
    baseUrl,
    createSession,
    run,
    runStream,
  };
}
