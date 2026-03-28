"""
=============================================================
PROBLEM 5 — HuggingFace Transformers Inference Service (FastAPI)
=============================================================

ROLE: AI Engineer @ JPMorgan Chase
DIFFICULTY: Medium-Hard

----- PROBLEM STATEMENT -----
Build an NLP inference microservice powered by HuggingFace Transformers.

Expose two inference capabilities:
  POST /classify   — sentiment classification (positive/negative)
  POST /summarize  — abstractive text summarisation

Both endpoints must:
  - Accept a list of texts for batch inference
  - Return confidence scores
  - Handle errors gracefully (text too long, model not ready, etc.)

EXPECTED INPUT  (/classify):
  { "texts": ["I love working with transformers!", "This is terrible."] }

EXPECTED OUTPUT (/classify):
  {
    "results": [
      {"text": "I love ...", "label": "POSITIVE", "score": 0.999},
      {"text": "This is ...", "label": "NEGATIVE", "score": 0.997}
    ]
  }

CONSTRAINTS:
  - /classify uses  "distilbert-base-uncased-finetuned-sst-2-english"
  - /summarize uses "sshleifer/distilbart-cnn-12-6" (smaller + faster than bart-large)
  - Load both models at startup using AutoTokenizer + AutoModelForXxx.
  - Do NOT use the high-level pipeline() abstraction — use tokenizer + model directly.
  - Truncate inputs at 512 tokens for classify, 1024 for summarize.

----- CONCEPTS COVERED (20%) -----
  ✅  FastAPI skeleton
  ✅  Lifespan model loading (provided shell)
  ✅  Model registry dict
  ✅  Request/response schemas

----- YOUR TASK (80%) -----
  ❌  Load AutoTokenizer + AutoModelForSequenceClassification at startup
  ❌  Load AutoTokenizer + AutoModelForSeq2SeqLM at startup
  ❌  /classify — tokenize → forward → softmax → id2label
  ❌  /summarize — tokenize → model.generate() → decode
  ❌  Bonus: add a GET /models endpoint listing loaded models + memory usage
  ❌  Bonus: add token-level attention visualization for /classify

----- RUN -----
  pip install -r requirements.txt
  uvicorn main:app --port 8005 --reload
  (downloads ~250MB models on first run)

----- HINTS -----
  Hint 1: AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
  Hint 2: inputs = tokenizer(texts, return_tensors="pt", truncation=True, padding=True, max_length=512)
  Hint 3: with torch.no_grad(): logits = model(**inputs).logits;  probs = F.softmax(logits, dim=-1)
  Hint 4: label = model.config.id2label[predicted_class_id]
  Hint 5: summary_ids = model.generate(inputs["input_ids"], max_new_tokens=100, num_beams=4)
           decoded = tokenizer.batch_decode(summary_ids, skip_special_tokens=True)
=============================================================
"""

import torch
import torch.nn.functional as F
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
from typing import List, Optional
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    AutoModelForSeq2SeqLM,
)

# --------------- Model registry (keys loaded at startup) ---------------
models = {}
# Expected structure after your implementation:
#   models["clf_tokenizer"]   = AutoTokenizer(...)
#   models["clf_model"]       = AutoModelForSequenceClassification(...)
#   models["sum_tokenizer"]   = AutoTokenizer(...)
#   models["sum_model"]       = AutoModelForSeq2SeqLM(...)

CLASSIFY_MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"
SUMMARIZE_MODEL_NAME = "sshleifer/distilbart-cnn-12-6"

# --------------- Startup (shell provided — you fill the loading) ---------------
@asynccontextmanager
async def lifespan(app):
    """
    YOUR TASK:
    1. Load clf tokenizer + model → store in models dict
    2. Load summarization tokenizer + model → store in models dict
    3. Set both models to eval() mode
    """
    print("Loading classification model...")
    # AutoTokenizer converts raw strings → input_ids, attention_mask tensors
    models["clf_tokenizer"] = AutoTokenizer.from_pretrained(CLASSIFY_MODEL_NAME)
    # AutoModelForSequenceClassification has a classification head on top of the encoder
    models["clf_model"]     = AutoModelForSequenceClassification.from_pretrained(CLASSIFY_MODEL_NAME)
    models["clf_model"].eval()  # no dropout during inference

    print("Loading summarization model...")
    # AutoModelForSeq2SeqLM has both encoder (reads input) + decoder (generates output)
    models["sum_tokenizer"] = AutoTokenizer.from_pretrained(SUMMARIZE_MODEL_NAME)
    models["sum_model"]     = AutoModelForSeq2SeqLM.from_pretrained(SUMMARIZE_MODEL_NAME)
    models["sum_model"].eval()

    print("All models ready.")
    yield
    models.clear()

app = FastAPI(title="HuggingFace Inference Service", version="1.0", lifespan=lifespan)

# --------------- Request schemas ---------------
class ClassifyRequest(BaseModel):
    texts: List[str]

class SummarizeRequest(BaseModel):
    texts: List[str]
    max_new_tokens: int = 100
    num_beams: int = 4

# --------------- Endpoints ---------------
@app.post("/classify")
def classify(req: ClassifyRequest):
    """
    Full tokenize → forward → softmax → label pipeline (manual, no pipeline()):

    1. Tokenizer: converts text strings to token IDs.
       return_tensors="pt"  → PyTorch tensors
       padding=True         → pads shorter sequences to the same length
       truncation=True      → cuts texts longer than max_length tokens
       max_length=512       → DistilBERT's context window

    2. Forward pass (model(**inputs)):
       Runs the transformer layers. .logits is the raw pre-softmax output.

    3. Softmax: converts logits to probabilities summing to 1.

    4. id2label: the model's config maps 0→"NEGATIVE", 1→"POSITIVE" etc.
    """
    if "clf_model" not in models:
        raise HTTPException(status_code=503, detail="Classification model not loaded.")

    tokenizer = models["clf_tokenizer"]
    clf_model  = models["clf_model"]

    inputs = tokenizer(
        req.texts,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512,
    )

    with torch.no_grad():
        logits = clf_model(**inputs).logits          # (N, num_labels)
    probs = F.softmax(logits, dim=-1)                # (N, num_labels)

    results = []
    for i, text in enumerate(req.texts):
        pred_class  = int(probs[i].argmax().item())
        label       = clf_model.config.id2label[pred_class]
        score       = round(float(probs[i][pred_class].item()), 4)
        results.append({"text": text, "label": label, "score": score})

    return {"results": results}

@app.post("/summarize")
def summarize(req: SummarizeRequest):
    """
    Summarization uses an encoder-decoder (seq2seq) architecture:
    - Encoder reads the full input text and builds context representations.
    - Decoder autoregressively generates the summary token by token.

    model.generate() handles the decoding loop:
      num_beams > 1 → beam search: keeps top-N candidate sequences at each step,
                      which produces better quality summaries than greedy (num_beams=1).

    tokenizer.batch_decode() converts token ID tensors back to strings.
    skip_special_tokens=True removes <pad>, <eos>, etc.
    """
    if "sum_model" not in models:
        raise HTTPException(status_code=503, detail="Summarization model not loaded.")

    tokenizer  = models["sum_tokenizer"]
    sum_model  = models["sum_model"]

    results = []
    for text in req.texts:
        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=1024,
        )
        with torch.no_grad():
            summary_ids = sum_model.generate(
                inputs["input_ids"],
                max_new_tokens=req.max_new_tokens,
                num_beams=req.num_beams,
                early_stopping=True,
            )
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        results.append({"original": text, "summary": summary})

    return {"results": results}

@app.get("/models")
def list_models():
    """
    Reports which models are currently loaded.
    Useful for health checks and observability in production.
    """
    loaded = [k for k in models if "model" in k]
    param_counts = {}
    for k in loaded:
        m = models[k]
        param_counts[k] = sum(p.numel() for p in m.parameters())
    return {"loaded_models": loaded, "parameter_counts": param_counts}
