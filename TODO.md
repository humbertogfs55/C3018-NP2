# Projeto C318 - TODO List

This file outlines the tasks for the development of the Machine Learning project for the C318 course.

---

## 1. Project Setup

- [x] Create project directory structure
- [x] Initialize Git repository
- [x] Set up Python virtual environment (`venv`)  
- [x] Install required dependencies:
  - `python-dotenv` for environment variables
  - `pandas`, `numpy`, `scikit-learn`
  - `matplotlib`, `seaborn` for data visualization
  - `requests` for API access
- [x] Create `.env` file for sensitive keys (e.g., OpenDota API)
- [x] Add `config.py` for configuration settings

---

## 2. Assorted Tasks

- [x] edit preprocess.py to clean unwanted data from raw
- [x] add a helper function to convert hero ints to hero names for data visualization
- [x] create a final notebook for project visualization, think of a better name
- [x] Change how the tuple of hero lists enters X in train_model.py — from string to list of integers
- [x] Perform collinearity test
- [x] Save training seed (MLflow integration)
- [x] Adjust decision threshold
- [x] Count number of True/False values in the cleaned CSV (to check class imbalance)
- [x] Test variations of stratify=y (line 160 in train_model.py)











