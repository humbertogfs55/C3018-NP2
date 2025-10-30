"""
src package
-----------
Central initializer for the OpenDota ML project.
Exposes key functions and constants for easier imports.

Examples: 
    from src import fetch_public_matches
    
    # Fetch and process matches
    df = fetch_public_matches(n_batches=10)
"""

from __future__ import annotations
import logging

# --- Logging setup ---
_logger = logging.getLogger("c318")
if not _logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")
    handler.setFormatter(formatter)
    _logger.addHandler(handler)
_logger.setLevel(logging.INFO)
_logger.propagate = False

# --- config ---
from .config import (
    API_KEY,
    BASE_URL,
    PROJECT_ROOT,
    DATA_DIR,
    RAW_DIR,
    PROCESSED_DIR,
    DEFAULT_HEADERS,
    DEFAULT_MATCH_BATCH,
)

# --- fetch_data ---
from .fetch_data import fetch_public_matches, save_matches

# --- preprocess ---
from .preprocess import (
    load_raw_matches,
    validate_matches,
    enrich_matches,
    save_clean_matches,
    process_pipeline,
)

# --- train_model ---
from .train_model import train_and_save

__all__ = [
    # Config
    "API_KEY",
    "BASE_URL",
    "PROJECT_ROOT",
    "DATA_DIR",
    "RAW_DIR",
    "PROCESSED_DIR",
    "DEFAULT_HEADERS",
    "DEFAULT_MATCH_BATCH",
    # Fetch
    "fetch_public_matches",
    "save_matches",
    # Preprocess
    "load_raw_matches",
    "validate_matches",
    "enrich_matches",
    "save_clean_matches",
    "process_pipeline",
    # Train
    "train_and_save",
]