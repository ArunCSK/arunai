"""
=============================================================
PROBLEM 3 — PyTorch MLP Training Loop (FastAPI)
=============================================================

ROLE: AI Engineer @ JPMorgan Chase
DIFFICULTY: Medium

----- PROBLEM STATEMENT -----
Build a microservice that defines a Multi-Layer Perceptron (MLP)
in PyTorch, trains it on the Iris dataset, and serves predictions.

Endpoints:
  POST /train      — trains the model, returns loss curve + accuracy
  POST /predict    — returns predicted class + confidence
  GET  /model-info — returns number of parameters + architecture string

EXPECTED INPUT  (/predict):
  { "features": [5.1, 3.5, 1.4, 0.2] }

EXPECTED OUTPUT (/predict):
  { "predicted_class": 0, "class_name": "setosa", "confidence": 0.98 }

CONSTRAINTS:
  - Define IrisNet as a proper nn.Module subclass.
  - Use CrossEntropyLoss and Adam optimiser.
  - Training must use mini-batches via DataLoader (batch_size=16).
  - Model must be in eval() mode during inference.
  - Return EVERY epoch's loss in /train for plotting.

----- CONCEPTS COVERED (20%) -----
  ✅  FastAPI skeleton
  ✅  IrisDataset (torch.utils.data.Dataset) — provided
  ✅  Model state holder
  ✅  Data loading (Iris) + tensor conversion helpers

----- YOUR TASK (80%) -----
  ❌  IrisNet — define __init__ and forward with nn.Linear + ReLU
  ❌  /train — create DataLoader, loss, optimiser, training loop
  ❌  /predict — eval mode, softmax, argmax
  ❌  /model-info — count parameters, print architecture
  ❌  Bonus: add a learning rate scheduler (StepLR)
  ❌  Bonus: add early stopping if val_loss stops improving

----- RUN -----
  pip install -r requirements.txt
  uvicorn main:app --port 8003 --reload

----- HINTS -----
  Hint 1: class IrisNet(nn.Module): def __init__(self): super().__init__(); self.fc1 = nn.Linear(4,16); ...
  Hint 2: for epoch in range(epochs): for X_b, y_b in loader: optimizer.zero_grad(); loss = criterion(model(X_b), y_b); loss.backward(); optimizer.step()
  Hint 3: with torch.no_grad(): outputs = model(tensor); probs = F.softmax(outputs, dim=1)
  Hint 4: sum(p.numel() for p in model.parameters() if p.requires_grad)
=============================================================
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from typing import List, Optional
import numpy as np

app = FastAPI(title="PyTorch MLP Service", version="1.0")

CLASS_NAMES = ["setosa", "versicolor", "virginica"]

# Global model state
net: Optional[nn.Module] = None
scaler = StandardScaler()

# --------------- Dataset wrapper (PROVIDED) ---------------
class IrisDataset(Dataset):
    def __init__(self, X: np.ndarray, y: np.ndarray):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.long)

    def __len__(self):
        return len(self.y)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

# --------------- Network definition ---------------
class IrisNet(nn.Module):
    """
    nn.Module is PyTorch's base class for all neural networks.

    Architecture:
      Input (4) → Linear → ReLU → Linear → ReLU → Output (3 logits)
                    ↑ 16 neurons       ↑ 8 neurons

    We define layers in __init__ and wire them in forward().
    nn.Linear(in, out) = learnable weight matrix W (in×out) + bias b.
    ReLU(x) = max(0, x) — introduces non-linearity so we can learn complex patterns.
    Final layer outputs RAW LOGITS (not probabilities). CrossEntropyLoss handles softmax internally.
    """
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(4, 16)   # 4 features → 16 hidden neurons
        self.fc2 = nn.Linear(16, 8)   # 16 → 8
        self.fc3 = nn.Linear(8, 3)    # 8 → 3 classes (logits)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = F.relu(self.fc1(x))   # hidden layer 1
        x = F.relu(self.fc2(x))   # hidden layer 2
        return self.fc3(x)         # output logits — NO activation here

# --------------- Request schemas ---------------
class PredictRequest(BaseModel):
    features: List[float]

class TrainRequest(BaseModel):
    epochs: int = 100
    learning_rate: float = 0.001
    batch_size: int = 16

# --------------- Endpoints ---------------
@app.post("/train")
def train(cfg: TrainRequest = TrainRequest()):
    """
    Key PyTorch training loop pattern (memorise this):
      for batch in DataLoader:
          optimizer.zero_grad()   ← clear stale gradients from last step
          output = model(X)       ← forward pass
          loss   = criterion(output, y)
          loss.backward()         ← compute all gradients via autograd
          optimizer.step()        ← update weights: W -= lr * dL/dW
    """
    global net, scaler
    iris = load_iris()
    X = scaler.fit_transform(iris.data)
    y = iris.target

    dataset = IrisDataset(X, y)
    loader  = DataLoader(dataset, batch_size=cfg.batch_size, shuffle=True)

    net       = IrisNet()
    criterion = nn.CrossEntropyLoss()   # softmax + NLLLoss combined
    optimizer = torch.optim.Adam(net.parameters(), lr=cfg.learning_rate)

    loss_history = []
    net.train()   # enable dropout/batchnorm training behaviour (good habit)

    for epoch in range(cfg.epochs):
        epoch_loss = 0.0
        for X_batch, y_batch in loader:
            optimizer.zero_grad()                   # 1. clear old gradients
            outputs = net(X_batch)                   # 2. forward
            loss    = criterion(outputs, y_batch)    # 3. loss
            loss.backward()                          # 4. backprop
            optimizer.step()                         # 5. update weights
            epoch_loss += loss.item()

        avg_loss = epoch_loss / len(loader)
        loss_history.append(round(avg_loss, 6))

    # Final accuracy
    net.eval()
    with torch.no_grad():
        all_X   = torch.tensor(X, dtype=torch.float32)
        logits  = net(all_X)
        preds   = logits.argmax(dim=1).numpy()
    accuracy = float(np.mean(preds == y))

    return {
        "final_loss":     loss_history[-1],
        "final_accuracy": round(accuracy, 4),
        "loss_curve":     loss_history,
    }

@app.post("/predict")
def predict(req: PredictRequest):
    """
    Important: net.eval() switches off dropout/batchnorm randomness.
    torch.no_grad() disables gradient tracking — faster + less memory.
    F.softmax converts raw logits → class probabilities summing to 1.
    """
    global net, scaler
    if net is None:
        raise HTTPException(status_code=400, detail="Model not trained. POST /train first.")

    net.eval()
    with torch.no_grad():
        x      = torch.tensor(scaler.transform([req.features]), dtype=torch.float32)
        logits = net(x)                           # (1, 3) raw logits
        probs  = F.softmax(logits, dim=1)[0]      # (3,) probabilities
        cls    = int(probs.argmax().item())

    return {
        "predicted_class":  cls,
        "class_name":       CLASS_NAMES[cls],
        "confidence":       round(float(probs[cls].item()), 4),
        "all_probabilities": {CLASS_NAMES[i]: round(float(p), 4) for i, p in enumerate(probs)},
    }

@app.get("/model-info")
def model_info():
    """
    str(net) calls IrisNet.__repr__() — PyTorch prints the full layer tree.
    total_params counts every learnable scalar (weights + biases).
    """
    global net
    trained = net is not None
    if not trained:
        return {"trained": False, "architecture": None, "total_params": 0}

    total_params = sum(p.numel() for p in net.parameters() if p.requires_grad)
    return {
        "trained":      True,
        "architecture": str(net),
        "total_params": total_params,
    }
