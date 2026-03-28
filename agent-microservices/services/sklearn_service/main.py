"""
=============================================================
PROBLEM 2 — Scikit-learn Classifier Microservice (FastAPI)
=============================================================

ROLE: AI Engineer @ JPMorgan Chase
DIFFICULTY: Easy-Medium

----- PROBLEM STATEMENT -----
Build a REST API that trains a classifier on the Iris dataset and
serves predictions. The API should be retrain-able at runtime.

Expose three endpoints:
  POST /train      — trains the model, returns metrics
  POST /predict    — predicts class for new input
  GET  /features   — returns feature importance scores

EXPECTED INPUT  (/predict):
  { "features": [5.1, 3.5, 1.4, 0.2] }

EXPECTED OUTPUT (/predict):
  { "predicted_class": 0, "class_name": "setosa", "probability": 0.97 }

CONSTRAINTS:
  - Use RandomForestClassifier as the default model.
  - Apply StandardScaler in a Pipeline so the scaler is saved with the model.
  - Return cross-validation F1 score during /train.
  - /predict must return the max class probability.

----- CONCEPTS COVERED (20%) -----
  ✅  FastAPI app skeleton
  ✅  Pydantic request model
  ✅  Dataset loading + class names

----- YOUR TASK (80%) -----
  ❌  Build sklearn Pipeline (scaler + classifier)
  ❌  cross_val_score with cv=5
  ❌  /train endpoint — fit pipeline, return accuracy + f1
  ❌  /predict endpoint — predict + predict_proba
  ❌  /features endpoint — expose feature importances
  ❌  Try swapping RandomForest with SVM, LogisticRegression
      and observe accuracy changes.

----- RUN -----
  pip install -r requirements.txt
  uvicorn main:app --port 8002 --reload

----- HINTS -----
  Hint 1: Pipeline([("scaler", StandardScaler()), ("clf", RandomForestClassifier())])
  Hint 2: cross_val_score(pipeline, X, y, cv=5, scoring='f1_weighted').mean()
  Hint 3: pipeline.predict_proba(X_new)[0].max()
  Hint 4: pipeline.named_steps['clf'].feature_importances_
=============================================================
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from typing import List, Optional
import numpy as np

app = FastAPI(title="Sklearn Classifier Service", version="1.0")

CLASS_NAMES = ["setosa", "versicolor", "virginica"]
FEATURE_NAMES = ["sepal_length", "sepal_width", "petal_length", "petal_width"]

# Global pipeline (trained on demand)
pipeline: Optional[Pipeline] = None

# --------------- Request schemas (PROVIDED) ---------------
class PredictRequest(BaseModel):
    features: List[float]

class TrainRequest(BaseModel):
    model_type: str = "random_forest"  # or "svm", "logistic"
    n_estimators: int = 100            # for RandomForest
    max_depth: Optional[int] = None

# --------------- Build pipeline ---------------
def build_pipeline(config: TrainRequest) -> Pipeline:
    """
    A sklearn Pipeline chains steps sequentially:
      Input → StandardScaler → Classifier → Output
    This prevents data leakage because the scaler is fitted only on
    training data even during cross-validation.
    """
    if config.model_type == "random_forest":
        # Ensemble of decision trees — averages their votes
        clf = RandomForestClassifier(
            n_estimators=config.n_estimators,
            max_depth=config.max_depth,
            random_state=42,
        )
    elif config.model_type == "svm":
        # Finds a hyperplane that maximises margin between classes
        # probability=True enables predict_proba via Platt scaling
        clf = SVC(probability=True, random_state=42)
    elif config.model_type == "logistic":
        # Linear model with sigmoid output — baselines are fast
        clf = LogisticRegression(max_iter=200, random_state=42)
    else:
        raise HTTPException(status_code=400, detail=f"Unknown model_type: {config.model_type}")

    return Pipeline([
        ("scaler", StandardScaler()),   # step 1: normalise features
        ("clf",    clf),                # step 2: classify
    ])

# --------------- Endpoints ---------------
@app.post("/train")
def train(config: TrainRequest = TrainRequest()):
    """
    cross_val_score splits data into 5 folds, trains on 4, scores on 1,
    repeating 5 times. This gives a much more honest accuracy than a
    simple train/test split.
    """
    global pipeline
    iris = load_iris()
    X, y = iris.data, iris.target

    pipeline = build_pipeline(config)

    # 5-fold cross-validation — returns an array of 5 scores
    cv_accuracy = cross_val_score(pipeline, X, y, cv=5, scoring="accuracy").mean()
    cv_f1       = cross_val_score(pipeline, X, y, cv=5, scoring="f1_weighted").mean()

    # Fit on full dataset so /predict uses all available data
    pipeline.fit(X, y)

    return {
        "model_type":    config.model_type,
        "cv_accuracy":   round(float(cv_accuracy), 4),
        "cv_f1_weighted": round(float(cv_f1), 4),
    }

@app.post("/predict")
def predict(req: PredictRequest):
    """
    pipeline.predict_proba returns shape (1, 3) — one probability per class.
    We take the max as the confidence score for the predicted class.
    """
    global pipeline
    if pipeline is None:
        raise HTTPException(status_code=400, detail="Model not trained. POST /train first.")

    X_new      = [req.features]                           # shape (1, 4)
    class_idx  = int(pipeline.predict(X_new)[0])          # integer label
    proba      = pipeline.predict_proba(X_new)[0]         # [p_setosa, p_versicolor, p_virginica]
    confidence = float(proba.max())

    return {
        "predicted_class": class_idx,
        "class_name":      CLASS_NAMES[class_idx],
        "probability":     round(confidence, 4),
        "all_probabilities": {CLASS_NAMES[i]: round(float(p), 4) for i, p in enumerate(proba)},
    }

@app.get("/features")
def feature_importance():
    """
    feature_importances_ is specific to tree-based models.
    It measures how often / how much each feature reduces impurity across all trees.
    """
    global pipeline
    if pipeline is None:
        raise HTTPException(status_code=400, detail="Model not trained. POST /train first.")

    clf = pipeline.named_steps["clf"]
    if not hasattr(clf, "feature_importances_"):
        raise HTTPException(status_code=400, detail=f"{type(clf).__name__} does not support feature_importances_.")

    importances = clf.feature_importances_
    return {
        "feature_importances": {
            name: round(float(score), 4)
            for name, score in zip(FEATURE_NAMES, importances)
        },
        "most_important": FEATURE_NAMES[int(np.argmax(importances))],
    }
