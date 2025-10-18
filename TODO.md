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
- [ ] Create `.env` file for sensitive keys (e.g., OpenDota API)
- [ ] Add `config.py` for configuration settings

---

## 2. Project Planning & Documentation

- [ ] Define project objectives (business & data science perspective)
- [ ] Formulate research questions
- [ ] Determine ML problem type (classification, regression, clustering, EDA)
- [ ] Document initial research and project plan
- [ ] Schedule mentorship/checkpoints with professor

---

## 3. Data Collection

- [ ] Explore OpenDota API for public match data
- [ ] Decide relevant features for analysis (heroes, items, win rates, etc.)
- [ ] Implement data extraction scripts
- [ ] Store data locally or in a database for analysis
- [ ] Clean and preprocess data

---

## 4. Data Analysis & Feature Engineering

- [ ] Conduct exploratory data analysis (EDA)
- [ ] Identify key variables and relationships
- [ ] Handle missing or inconsistent data
- [ ] Engineer features for ML models
- [ ] Normalize or scale features if needed
- [ ] Visualize trends and insights

---

## 5. Model Development

- [ ] Split data into training and test sets
- [ ] Select appropriate ML algorithms
  - Classification: Logistic Regression, Random Forest, XGBoost
  - Regression: Linear Regression, Random Forest Regressor
  - Clustering: KMeans, PCA (if applicable)
- [ ] Train and validate models
- [ ] Tune hyperparameters
- [ ] Evaluate model performance with metrics (accuracy, precision, recall, RMSE, etc.)

---

## 6. Results & Communication

- [ ] Summarize findings in report / notebook
- [ ] Visualize predictions and model performance
- [ ] Interpret results for business context
- [ ] Prepare final presentation slides

---

## 7. Project Deliverables

- [ ] Scripts for data collection, analysis, and modeling
- [ ] Documentation of the project process and results
- [ ] Presentation summarizing project objectives, methodology, and findings

---

## 8. Optional / Future Work

- [ ] Automate data collection pipeline
- [ ] Explore additional ML models or ensemble methods
- [ ] Build a simple dashboard to visualize live match predictions
