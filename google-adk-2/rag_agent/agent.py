"""
agent.py  ── Google ADK 2.0 RAG Agent entry point
──────────────────────────────────────────────────
This module is loaded by `adk api_server` / `adk web` automatically.
ADK looks for a module-level variable named `root_agent`.
"""

import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

from .rag_store import RAGStore
from .knowledge_base import SAMPLE_DOCS

# ── Environment ───────────────────────────────────────────────────────────────
load_dotenv()  # reads .env from cwd

# ── Bootstrap RAG store (loaded once at import time) ─────────────────────────
print("[LOAD]  Loading RAG knowledge base...")
_rag = RAGStore()
n = _rag.add_documents(SAMPLE_DOCS)
print(f"[OK]  RAG store ready -- {n} chunks indexed from {len(SAMPLE_DOCS)} documents.")


# ── ADK Tools ─────────────────────────────────────────────────────────────────

def search_knowledge_base(query: str) -> str:
    """
    Search the internal knowledge base for information relevant to the query.

    Use this tool whenever the user asks a question that might be answered by
    the stored documents. Always cite the source(s) returned.

    Args:
        query: The user's question or search term.

    Returns:
        Relevant text passages with their source labels.
    """
    context = _rag.retrieve_as_context(query, top_k=3)
    return context


def add_to_knowledge_base(text: str, source: str = "user-provided") -> str:
    """
    Add new text to the knowledge base at runtime.

    Use this when the user wants to teach the agent new information.

    Args:
        text:   The text content to store.
        source: A label identifying where the text came from.

    Returns:
        Confirmation message with the number of chunks stored.
    """
    n = _rag.add_text(text, source=source)
    return f"[OK] Added {n} chunk(s) from '{source}' to the knowledge base."


def list_knowledge_sources() -> str:
    """
    Return a deduplicated list of all document sources in the knowledge base.

    Returns:
        A newline-separated list of source names.
    """
    if not _rag._chunks:
        return "The knowledge base is empty."
    sources = sorted(set(c.source for c in _rag._chunks))
    return "Knowledge base sources:\n" + "\n".join(f"  - {s}" for s in sources)


# ── Agent Definition ──────────────────────────────────────────────────────────
SYSTEM_PROMPT = """
You are **ADK RAG Assistant**, a helpful AI agent powered by Google ADK 2.0.

You have access to an internal knowledge base via the `search_knowledge_base` tool.

## How to respond:
1. For every factual question, ALWAYS call `search_knowledge_base` first.
2. If the retrieved context is relevant, base your answer on it and cite the source.
3. If the context is not helpful, say so honestly and answer from general knowledge.
4. Keep answers concise but complete.
5. If the user wants to add information, use `add_to_knowledge_base`.
6. If asked what you know about, call `list_knowledge_sources`.

You are running as a microservice exposed via the ADK API server, callable from
any HTTP client including Node.js.
""".strip()

root_agent = LlmAgent(
    name="rag_assistant",
    model="gemini-flash-latest",   # stable alias: always the current recommended Flash model
    description="A RAG-powered assistant that answers questions from a knowledge base.",
    instruction=SYSTEM_PROMPT,
    tools=[
        FunctionTool(search_knowledge_base),
        FunctionTool(add_to_knowledge_base),
        FunctionTool(list_knowledge_sources),
    ],
)
