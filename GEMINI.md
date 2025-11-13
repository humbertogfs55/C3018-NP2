# GEMINI.md

## Project Overview

This project is a machine learning pipeline for predicting the winner of Dota 2 matches. It is written in Python and uses common data science libraries such as pandas, scikit-learn, and matplotlib. The project is structured as a series of scripts that can be run independently to fetch data, preprocess it, and train a model.

The project is part of the C318 - Machine Learning Fundamentals course at the National Institute of Telecommunications (INATEL).

## Building and Running

### 1. Setup

1. **Create a virtual environment:**

    ```bash
    python -m venv .venv
    ```

2. **Activate the virtual environment:**

    * Linux/macOS:
        ```bash
        source .venv/bin/activate
        ```
    * Windows (cmd):
        ```
        .venv\Scripts\activate
        ```
    * Windows (PowerShell):
        ```
        .venv\scripts\Activate.ps1
        ```

3. **Install dependencies:**

    ```bash
    pip install pip-tools
    pip-compile requirements.in
    pip install -r requirements.txt
    ```

### 2. Data Pipeline

1. **Fetch Data**

    Fetches public match data from the OpenDota API and saves it to:

    ```
    data/raw/matches.csv
    ```

    Run:

    ```bash
    python src/fetch_data.py
    ```

2. **Preprocess Data**

    Loads raw data, validates and cleans it, then writes:

    ```
    data/processed/matches_clean.csv
    ```

    Run:

    ```bash
    python src/preprocess.py
    ```

3. **Train Model (with MLflow tracking)**

    This script trains multiple ML models, performs hyperparameter tuning, selects the best estimator, and saves:

    ```
    models/best_pipeline.joblib
    models/metrics.json
    ```

    In addition, **MLflow** is now integrated into the training pipeline.  
    MLflow automatically logs:

    - experiment name  
    - parameters  
    - metrics  
    - model artifacts  
    - cross-validation scores  
    - best estimator  
    - generated plots  

    All experiment data is stored inside:

    ```
    mlruns/
    ```

    **Run training:**

    ```bash
    python -m src.train_model
    ```

    **Open MLflow UI:**

    ```bash
    mlflow ui
    ```

    The dashboard will be available at:

    ```
    http://127.0.0.1:5000
    ```

    Example experiment run (link masked):

    🔗 [Open MLflow experiment example](http://127.0.0.1:5000/#/)

## Development Conventions

- The project follows a modular structure, with separate scripts for different stages of the machine learning pipeline.
- The `src` directory contains the core source code for the project.
- The `data` directory stores raw and processed data.
- The `models` directory stores trained pipelines and evaluation metrics.
- The `mlruns` directory stores all MLflow experiment data.
- The `notebooks` directory is used for experiments, prototyping, and exploratory analysis.
- The project uses `pip-tools` for dependency management.
- All scripts include descriptive docstrings.
