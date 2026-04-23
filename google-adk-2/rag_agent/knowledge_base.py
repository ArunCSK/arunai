"""
knowledge_base.py  ── Sample documents pre-loaded into the RAG store
──────────────────────────────────────────────────────────────────────
Edit or extend SAMPLE_DOCS to customise what the agent knows about.
"""

SAMPLE_DOCS = [
    {
        "source": "Google ADK Overview",
        "text": (
            "The Google Agent Development Kit (ADK) is an open-source, code-first Python "
            "framework for building, evaluating, and deploying AI agents. "
            "ADK makes it easy to get started, but is designed to support the "
            "full complexity needed for production-ready agentic systems. "
            "ADK is model-agnostic (works with Gemini, Claude, GPT-4, Llama, etc.) and "
            "deployment-agnostic (runs locally, on Cloud Run, or Vertex AI Agent Engine)."
        ),
    },
    {
        "source": "ADK Core Concepts",
        "text": (
            "An ADK Agent is defined by three things: a model (the LLM powering the agent), "
            "a set of tools (Python functions the agent can call), and instructions "
            "(a system prompt that shapes the agent's behaviour). "
            "Tools are plain Python functions decorated with `@tool` or passed directly. "
            "ADK ships with built-in tools for Google Search, code execution, and more."
        ),
    },
    {
        "source": "ADK RAG Pattern",
        "text": (
            "Retrieval-Augmented Generation (RAG) is a technique where an agent retrieves "
            "relevant documents from a knowledge base before generating a response. "
            "In ADK you implement RAG as a custom tool: the tool receives the user query, "
            "calls a vector store (e.g. FAISS, Vertex AI RAG Engine), and returns the "
            "top-k relevant passages as a string. The agent then conditions its answer "
            "on that retrieved context."
        ),
    },
    {
        "source": "ADK API Server",
        "text": (
            "Running `adk api_server` in your project directory starts a FastAPI-based "
            "HTTP server (default port 8000). It exposes two main endpoints: "
            "POST /run for single-turn request/response, and "
            "POST /run_sse for streaming via Server-Sent Events. "
            "Any HTTP client (Node.js, curl, Python requests) can call these endpoints "
            "to interact with your agent without needing the ADK Python library."
        ),
    },
    {
        "source": "Node.js + ADK Integration",
        "text": (
            "A Node.js application can talk to an ADK agent by sending HTTP POST requests "
            "to the ADK API server. The request body must include: app_name (your agent "
            "module name), user_id, session_id, and a message object containing the "
            "user's text. The response is a JSON array of events; look for "
            "event.content.parts[0].text to find the final assistant reply."
        ),
    },
    {
        "source": "ADK Multi-Agent Systems",
        "text": (
            "ADK supports multi-agent architectures via sub-agents and agent-as-tool. "
            "An orchestrator agent can delegate specialised tasks to sub-agents. "
            "Common patterns: sequential pipeline (agent A calls agent B), "
            "parallel fan-out (orchestrator calls multiple sub-agents concurrently), "
            "and hierarchical (nested coordinators). "
            "ADK's LlmAgent class handles all routing automatically when sub-agents "
            "are registered in the `sub_agents` parameter."
        ),
    },
]
