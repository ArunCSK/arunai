# Live Coding Practice — AI/ML Engineer (JPMorgan Chase)

> **80/20 Rule:** Each problem gives you ~20% scaffold. You implement the remaining 80%.

---

## Project Layout

```
services/
  nn_scratch/                  ← Problem 1  (port 8001)
  sklearn_service/             ← Problem 2  (port 8002)
  pytorch_service/             ← Problem 3  (port 8003)
  sentence_transformer_service/ ← Problem 4  (port 8004)
  hf_service/                  ← Problem 5  (port 8005)
rag-cli/                       ← Problem 6  (Node.js CLI)
```

---

## Problem Summary

| # | Topic | Key Concept You Implement | Port |
|---|-------|--------------------------|------|
| 1 | Neural Net (NumPy) | Forward pass, cross-entropy, backprop, gradient descent | 8001 |
| 2 | Scikit-learn | Pipeline, cross_val_score, feature_importances | 8002 |
| 3 | PyTorch MLP | nn.Module, DataLoader, training loop, eval mode | 8003 |
| 4 | Sentence-Transformers | Batch encode, cosine similarity, semantic search | 8004 |
| 5 | HuggingFace Transformers | AutoModel tokenize→forward→decode, generate() | 8005 |
| 6 | RAG CLI (Node.js) | Cosine similarity in JS, retrieval pipeline, CLI UX | — |

---

## Quick Start

### Python services (one terminal per service)

```powershell
# Problem 1 — Neural Net from Scratch
cd services\nn_scratch
pip install -r requirements.txt
uvicorn main:app --port 8001 --reload

# Problem 2 — Scikit-learn
cd services\sklearn_service
pip install -r requirements.txt
uvicorn main:app --port 8002 --reload

# Problem 3 — PyTorch
cd services\pytorch_service
pip install -r requirements.txt
uvicorn main:app --port 8003 --reload

# Problem 4 — Sentence-Transformers
cd services\sentence_transformer_service
pip install -r requirements.txt
uvicorn main:app --port 8004 --reload

# Problem 5 — HuggingFace Transformers
cd services\hf_service
pip install -r requirements.txt
uvicorn main:app --port 8005 --reload
```

### RAG CLI (Node.js)

```powershell
cd rag-cli
npm install
node bin/rag.js "What is machine learning?"
node bin/rag.js --top-k 3 "How does PyTorch work?"
```

---

## Testing Each Service (curl)

```bash
# Problem 1
curl -X POST http://localhost:8001/train
curl -X POST http://localhost:8001/predict \
  -H "Content-Type: application/json" \
  -d "{\"features\":[5.1,3.5,1.4,0.2]}"

# Problem 2
curl -X POST http://localhost:8002/train
curl -X POST http://localhost:8002/predict \
  -H "Content-Type: application/json" \
  -d "{\"features\":[5.1,3.5,1.4,0.2]}"
curl http://localhost:8002/features

# Problem 3
curl -X POST http://localhost:8003/train
curl http://localhost:8003/model-info

# Problem 4
curl -X POST http://localhost:8004/search \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"What is deep learning?\"}"

curl -X POST http://localhost:8004/similarity \
  -H "Content-Type: application/json" \
  -d "{\"text_a\":\"PyTorch is great\",\"text_b\":\"I love deep learning\"}"

# Problem 5
curl -X POST http://localhost:8005/classify \
  -H "Content-Type: application/json" \
  -d "{\"texts\":[\"I love this!\",\"This is terrible.\"]}"

curl -X POST http://localhost:8005/summarize \
  -H "Content-Type: application/json" \
  -d "{\"texts\":[\"Machine learning is a field of artificial intelligence...\"]}"
```

---

## Learning Path (80% Self-Exploration)

| Problem | Explore Next |
|---------|-------------|
| 1 — NumPy NN | Batch norm, dropout, Adam (math from scratch) |
| 2 — Sklearn | GridSearchCV, SHAP values, ROC-AUC |
| 3 — PyTorch | LR scheduler, early stopping, CUDA move, DataLoader workers |
| 4 — Sent-Transformers | FAISS ANN index, fine-tuning with triplet loss |
| 5 — HuggingFace | Fine-tuning on custom dataset, ONNX export, quantization |
| 6 — RAG CLI | Chunking strategies, re-ranking, streaming responses, LangChain |

---

## Interview Patterns to Know

1. **Backpropagation** — be able to derive dW for any layer on a whiteboard
2. **Overfitting remedies** — dropout, L2 reg, early stopping, data augmentation
3. **Attention mechanism** — Q, K, V matrices; scaled dot-product attention formula
4. **RAG vs fine-tuning** — when to use which, trade-offs
5. **Microservice design** — stateless vs stateful, health checks, versioning
