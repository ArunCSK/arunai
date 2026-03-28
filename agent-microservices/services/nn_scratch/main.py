"""
=============================================================
PROBLEM 1 — Neural Network from Scratch (NumPy + FastAPI)
=============================================================

ROLE: AI Engineer @ JPMorgan Chase
DIFFICULTY: Medium

----- PROBLEM STATEMENT -----
You are asked to implement a 2-layer neural network using ONLY NumPy
to classify Iris flowers into 3 classes.

Expose two REST endpoints:
  POST /train   — trains the network and returns final loss + accuracy
  POST /predict — accepts 4 features, returns predicted class index

EXPECTED INPUT  (/predict):
  { "features": [5.1, 3.5, 1.4, 0.2] }

EXPECTED OUTPUT (/predict):
  { "predicted_class": 0, "class_name": "setosa" }

CONSTRAINTS:
  - No PyTorch, no TensorFlow, no sklearn models.
  - Only NumPy for the math, sklearn only to load the dataset.
  - 2 hidden layers max.
  - Must train in < 30 seconds on CPU.

----- CONCEPTS COVERED (20%) -----
  ✅  FastAPI app skeleton
  ✅  Dataset loading (Iris)
  ✅  Weight initialisation
  ✅  Sigmoid activation (provided)
  ✅  Softmax (provided)

----- YOUR TASK (80%) -----
  ❌  forward()   — matrix multiply + activations
  ❌  loss()      — cross-entropy loss
  ❌  backward()  — gradients via chain rule
  ❌  update()    — gradient descent weight update
  ❌  /train endpoint — training loop (fill TODOs)
  ❌  /predict endpoint — run forward, argmax (fill TODOs)

----- RUN -----
  pip install -r requirements.txt
  uvicorn main:app --port 8001 --reload

----- HINTS (read only when stuck) -----
  Hint 1: forward pass formula  →  Z = X @ W + b;  A = activation(Z)
  Hint 2: cross-entropy loss    →  -mean(sum(Y_onehot * log(A_out), axis=1))
  Hint 3: output layer delta    →  dZ = A_out - Y_onehot
  Hint 4: hidden layer delta    →  dZ = (dZ_next @ W_next.T) * sigmoid_prime(Z)
=============================================================
"""

import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.datasets import load_iris
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from typing import List

app = FastAPI(title="Neural Net from Scratch", version="1.0")

# --------------- Activation helpers (PROVIDED) ---------------
def sigmoid(z: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-z))

def sigmoid_prime(z: np.ndarray) -> np.ndarray:
    s = sigmoid(z)
    return s * (1 - s)

def softmax(z: np.ndarray) -> np.ndarray:
    exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
    return exp_z / exp_z.sum(axis=1, keepdims=True)

# --------------- Network state (global, simple for practice) ---------------
model = {}          # will hold W1, b1, W2, b2
scaler = StandardScaler()
CLASS_NAMES = ["setosa", "versicolor", "virginica"]

# --------------- Weight initialisation (PROVIDED) ---------------
def init_weights(input_dim: int, hidden_dim: int, output_dim: int):
    np.random.seed(42)
    W1 = np.random.randn(input_dim, hidden_dim) * 0.01
    b1 = np.zeros((1, hidden_dim))
    W2 = np.random.randn(hidden_dim, output_dim) * 0.01
    b2 = np.zeros((1, output_dim))
    return W1, b1, W2, b2

# --------------- Forward pass ---------------
def forward(X: np.ndarray) -> dict:
    """
    How it works:
    ┌─────────┐   Z1=X@W1+b1   ┌──────────┐   Z2=A1@W2+b2   ┌──────────┐
    │ Input X │ ──────────────► │ Hidden A1│ ──────────────► │ Output A2│
    │ (N x 4) │   sigmoid(Z1)  │ (N x 8)  │   softmax(Z2)  │ (N x 3)  │
    └─────────┘                 └──────────┘                 └──────────┘
    We cache Z1 and A1 because backward() needs them to compute gradients.
    """
    W1, b1, W2, b2 = model["W1"], model["b1"], model["W2"], model["b2"]

    Z1 = X @ W1 + b1          # (N, 8) — pre-activation hidden layer
    A1 = sigmoid(Z1)           # (N, 8) — hidden layer output
    Z2 = A1 @ W2 + b2          # (N, 3) — pre-activation output layer
    A2 = softmax(Z2)           # (N, 3) — class probabilities (sum to 1)

    return {"Z1": Z1, "A1": A1, "Z2": Z2, "A2": A2}

# --------------- Cross-entropy loss ---------------
def compute_loss(A2: np.ndarray, Y_onehot: np.ndarray) -> float:
    """
    Categorical cross-entropy: measures how far our predicted probabilities
    are from the ground truth one-hot labels.
      loss = -mean( sum( Y * log(A2), axis=1 ) )
    The 1e-8 prevents log(0) which would be -inf.
    """
    return -np.mean(np.sum(Y_onehot * np.log(A2 + 1e-8), axis=1))

# --------------- Backward pass (backpropagation) ---------------
def backward(X: np.ndarray, Y_onehot: np.ndarray, cache: dict, learning_rate: float = 0.1):
    """
    Chain rule applied layer by layer from output → input.

    OUTPUT LAYER gradient:
      dZ2 = A2 - Y   ← because softmax + cross-entropy derivative simplifies to this
      dW2 = A1ᵀ @ dZ2 / m
      db2 = mean(dZ2)

    HIDDEN LAYER gradient:
      dA1 = dZ2 @ W2ᵀ          ← propagate error back through W2
      dZ1 = dA1 * σ'(Z1)       ← multiply by sigmoid derivative (element-wise)
      dW1 = Xᵀ @ dZ1 / m
      db1 = mean(dZ1)

    We divide by m (batch size) so learning_rate is independent of dataset size.
    """
    m = X.shape[0]
    A1, A2, Z1 = cache["A1"], cache["A2"], cache["Z1"]

    # Output layer
    dZ2 = A2 - Y_onehot                     # (N, 3)
    dW2 = A1.T @ dZ2 / m                    # (8, 3)
    db2 = np.mean(dZ2, axis=0, keepdims=True)  # (1, 3)

    # Hidden layer
    dA1 = dZ2 @ model["W2"].T               # (N, 8)
    dZ1 = dA1 * sigmoid_prime(Z1)           # (N, 8) — element-wise gate
    dW1 = X.T @ dZ1 / m                     # (4, 8)
    db1 = np.mean(dZ1, axis=0, keepdims=True)  # (1, 8)

    # Gradient descent update (subtract because we minimise loss)
    model["W2"] -= learning_rate * dW2
    model["b2"] -= learning_rate * db2
    model["W1"] -= learning_rate * dW1
    model["b1"] -= learning_rate * db1

# --------------- Endpoints ---------------
@app.post("/train")
def train(epochs: int = 1000, learning_rate: float = 0.1):
    """
    Full training loop:
      for each epoch → forward → compute_loss → backward (updates weights)
    Returns the final loss and training accuracy.
    """
    global model, scaler
    iris = load_iris()
    X_raw, y = iris.data, iris.target

    # Standardise: zero mean, unit variance — critical for gradient stability
    X = scaler.fit_transform(X_raw)

    # One-hot encode labels: [0,1,2] → [[1,0,0],[0,1,0],[0,0,1]]
    enc = OneHotEncoder(sparse_output=False)
    Y_onehot = enc.fit_transform(y.reshape(-1, 1))   # (150, 3)

    # Initialise weights: input=4, hidden=8, output=3
    W1, b1, W2, b2 = init_weights(4, 8, 3)
    model.update({"W1": W1, "b1": b1, "W2": W2, "b2": b2})

    # Training loop
    loss_history = []
    for epoch in range(epochs):
        cache = forward(X)
        loss  = compute_loss(cache["A2"], Y_onehot)
        backward(X, Y_onehot, cache, learning_rate)
        loss_history.append(round(float(loss), 6))
        if epoch % 100 == 0:
            print(f"Epoch {epoch:4d} | Loss: {loss:.4f}")

    # Accuracy: compare argmax of predictions to true labels
    final_cache = forward(X)
    preds    = np.argmax(final_cache["A2"], axis=1)
    accuracy = float(np.mean(preds == y))

    return {
        "final_loss": loss_history[-1],
        "accuracy":   round(accuracy, 4),
        "epochs_run": epochs,
    }

@app.post("/predict")
def predict(body: dict):
    """
    Scale → forward → argmax.
    The scaler.transform ensures the same normalisation as training.
    """
    if not model:
        return {"error": "Model not trained. Call POST /train first."}

    features = np.array(body["features"]).reshape(1, -1)   # (1, 4)
    X_scaled = scaler.transform(features)                   # normalise
    cache    = forward(X_scaled)
    class_idx = int(np.argmax(cache["A2"], axis=1)[0])

    return {
        "predicted_class": class_idx,
        "class_name":      CLASS_NAMES[class_idx],
        "probabilities":   [round(float(p), 4) for p in cache["A2"][0]],
    }
