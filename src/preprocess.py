"""
Preprocessing utilities for Projeto C318.

Functions:
- load_raw_matches: Read raw CSV (no header) and parse only essential columns to typed DataFrame.
- validate_matches: Validate required fields and 5v5 team sizes; drop or flag invalid.
- enrich_matches: Add essential derived features (sorted teams).
- save_clean_matches: Serialize list columns to JSON strings and write processed CSV.
- process_pipeline: Run load → validate → enrich → save and return the DataFrame.

Essential columns kept: radiant_win, radiant_team, dire_team
"""

from __future__ import annotations
from src.utils.heroes import hero_list_to_names


import ast
import logging
from pathlib import Path
from typing import List, Optional

import pandas as pd
import json


# Configure module logger (caller can reconfigure)
logger = logging.getLogger("c318.preprocess")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s [%(name)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)


# Default paths (customize via function args)
RAW_PATH = Path("data/raw/matches.csv")
PROCESSED_PATH = Path("data/processed/matches_clean.csv")


# --- Helpers -----------------------------------------------------------------
def _parse_hero_list(cell: str) -> Optional[List[int]]:
    """Parse a hero list cell into list[int], or None if it cannot be parsed."""
    if pd.isna(cell):
        return None
    if isinstance(cell, (list, tuple)):
        # already parsed
        return list(cell)
    try:
        parsed = ast.literal_eval(cell)
        if isinstance(parsed, (list, tuple)):
            return [int(x) for x in parsed]
        # if it's a single int, return as single-element list
        if isinstance(parsed, int):
            return [parsed]
    except Exception:
        # fallback: try to parse comma-separated values
        try:
            text = str(cell).strip()
            # remove enclosing brackets if present
            text = text.strip("[]() ")
            if text == "":
                return []
            parts = [p.strip() for p in text.split(",")]
            return [int(p) for p in parts if p != ""]
        except Exception:
            logger.debug("Failed to parse hero list cell: %r", cell)
            return None
    return None


# --- Core functions ---------------------------------------------------------
def load_raw_matches(path: Path | str = RAW_PATH) -> pd.DataFrame:
    """Read the raw matches CSV (no header) and return a typed DataFrame with only essential columns.

    Columns parsed:
    - radiant_win: bool-like to {True, False, <NA>}
    - radiant_team, dire_team: list[int]
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Raw matches file not found: {path}")

    # read without type coercion to preserve hero list strings
    df = pd.read_csv(path, header=None, dtype=str, keep_default_na=False)
    # Expect 12 columns according to the spec, but we only need columns 2, 10, 11
    expected_cols = [
        "match_id",
        "match_seq_num",
        "radiant_win",
        "start_time",
        "duration",
        "lobby_type",
        "game_mode",
        "avg_rank_tier",
        "num_rank_tier",
        "cluster",
        "radiant_team",
        "dire_team",
    ]
    if df.shape[1] < len(expected_cols):
        raise ValueError(
            f"Expected at least {len(expected_cols)} columns, found {df.shape[1]}")

    df = df.iloc[:, : len(expected_cols)]
    df.columns = expected_cols

    # Only keep essential columns: radiant_win, radiant_team, dire_team
    essential_cols = ["radiant_win", "radiant_team", "dire_team"]
    df = df[essential_cols].copy()

    # radiant_win may be 'True'/'False' or '1'/'0'
    df["radiant_win"] = df["radiant_win"].map(
        lambda x: True if str(x).strip().lower() in {"true", "1", "t", "yes", "y"} else
        (False if str(x).strip().lower() in {
         "false", "0", "f", "no", "n"} else pd.NA)
    )

    # Parse hero lists
    df["radiant_team"] = df["radiant_team"].map(_parse_hero_list)
    df["dire_team"] = df["dire_team"].map(_parse_hero_list)

    logger.info("Loaded %d rows from %s (essential columns only)", len(df), path)
    return df


def validate_matches(df: pd.DataFrame, drop_invalid: bool = True) -> pd.DataFrame:
    """Validate required fields and team sizes.

    Checks:
    - Non-null: radiant_win
    - Team lists present and length == 5 for both sides

    If drop_invalid is True, return only valid rows. Otherwise, add 'is_valid'.
    """
    checks = pd.Series(True, index=df.index)

    # required field
    checks &= df["radiant_win"].notna()

    # team presence and expected size (5 heroes)
    def team_ok(lst):
        if lst is None:
            return False
        try:
            return len(lst) == 5
        except Exception:
            return False

    team_ok_series = df["radiant_team"].map(
        team_ok) & df["dire_team"].map(team_ok)
    checks &= team_ok_series

    if drop_invalid:
        bad_count = (~checks).sum()
        if bad_count > 0:
            logger.info(
                "Dropping %d invalid rows during validation", int(bad_count))
        df_clean = df.loc[checks].reset_index(drop=True)
        return df_clean
    else:
        df = df.copy()
        df["is_valid"] = checks
        return df


def enrich_matches(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived features to the matches DataFrame.

    Adds: radiant_team_sorted, dire_team_sorted.
    """
    df = df.copy()

    # sorted hero lists for deterministic ordering
    df["radiant_team_sorted"] = df["radiant_team"].map(
        lambda lst: sorted(lst) if isinstance(lst, list) else lst)
    df["dire_team_sorted"] = df["dire_team"].map(
        lambda lst: sorted(lst) if isinstance(lst, list) else lst)

    logger.info("Enriched dataframe with essential derived features")

    df["radiant_heroes"] = df["radiant_team_sorted"].map(hero_list_to_names)
    df["dire_heroes"] = df["dire_team_sorted"].map(hero_list_to_names)
    
    return df


def save_clean_matches(df: pd.DataFrame, path: Path | str = PROCESSED_PATH) -> Path:
    """Write the processed DataFrame to CSV, serializing list columns as JSON strings."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # use index=False for a clean CSV; convert lists to JSON-like strings for portability
    df_to_save = df.copy()

    # Serialize sorted team columns if present
    def _to_serialized_string(value):
        if isinstance(value, (list, tuple)):
            return json.dumps(list(value))
        # Handle pandas/Numpy NA values gracefully
        try:
            return "" if pd.isna(value) else str(value)
        except Exception:
            return str(value)

    for col in ["radiant_team_sorted", "dire_team_sorted"]:
        if col in df_to_save.columns:
            df_to_save[col] = df_to_save[col].map(_to_serialized_string)

    # IMPORTANT: remove the original unsorted team columns before saving
    unsorted_cols = ["radiant_team", "dire_team"]
    dropped = [c for c in unsorted_cols if c in df_to_save.columns]
    if dropped:
        df_to_save = df_to_save.drop(columns=dropped)
        logger.debug(
            "Dropped unsorted team columns from saved DataFrame: %s", dropped)

    df_to_save.to_csv(path, index=False)
    logger.info("Saved processed matches to %s (rows: %d)",
                path, len(df_to_save))
    return path


# --- Convenience CLI --------------------------------------------------------
def process_pipeline(
    raw_path: Optional[Path | str] = None,
    out_path: Optional[Path | str] = None,
    drop_invalid: bool = True,
) -> pd.DataFrame:
    """Run load → validate → enrich → save. Return the processed DataFrame."""
    raw_path = raw_path or RAW_PATH
    out_path = out_path or PROCESSED_PATH

    df = load_raw_matches(raw_path)
    df = validate_matches(df, drop_invalid=drop_invalid)
    df = enrich_matches(df)
    save_clean_matches(df, out_path)
    return df


if __name__ == "__main__":
    # quick run from project root: python src/preprocess.py
    logger.info("Running preprocessing pipeline (raw -> processed)")
    try:
        processed_df = process_pipeline()
        logger.info(
            "Pipeline finished successfully. Processed rows: %d", len(processed_df))
    except Exception as e:
        logger.exception("Preprocessing pipeline failed: %s", e)
        raise
