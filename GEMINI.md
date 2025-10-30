# GEMINI.md

## Project Overview

This project is a machine learning pipeline for predicting the winner of Dota 2 matches. It is written in Python and uses common data science libraries such as pandas, scikit-learn, and matplotlib. The project is structured as a series of scripts that can be run independently to fetch data, preprocess it, and train a model.

The project is part of the C318 - Machine Learning Fundamentals course at the National Institute of Telecommunications (INATEL).

## Building and Running

### 1. Setup

1.  **Create a virtual environment:**

    ```bash
    python -m venv .venv
    ```

2.  **Activate the virtual environment:**

    *   **Linux/macOS:**
        ```bash
        source .venv/bin/activate
        ```
    *   **Windows (cmd):**
        ```
        .venv\Scripts\activate
        ```
    *   **Windows (PowerShell):**
        ```
        .venv\scripts\Activate.ps1
        ```

3.  **Install dependencies:**

    ```bash
    pip install pip-tools
    pip-compile requirements.in
    pip install -r requirements.txt
    ```

### 2. Data Pipeline

1.  **Fetch Data:**

    This script fetches public match data from the OpenDota API and saves it to `data/raw/matches.csv`.

    ```bash
    python src/fetch_data.py
    ```

2.  **Preprocess Data:**

    This script loads the raw data, cleans it, and saves the processed data to `data/processed/matches_clean.csv`.

    ```bash
    python src/preprocess.py
    ```

3.  **Train Model:**

    This script trains a machine learning model on the preprocessed data, evaluates it, and saves the best model to `models/best_pipeline.joblib` and metrics to `models/metrics.json`.

    ```bash
    python src/train_model.py
    ```

## Development Conventions

*   The project follows a modular structure, with separate scripts for different stages of the machine learning pipeline.
*   The `src` directory contains the core source code for the project.
*   The `data` directory is used to store raw and processed data.
*   The `models` directory is used to store trained models and evaluation metrics.
*   The project uses `pip-tools` to manage dependencies.
*   The code is documented with docstrings.
