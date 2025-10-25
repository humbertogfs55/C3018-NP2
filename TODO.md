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

- [ ] edit preprocess.py to clean unwanted data from raw
- [ ] add a helper function to convert hero ints to hero names for data visualization
- [ ] create a final notebook for project visualization, think of a better name

- [ ] ALTERAR  a forma como a tupla de listas entra pro X no train model de string para lista de int. 

____
teste de colinearidade 

salvar a seed de treinamento (MLFLOW )

alterar o treshhold 

contar quantos true/false no csv limpo. (pra verificar desbalance)

verificar variacoes de stratify = y (linha 160 train model)

Futicar nos valores dos herois pensar em pesos/ outras possibilidades