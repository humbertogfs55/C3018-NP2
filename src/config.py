"""
config.py
Stores configuration settings for the OpenDota ML project.
Handles API key loading, constants, and directory paths.
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file (if it exists)
load_dotenv()

# === API SETTINGS ===
API_KEY = os.getenv("OPENDOTA_API_KEY")
BASE_URL = "https://api.opendota.com/api"

# === PATH SETTINGS ===
# Project root (2 levels up from this file)
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

# Create directories if they don’t exist
for directory in [DATA_DIR, RAW_DIR, PROCESSED_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# === REQUEST SETTINGS ===
DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}" if API_KEY else None
}

# === GENERAL SETTINGS ===
# Limit how many public matches to fetch per run
DEFAULT_MATCH_BATCH = 100

if not API_KEY:
    print("⚠️  Warning: OPENDOTA_API_KEY not found. Set it in your .env file.")
