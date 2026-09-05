"""
Check the saved pipeline against the real dataset it was trained on.

Usage:
    1. Download heart.csv (Kaggle: fedesoriano/heart-failure-prediction)
       and place it next to this file.
    2. python evaluate_model.py

It rebuilds the exact same train/test split the notebook used
(test_size=0.20, random_state=42), so the 184 test rows reported below
are rows the model never saw during training.
"""

import os
import warnings

import joblib
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split

warnings.filterwarnings("ignore")

CSV = "heart.csv"
TARGET = "HeartDisease"

if not os.path.exists(CSV):
    raise SystemExit(
        f"{CSV} not found. Download it from Kaggle "
        "(fedesoriano/heart-failure-prediction) and put it in this folder."
    )

df = pd.read_csv(CSV)
print(f"Loaded {CSV}: {df.shape[0]} rows, {df.shape[1]} columns\n")

X = df.drop(columns=[TARGET])
y = df[TARGET]

# Same split as the training notebook, so X_test is genuinely unseen data.
_, X_test, _, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

pipeline = joblib.load(os.path.join("saved_model", "heart_pipeline.pkl"))
y_pred = pipeline.predict(X_test)
y_prob = pipeline.predict_proba(X_test)[:, 1]

print(f"Held-out test rows: {len(X_test)}")
print(f"Accuracy : {accuracy_score(y_test, y_pred):.4f}")
print(f"F1 score : {f1_score(y_test, y_pred):.4f}")
print(f"ROC AUC  : {roc_auc_score(y_test, y_prob):.4f}\n")

tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
print("Confusion matrix")
print(f"  True negatives : {tn}")
print(f"  False positives: {fp}   (healthy, flagged as at risk)")
print(f"  False negatives: {fn}   (at risk, missed -- the dangerous kind)")
print(f"  True positives : {tp}\n")

print(classification_report(y_test, y_pred, target_names=["No disease", "Disease"]))
