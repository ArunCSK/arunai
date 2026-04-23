# Google ADK 2.0 -- RAG Agent Demo

A complete demo showing how to:
1. **Build a RAG agent in Python** using Google ADK 2.0 with FAISS + sentence-transformers
2. **Expose it as an HTTP microservice** via `adk api_server`
3. **Call it from Node.js** with both single-turn and streaming modes

---

## Project Structure

```
google-adk-2/
├── adk2-venv/              ← Python virtual environment (created below)
├── requirements.txt        ← All Python dependencies
├── .env.example            ← Copy to .env and fill in your API key
│
├── rag_agent/              ← ADK agent module (loaded by `adk api_server`)
│   ├── agent.py            ← root_agent definition + RAG tools
│   ├── rag_store.py        ← FAISS-based in-memory vector store
│   └── knowledge_base.py  ← Sample documents pre-loaded at startup
│
└── node-client/            ← Node.js client
    ├── package.json
    ├── adkClient.js        ← Reusable ADK HTTP client (run + run_sse)
    ├── demo.js             ← Automated demo (preset questions)
    └── client.js           ← Interactive CLI chat
```

---

## Setup

### 1 — Python: Create & Activate `adk2-venv`

```powershell
# From the project root
python -m venv adk2-venv

# Activate (PowerShell)
.\adk2-venv\Scripts\Activate.ps1

# Install all dependencies
pip install -r requirements.txt
```

### 2 — Configure your API key

```powershell
# Copy the template
copy .env.example .env

# Edit .env and paste your Gemini API key
# GOOGLE_API_KEY=AIza...
```

> Get a free Gemini API key at: https://aistudio.google.com/app/apikey

### 3 — Node.js: Install dependencies

```powershell
cd node-client
npm install
cd ..
```

---

## Running the Demo

### Terminal 1 -- Start the ADK server (choose ONE option)

> [!IMPORTANT]
> `adk api_server` and `adk web` both bind to port 8000 by default.
> Run ONLY ONE at a time. Starting both causes:
> `[Errno 10048] error while attempting to bind on address ('127.0.0.1', 8000)`

```powershell
# Activate venv first (run from project root)
.\adk2-venv\Scripts\Activate.ps1
```

**Option A -- API Server only** (for use with the Node.js client)
```powershell
adk api_server
# Serves REST API at http://localhost:8000
# Auto-discovers rag_agent/agent.py -> root_agent
```

**Option B -- Web UI** (browser-based chat + trace explorer, no Node.js client needed)
```powershell
adk web
# Serves REST API + browser UI at http://localhost:8000
# Open http://localhost:8000 in your browser
```

**Option C -- Run both simultaneously on different ports**
```powershell
# Terminal 1: API server on 8000 (for Node.js client)
adk api_server --port 8000

# Terminal 2: Web UI on 8001 (for browser)
adk web --port 8001
```

### Terminal 2 -- Run the Node.js client (requires Option A or C above)

```powershell
cd node-client

# Option A: Automated demo (fires 7 preset questions, streams output)
npm run demo

# Option B: Interactive chat REPL
npm run chat
# Commands: /exit  /sources  /add  /clear
```

---

## ADK API Endpoints

The ADK server exposes these REST endpoints:

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/run` | Single-turn: send message, get full response |
| `POST` | `/run_sse` | Streaming: response via Server-Sent Events |
| `POST` | `/apps/{app}/users/{uid}/sessions/{sid}` | Create a session |
| `GET`  | `/apps/{app}/users/{uid}/sessions/{sid}` | Get session history |
| `DELETE` | `/apps/{app}/users/{uid}/sessions/{sid}` | Delete session |

### Example `curl` call

```bash
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "rag_agent",
    "user_id": "user-123",
    "session_id": "sess-abc",
    "new_message": {
      "role": "user",
      "parts": [{"text": "What is Google ADK?"}]
    }
  }'
```

---

## How the RAG Pipeline Works

```
User query (Node.js)
       │
       ▼
  ADK API Server  (Python / FastAPI)
       │
       ▼
  LlmAgent (Gemini 2.0 Flash)
       │  decides to call tool
       ▼
  search_knowledge_base(query)
       │
       ▼
  RAGStore.retrieve(query)
    ├── Embed query  →  sentence-transformers (all-MiniLM-L6-v2)
    ├── ANN search   →  FAISS IndexFlatIP
    └── Top-3 chunks returned
       │
       ▼
  Agent generates answer grounded in retrieved context
       │
       ▼
  Streaming response  →  Node.js client prints tokens
```

---

## ADK Tools Available to the Agent

| Tool | What it does |
|------|-------------|
| `search_knowledge_base` | Embeds query → searches FAISS → returns top-3 chunks |
| `add_to_knowledge_base` | Chunks & embeds new text → adds to FAISS at runtime |
| `list_knowledge_sources` | Returns all unique source labels in the store |

---

## Key Dependencies (`requirements.txt`)

| Package | Role |
|---------|------|
| `google-adk` | ADK framework — agent, tools, API server |
| `google-generativeai` | Gemini model access |
| `sentence-transformers` | Local embedding model (no API key needed) |
| `faiss-cpu` | Fast approximate nearest-neighbour search |
| `pypdf` | PDF ingestion (extend the RAG store) |
| `python-dotenv` | Load `.env` config |
| `fastapi` + `uvicorn` | HTTP server used by `adk api_server` |

---

## Extending the Demo

### Add your own documents
```python
# In knowledge_base.py — add to SAMPLE_DOCS:
{"source": "My Docs", "text": "Your content here…"}

# Or at runtime via the Node.js chat:
# /add  →  enter source label  →  enter text
```

### Ingest a PDF
```python
from pypdf import PdfReader
from rag_store import RAGStore

store = RAGStore()
reader = PdfReader("my_doc.pdf")
text = "\n".join(p.extract_text() for p in reader.pages)
store.add_text(text, source="my_doc.pdf")
```

### Switch to a better model
```python
# In agent.py — change:
model="gemini-2.0-flash"
# to:
model="gemini-1.5-pro"   # higher quality
model="gemini-2.5-pro"   # highest quality (preview)
```
