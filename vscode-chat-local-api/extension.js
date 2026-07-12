const vscode = require('vscode');
const http = require('http');

let server = null;
let statusBarItem = null;
let treeView = null;
let treeDataProvider = null;
let serverRunning = false;
let chatParticipant = null;
const PORT = Number(process.env.VSCODE_CHAT_LOCAL_PORT || 3333);

async function generateReply(message) {
  // If an OpenAI API key is present, send the prompt to OpenAI Chat Completions.
  // Otherwise fall back to the simple echo placeholder.
  const safe = (message || '').toString();
  const apiKey = process.env.OPENAI_API_KEY || null;
  if (!apiKey) {
    return `Echo: ${safe}`;
  }

  // Use the OpenAI Chat Completions API via HTTPS (no external deps required).
  const https = require('https');

  const modelName = process.env.OPENAI_MODEL || 'gpt-3.5-turbo';
  const body = JSON.stringify({
    model: modelName,
    messages: [{ role: 'user', content: safe }],
    temperature: 0.2,
    max_tokens: 512
  });

  const options = {
    hostname: 'api.openai.com',
    port: 443,
    path: '/v1/chat/completions',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(body),
      'Authorization': `Bearer ${apiKey}`
    }
  };

  return await new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          // Pull assistant text from response structure
          const text = (parsed && parsed.choices && parsed.choices[0] && parsed.choices[0].message && parsed.choices[0].message.content) || null;
          if (text) return resolve(text);
          // fallback to full response as string
          return resolve(JSON.stringify(parsed));
        } catch (e) {
          return reject(e);
        }
      });
    });

    req.on('error', (e) => reject(e));
    req.write(body);
    req.end();
  }).catch((err) => {
    // On error, return a readable message so the client sees why parsing failed.
    return `Error: failed to call OpenAI: ${String(err)}`;
  });
}

// Shared handler used by both the Chat Participant and the HTTP /chat endpoint.
async function handleMessageForClient(message, model) {
  if (model) {
    try {
      const https = require('https');
      const body = JSON.stringify({
        model,
        messages: [{ role: 'user', content: (message || '').toString() }],
        temperature: 0.2,
        max_tokens: 512
      });
      const apiKey = process.env.OPENAI_API_KEY || null;
      if (!apiKey) {
        return `Error: OPENAI_API_KEY is required to use custom model selection.`;
      }
      const options = {
        hostname: 'api.openai.com',
        port: 443,
        path: '/v1/chat/completions',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(body),
          'Authorization': `Bearer ${apiKey}`
        }
      };
      return await new Promise((resolve, reject) => {
        const req = https.request(options, (res) => {
          let data = '';
          res.on('data', (chunk) => { data += chunk; });
          res.on('end', () => {
            try {
              const parsed = JSON.parse(data);
              const text = (parsed && parsed.choices && parsed.choices[0] && parsed.choices[0].message && parsed.choices[0].message.content) || null;
              if (text) return resolve(text);
              return resolve(JSON.stringify(parsed));
            } catch (e) {
              return reject(e);
            }
          });
        });
        req.on('error', (e) => reject(e));
        req.write(body);
        req.end();
      });
    } catch (err) {
      return `Error: failed to call model ${model}: ${String(err)}`;
    }
  }
  return await generateReply(message);
}

class ChatApiStatusProvider {
  constructor() {
    this._onDidChangeTreeData = new vscode.EventEmitter();
    this.onDidChangeTreeData = this._onDidChangeTreeData.event;
  }

  refresh() {
    this._onDidChangeTreeData.fire(undefined);
  }

  getTreeItem(element) {
    return element;
  }

  async getChildren(element) {
    if (!element) {
      const status = serverRunning ? 'Running on http://localhost:' + PORT : 'Stopped';
      const icon = serverRunning ? 'circle-filled' : 'circle-outline';
      const item = new vscode.TreeItem(status, vscode.TreeItemCollapsibleState.None);
      item.iconPath = new vscode.ThemeIcon(icon, new vscode.ThemeColor(serverRunning ? 'testing.iconPassed' : 'testing.iconFailed'));
      item.command = {
        command: 'vscodeChatLocalApi.toggleServer',
        title: 'Toggle Server',
        arguments: []
      };
      item.tooltip = 'Click to ' + (serverRunning ? 'stop' : 'start') + ' the Chat API server';
      return [item];
    }
    return [];
  }
}


function startServer(context) {
  if (serverRunning) return;

  server = http.createServer(async (req, res) => {
    const url = req.url || '/';
    const method = req.method || 'GET';

    if (method === 'GET' && url === '/status') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ running: true, port: PORT }));
      return;
    }

    if (method === 'POST' && url === '/chat') {
      let body = '';
      req.on('data', (chunk) => {
        body += chunk.toString();
      });

      req.on('end', async () => {
        try {
          const data = body ? JSON.parse(body) : {};
          const reply = await handleMessageForClient(data.message, data.model);
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ reply }));
        } catch (err) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: String(err) }));
        }
      });
      return;
    }

    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Not found' }));
  });

  server.listen(PORT, () => {
    serverRunning = true;
    updateStatusBar();
    if (treeDataProvider) treeDataProvider.refresh();
    vscode.window.showInformationMessage(`Chat Local API listening on http://localhost:${PORT}`);
  });

  server.on('error', (err) => {
    vscode.window.showErrorMessage(`Chat Local API error: ${err.message}`);
  });
}

function stopServer() {
  if (server && serverRunning) {
    server.close(() => {
      server = null;
      serverRunning = false;
      updateStatusBar();
      if (treeDataProvider) treeDataProvider.refresh();
      vscode.window.showInformationMessage('Chat Local API stopped');
    });
  }
}

function updateStatusBar() {
  if (!statusBarItem) return;
  statusBarItem.text = serverRunning ? '$(radio-tower) Chat API: On' : '$(circle-slash) Chat API: Off';
  statusBarItem.tooltip = 'Toggle the Chat Local API server';
  statusBarItem.command = 'vscodeChatLocalApi.toggleServer';
  statusBarItem.show();
}

function activate(context) {
  const registerCommands = () => {
    const toggle = vscode.commands.registerCommand('vscodeChatLocalApi.toggleServer', () => {
      if (serverRunning) stopServer(); else startServer(context);
    });

    const refresh = vscode.commands.registerCommand('vscodeChatLocalApi.refreshStatus', () => {
      if (treeDataProvider) treeDataProvider.refresh();
      else {
        vscode.window.showInformationMessage('Chat API status view is starting.');
      }
    });

    context.subscriptions.push(toggle, refresh);
  };

  registerCommands();

  statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
  statusBarItem.name = 'Chat Local API';
  updateStatusBar();

  treeDataProvider = new ChatApiStatusProvider();
  treeView = vscode.window.createTreeView('chatLocalApiStatus', {
    treeDataProvider: treeDataProvider,
    showCollapseAll: false
  });

  context.subscriptions.push(statusBarItem, treeView);

  // Register a Chat Participant so the Chat view can invoke this extension
  // directly. If the host doesn't support the Chat API this will safely
  // no-op.
  try {
    if (vscode.chat && typeof vscode.chat.createChatParticipant === 'function') {
      const participant = vscode.chat.createChatParticipant('chatLocalApi.participant',
        async (request, _context, stream, token) => {
          const prompt = request.prompt || '';
          let reply = '';

          if (request.model) {
            try {
              const response = await request.model.sendRequest([
                vscode.LanguageModelChatMessage.User(prompt)
              ], {}, token);
              for await (const fragment of response.text) {
                reply += fragment;
              }
            } catch (e) {
              reply = `Error calling model: ${String(e)}`;
            }
          } else {
            reply = await handleMessageForClient(prompt, token);
          }

          // Stream the result back to the Chat view and return metadata.
          stream.markdown(`\n\`\`\`\n${reply}\n\`\`\`\n`);
          return { metadata: { source: 'chatLocalApi' } };
        }
      );
      context.subscriptions.push(participant);
      chatParticipant = participant;
    }
  } catch (e) {
    // Non-fatal; Chat API may not be available in the user's host.
    console.log('Chat participant not registered:', e && e.message);
  }

  // Start the server automatically and show the status item again after activation.
  startServer(context);
  setTimeout(() => {
    if (statusBarItem) {
      statusBarItem.show();
    }
    if (treeDataProvider) treeDataProvider.refresh();
  }, 500);
}

function deactivate() {
  stopServer();
}

module.exports = { activate, deactivate };
