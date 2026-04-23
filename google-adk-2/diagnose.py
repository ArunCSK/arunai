"""
diagnose.py -- Standalone diagnostic for the ADK RAG agent stack.
Run this from the project root WITH the venv active:

    python diagnose.py

It tests each layer independently so you can pinpoint the 500 error.
"""

import sys
import os

SEP = "-" * 60

def section(title):
    print(f"\n{SEP}")
    print(f"  {title}")
    print(SEP)

# ── 1. Python version ─────────────────────────────────────────────────────────
section("1. Python version")
print(f"  {sys.version}")

# ── 2. Environment / API key ──────────────────────────────────────────────────
section("2. Environment (.env)")
try:
    from dotenv import load_dotenv
    load_dotenv()
    key = os.environ.get("GOOGLE_API_KEY", "")
    if not key or key == "your_gemini_api_key_here":
        print("  [FAIL] GOOGLE_API_KEY is missing or still set to placeholder!")
        print("         Edit .env and paste your key from https://aistudio.google.com/app/apikey")
    else:
        masked = key[:8] + "..." + key[-4:]
        print(f"  [OK]   GOOGLE_API_KEY found: {masked}")
except ImportError:
    print("  [FAIL] python-dotenv not installed. Run: pip install python-dotenv")

# ── 3. sentence-transformers ──────────────────────────────────────────────────
section("3. sentence-transformers import")
try:
    from sentence_transformers import SentenceTransformer
    print("  [OK]   sentence-transformers imported")
    print("         Loading model all-MiniLM-L6-v2 (may download ~80 MB first run)...")
    m = SentenceTransformer("all-MiniLM-L6-v2")
    v = m.encode(["test"], normalize_embeddings=True)
    print(f"  [OK]   Model loaded. Embedding dim = {v.shape[1]}")
except Exception as e:
    print(f"  [FAIL] {e}")

# ── 4. FAISS ──────────────────────────────────────────────────────────────────
section("4. FAISS import")
try:
    import faiss
    idx = faiss.IndexFlatIP(384)
    print(f"  [OK]   faiss-cpu imported. Version: {faiss.__version__}")
except Exception as e:
    print(f"  [FAIL] {e}")

# ── 5. RAGStore end-to-end ────────────────────────────────────────────────────
section("5. RAGStore (embed + index + retrieve)")
try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "rag_agent"))
    from rag_store import RAGStore
    store = RAGStore()
    n = store.add_text("Google ADK is an agent development framework.", source="test")
    print(f"  [OK]   Added {n} chunk(s)")
    result = store.retrieve_as_context("What is ADK?", top_k=1)
    print(f"  [OK]   Retrieved: {result[:80]}...")
except Exception as e:
    print(f"  [FAIL] {e}")
    import traceback; traceback.print_exc()

# ── 6. google-adk import ──────────────────────────────────────────────────────
section("6. google-adk import")
try:
    from google.adk.agents import LlmAgent
    from google.adk.tools import tool
    print("  [OK]   google.adk imported successfully")
except Exception as e:
    print(f"  [FAIL] {e}")

# ── 7. Gemini API connectivity ────────────────────────────────────────────────
section("7. Gemini API connectivity (live call)")
try:
    import google.generativeai as genai
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY", ""))
    model = genai.GenerativeModel("gemini-2.0-flash")
    resp = model.generate_content("Reply with exactly: OK")
    print(f"  [OK]   Gemini response: {resp.text.strip()}")
except Exception as e:
    print(f"  [FAIL] {e}")

# ── 8. agent.py root_agent load ───────────────────────────────────────────────
section("8. agent.py root_agent load")
try:
    os.chdir(os.path.join(os.path.dirname(__file__), "rag_agent"))
    import importlib.util
    spec = importlib.util.spec_from_file_location("agent", "agent.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    agent = getattr(mod, "root_agent", None)
    if agent:
        print(f"  [OK]   root_agent loaded: name={agent.name}, model={agent.model}")
    else:
        print("  [FAIL] root_agent variable not found in agent.py")
except Exception as e:
    print(f"  [FAIL] {e}")
    import traceback; traceback.print_exc()

print(f"\n{SEP}")
print("  Diagnostics complete.")
print(SEP)
