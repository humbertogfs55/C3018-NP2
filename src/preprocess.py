"""
Preprocessing utilities for Projeto C318.

Functions:
- load_raw_matches: Read raw CSV (no header) and parse columns to typed DataFrame.
- validate_matches: Validate required fields and 5v5 team sizes; drop or flag invalid.
- enrich_matches: Add derived features (timestamps, minutes, win flag, sorted teams, sizes).
- save_clean_matches: Serialize list columns to JSON strings and write processed CSV.
- process_pipeline: Run load → validate → enrich → save and return the DataFrame.
"""

from __future__ import annotations

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
    formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")
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
    """Read the raw matches CSV (no header) and return a typed DataFrame.

    Columns parsed:
    - match_id, match_seq_num: Int64
    - radiant_win: bool-like to {True, False, <NA>}
    - start_time, duration, lobby_type, game_mode, cluster: Int64
    - avg_rank_tier: numeric (float/Int64 with NaN)
    - num_rank_tier: Int64
    - radiant_team, dire_team: list[int]
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Raw matches file not found: {path}")

    # read without type coercion to preserve hero list strings
    df = pd.read_csv(path, header=None, dtype=str, keep_default_na=False)
    # Expect 12 columns according to the spec
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
        raise ValueError(f"Expected at least {len(expected_cols)} columns, found {df.shape[1]}")

    df = df.iloc[:, : len(expected_cols)]
    df.columns = expected_cols

    # Convert straightforward columns
    # Use errors='coerce' to turn malformed values into NaN for later handling
    df["match_id"] = pd.to_numeric(df["match_id"], errors="coerce").astype("Int64")
    df["match_seq_num"] = pd.to_numeric(df["match_seq_num"], errors="coerce").astype("Int64")

    # radiant_win may be 'True'/'False' or '1'/'0'
    df["radiant_win"] = df["radiant_win"].map(
        lambda x: True if str(x).strip().lower() in {"true", "1", "t", "yes", "y"} else
        (False if str(x).strip().lower() in {"false", "0", "f", "no", "n"} else pd.NA)
    )

    df["start_time"] = pd.to_numeric(df["start_time"], errors="coerce").astype("Int64")
    df["duration"] = pd.to_numeric(df["duration"], errors="coerce").astype("Int64")
    df["lobby_type"] = pd.to_numeric(df["lobby_type"], errors="coerce").astype("Int64")
    df["game_mode"] = pd.to_numeric(df["game_mode"], errors="coerce").astype("Int64")
    df["avg_rank_tier"] = pd.to_numeric(df["avg_rank_tier"], errors="coerce")
    df["num_rank_tier"] = pd.to_numeric(df["num_rank_tier"], errors="coerce").astype("Int64")
    df["cluster"] = pd.to_numeric(df["cluster"], errors="coerce").astype("Int64")

    # Parse hero lists
    df["radiant_team"] = df["radiant_team"].map(_parse_hero_list)
    df["dire_team"] = df["dire_team"].map(_parse_hero_list)

    logger.info("Loaded %d rows from %s", len(df), path)
    return df


def validate_matches(df: pd.DataFrame, drop_invalid: bool = True) -> pd.DataFrame:
    """Validate required fields and team sizes.

    Checks:
    - Non-null: match_id, start_time, duration
    - Team lists present and length == 5 for both sides

    If drop_invalid is True, return only valid rows. Otherwise, add 'is_valid'.
    """
    checks = pd.Series(True, index=df.index)

    # required numeric fields
    for col in ["match_id", "start_time", "duration"]:
        checks &= df[col].notna()

    # team presence and expected size (5 heroes)
    def team_ok(lst):
        if lst is None:
            return False
        try:
            return len(lst) == 5
        except Exception:
            return False

    team_ok_series = df["radiant_team"].map(team_ok) & df["dire_team"].map(team_ok)
    checks &= team_ok_series

    if drop_invalid:
        bad_count = (~checks).sum()
        if bad_count > 0:
            logger.info("Dropping %d invalid rows during validation", int(bad_count))
        df_clean = df.loc[checks].reset_index(drop=True)
        return df_clean
    else:
        df = df.copy()
        df["is_valid"] = checks
        return df


def enrich_matches(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived features to the matches DataFrame.

    Adds: start_datetime (UTC), duration_minutes, radiant_win_int,
    radiant_team_sorted, dire_team_sorted, radiant_team_size, dire_team_size.
    """
    df = df.copy()

    # convert epoch seconds -> pandas datetime (UTC)
    df["start_datetime"] = pd.to_datetime(df["start_time"].astype("Int64"), unit="s", utc=True)

    # duration minutes
    df["duration_minutes"] = df["duration"].astype("float") / 60.0

    # radiant_win int
    df["radiant_win_int"] = df["radiant_win"].map(lambda x: 1 if x is True else (0 if x is False else pd.NA)).astype("Int64")

    # sorted hero lists for deterministic ordering
    df["radiant_team_sorted"] = df["radiant_team"].map(lambda lst: sorted(lst) if isinstance(lst, list) else lst)
    df["dire_team_sorted"] = df["dire_team"].map(lambda lst: sorted(lst) if isinstance(lst, list) else lst)

    # simple team sizes (should be 5 for both after validation)
    df["radiant_team_size"] = df["radiant_team"].map(lambda lst: len(lst) if isinstance(lst, list) else 0).astype("Int64")
    df["dire_team_size"] = df["dire_team"].map(lambda lst: len(lst) if isinstance(lst, list) else 0).astype("Int64")

    logger.info("Enriched dataframe with derived features")
    return df


def save_clean_matches(df: pd.DataFrame, path: Path | str = PROCESSED_PATH) -> Path:
    """Write the processed DataFrame to CSV, serializing list columns as JSON strings."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # use index=False for a clean CSV; convert lists to JSON-like strings for portability
    df_to_save = df.copy()
    def _to_serialized_string(value):
        if isinstance(value, (list, tuple)):
            return json.dumps(list(value))
        # Handle pandas/Numpy NA values gracefully
        try:
            return "" if pd.isna(value) else str(value)
        except Exception:
            return str(value)

    for col in ["radiant_team", "dire_team", "radiant_team_sorted", "dire_team_sorted"]:
        if col in df_to_save.columns:
            df_to_save[col] = df_to_save[col].map(_to_serialized_string)

    df_to_save.to_csv(path, index=False)
    logger.info("Saved processed matches to %s (rows: %d)", path, len(df_to_save))
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
        logger.info("Pipeline finished successfully. Processed rows: %d", len(processed_df))
    except Exception as e:
        logger.exception("Preprocessing pipeline failed: %s", e)
        raise
