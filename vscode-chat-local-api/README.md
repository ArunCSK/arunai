# VS Code Chat Local API

This extension exposes a simple local HTTP API that returns chat-style responses. It includes a status-bar toggle (bottom-right) to start/stop the server.

Quick start

1. Install dependencies:

```bash
cd vscode-chat-local-api
npm install
```

2. Run the extension in VS Code (press F5) or package it.

3. Toggle the server using the status bar button labeled `Chat API: Off` / `Chat API: On`.

4. If the commands do not appear immediately, reload the window after installing the extension.

Example request

```bash
curl -X POST http://localhost:3333/chat -H "Content-Type: application/json" -d '{"message":"Hello from curl"}'

# Response
{"reply":"Echo: Hello from curl"}
```

Replace the `generateReply` implementation in `extension.js` to call Claude, Gemini (Google ADK), or Copilot Chat APIs as needed.
