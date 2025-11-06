"""
src/train_model.py

Train a classifier for the Projeto_C318 dataset.

Expected input:
  - data/processed/matches_clean.csv (or pass --input)

What it does:
  - Loads CSV
  - Splits into train/test
  - Builds a sklearn ColumnTransformer + Pipeline (scaling + encoding)
  - Runs GridSearchCV over LogisticRegression and RandomForestClassifier
  - Evaluates on hold-out test set (accuracy, precision, recall, f1, roc_auc)
  - Saves best pipeline and metrics to models/

Usage example:
  python src/train_model.py --input data/processed/matches_clean.csv --out models --target radiant_win
"""

import argparse
import json
import os
from pathlib import Path
from typing import Tuple, List, Dict
import ast
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score)
from sklearn.model_selection import GridSearchCV, train_test_split, StratifiedKFold, GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

os.environ["LOKY_MAX_CPU_COUNT"] = "4"
# -------------------------
# Helpers
# -------------------------

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError(f"Loaded dataframe is empty: {path}")
    return df


def safe_eval_list(val):
    if isinstance(val, str):
        try:
            parsed = ast.literal_eval(val)
            if isinstance(parsed, list):
                return parsed
        except Exception:
            pass
    return val


def expand_hero_lists(df: pd.DataFrame) -> pd.DataFrame:
    for side in ["radiant", "dire"]:
        col = f"{side}_team_sorted"
        if col in df.columns:
            df[[f"{col}_{i}" for i in range(5)]] = pd.DataFrame(
                df[col].tolist(), index=df.index)
            df = df.drop(columns=[col])
    return df


def split_X_y(df: pd.DataFrame, target: str) -> Tuple[pd.DataFrame, pd.Series]:
    if target not in df.columns:
        raise KeyError(
            f"Target column '{target}' not found in dataframe columns.")
    X = df.drop(columns=[target])
    y = df[target].astype(int)
    return X, y


def choose_feature_types(X: pd.DataFrame) -> Tuple[List[str], List[str]]:
    """
    Heuristic to split numeric vs categorical features.
    Adjust if your dataset has special columns (IDs, timestamps) to drop.
    """
    # Drop clearly-identifiers if present
    id_cols = [c for c in ["match_id", "match_seq_num",
                           "start_time"] if c in X.columns]
    if id_cols:
        X = X.drop(columns=id_cols)
    numeric_cols = X.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = X.select_dtypes(exclude=['number']).columns.tolist()
    return numeric_cols, categorical_cols


def build_preprocessor(numeric_cols: List[str], categorical_cols: List[str]) -> ColumnTransformer:
    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])
    transformers = []
    if numeric_cols:
        transformers.append(("num", numeric_pipeline, numeric_cols))
    if categorical_cols:
        transformers.append(("cat", categorical_pipeline, categorical_cols))
    preprocessor = ColumnTransformer(
        transformers, remainder="drop", verbose_feature_names_out=False)
    return preprocessor


def make_model_grid(random_state: int = 42) -> Tuple[List[Pipeline], List[Dict]]:
    """
    Returns candidate pipelines (preprocessor + estimator placeholder) and param grids for GridSearchCV.
    We'll construct final pipelines later with the preprocessor bound.
    """
    # Estimators
    lr = LogisticRegression(
        max_iter=500, solver="liblinear", random_state=random_state, class_weight="balanced")
    rf = RandomForestClassifier(n_jobs=-1, random_state=random_state, class_weight="balanced")
    hgb = HistGradientBoostingClassifier(random_state=random_state)

    # Basic parameter grids
    lr_grid = {
        "clf__C": [0.01, 0.1, 1.0, 5.0],
        "clf__penalty": ["l2"],
    }
    rf_grid = {
        "clf__n_estimators": [100, 200],
        "clf__max_depth": [None, 10, 20],
        "clf__min_samples_leaf": [1, 3],
    }
    hgb_grid = {
        "clf__learning_rate": [0.05, 0.1],
        "clf__max_iter": [100, 200],
        "clf__max_depth": [None, 10],
    }

    return [(lr, lr_grid), (rf, rf_grid), (hgb, hgb_grid)]


def evaluate_model(pipeline, X_test: pd.DataFrame, y_test: pd.Series) -> Dict:
    preds = pipeline.predict(X_test)
    metrics = {
        "accuracy": float(accuracy_score(y_test, preds)),
        "precision": float(precision_score(y_test, preds, zero_division=0)),
        "recall": float(recall_score(y_test, preds, zero_division=0)),
        "f1": float(f1_score(y_test, preds, zero_division=0)),
    }
    # If classifier supports predict_proba, compute ROC AUC
    if hasattr(pipeline, "predict_proba"):
        try:
            probs = pipeline.predict_proba(X_test)[:, 1]
            metrics["roc_auc"] = float(roc_auc_score(y_test, probs))
        except Exception:
            metrics["roc_auc"] = None
    else:
        metrics["roc_auc"] = None
    return metrics

# -------------------------
# Main training routine
# -------------------------
def train_and_save(
    input_csv: str,
    out_dir: str,
    target: str = "radiant_win",
    test_size: float = 0.2,
    random_state: int = 42,
    n_jobs: int = -1,
    cv_splits: int = 5,
):
    os.makedirs(out_dir, exist_ok=True)
    df = load_data(input_csv)

    # Convert stringified lists to py lists
    for col in ["radiant_team_sorted", "dire_team_sorted"]:
        if col in df.columns:
            df[col] = df[col].map(safe_eval_list)

    # Expand hero lists into separate columns
    df = expand_hero_lists(df)
    
    def _list_to_str(lst): 
        return ",".join(map(str, lst)) if isinstance(lst, list) else ""

    # Create groups for GroupShuffleSplit based on matchups
    if "radiant_team_sorted" in df.columns and "dire_team_sorted" in df.columns:
        r_key = df["radiant_team_sorted"].map(_list_to_str)
        d_key = df["dire_team_sorted"].map(_list_to_str)
        groups = (r_key + "|" + d_key).values
    else:
        # Fallback: use hero columns if matchup columns are not present
        sig_cols = [f"radiant_team_sorted_{i}" for i in range(5)] + [f"dire_team_sorted_{i}" for i in range(5)]
        groups = df[sig_cols].astype(str).agg(",".join, axis=1).values

    X, y = split_X_y(df, target)

    # Use GroupShuffleSplit to avoid leakage between train/test by matchup
    gss = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=random_state)
    train_idx, test_idx = next(gss.split(X, y, groups=groups))
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

    # Identify features; remove ids/timestamps if present
    numeric_cols, categorical_cols = choose_feature_types(X)

    # Important: if choose_feature_types dropped ID columns internally, re-assign X accordingly
    # (we rely on ColumnTransformer mapping by names below)
    preprocessor = build_preprocessor(numeric_cols, categorical_cols)

    results = {}
    best_overall_score = -np.inf
    best_overall = None
    best_name = None

    model_candidates = make_model_grid(random_state=random_state)

    cv = StratifiedKFold(n_splits=cv_splits, shuffle=True,
                         random_state=random_state)

    for estimator, grid in model_candidates:
        name = estimator.__class__.__name__
        print(f"\nTraining candidate estimator: {name}")

        pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("clf", estimator),
        ])

        # Grid search
        gs = GridSearchCV(
            estimator=pipeline,
            param_grid=grid,
            cv=cv,
            scoring="f1",
            n_jobs=n_jobs,
            verbose=1,
            refit=True,
        )

        gs.fit(X_train, y_train)

        print(f"Best params for {name}: {gs.best_params_}")
        print(f"Best CV score (f1) for {name}: {gs.best_score_:.4f}")

        # Evaluate on test
        metrics = evaluate_model(gs.best_estimator_, X_test, y_test)
        metrics.update({
            "cv_best_score_f1": float(gs.best_score_),
            "best_params": gs.best_params_,
        })

        results[name] = metrics

        # Track best by CV F1 (you can change this criterion)
        if gs.best_score_ > best_overall_score:
            best_overall_score = gs.best_score_
            best_overall = gs.best_estimator_
            best_name = name

    # Save best pipeline
    if best_overall is None:
        raise RuntimeError("No model was trained successfully.")
    model_path = Path(out_dir) / "best_pipeline.joblib"
    joblib.dump(best_overall, model_path)
    print(f"Saved best pipeline ({best_name}) to {model_path}")

    # Save all results/metrics
    metrics_path = Path(out_dir) / "metrics.json"
    summary = {
        "best_model_name": best_name,
        "best_cv_f1": float(best_overall_score),
        "results": results,
        "n_train": int(len(y_train)),
        "n_test": int(len(y_test)),
        "target": target,
    }
    with open(metrics_path, "w", encoding="utf8") as f:
        json.dump(summary, f, indent=2)
    print(f"Saved metrics summary to {metrics_path}")

    return model_path, metrics_path

# -------------------------
# CLI
# -------------------------


def parse_args():
    p = argparse.ArgumentParser(description="Train a model for Projeto_C318")
    p.add_argument("--input", "-i", type=str, default="./data/processed/matches_clean.csv",
                   help="Path to processed CSV with features and target (default: ./data/processed/matches_clean.csv)")
    p.add_argument("--out", "-o", type=str, default="./models",
                   help="Output directory to save model and metrics (default: ./models/)")
    p.add_argument("--target", "-t", type=str, default="radiant_win",
                   help="Target column name (default: radiant_win)")
    p.add_argument("--test-size", type=float, default=0.2,
                   help="Test split fraction (default: 0.2)")
    p.add_argument("--random-state", type=int, default=42,
                   help="Random seed (default: 42)")
    p.add_argument("--cv-splits", type=int, default=5,
                   help="Number of CV splits for GridSearch (default: 5)")
    return p.parse_args()


def main():
    args = parse_args()
    print("Starting training with args:", args)
    train_and_save(
        input_csv=args.input,
        out_dir=args.out,
        target=args.target,
        test_size=args.test_size,
        random_state=args.random_state,
        cv_splits=args.cv_splits
    )


if __name__ == "__main__":
    main()
