# 📄 Research_Docs.md

**Projeto:** Predição de Vitória em Partidas de Dota 2  
**Disciplina:** C318 – Fundamentos de Machine Learning  
**Instituição:** INATEL  
**Autores:** Adson Ferreira · Humberto Gomes · Caroliny Abreu · Guilherme Cotta · Iza Lopes  
**Data:** Novembro/2025  

---

# 🧭 1. Contexto e Justificativa

Dota 2 é um dos jogos mais complexos do cenário competitivo, com mais de 145 heróis e bilhões de combinações possíveis no draft. Antes mesmo da partida começar, as equipes escolhem seus cinco heróis — um processo estratégico que influencia diretamente o resultado do jogo.

Este projeto busca responder:

> **É possível prever o vencedor de uma partida usando apenas o draft (composição dos heróis)?**

Do ponto de vista acadêmico, o problema envolve:

- Alta dimensionalidade  
- Interações complexas entre features  
- Dados desequilibrados  
- Predição binária com variáveis categóricas  
- Engenharia de features baseada em IDs de heróis  

Do ponto de vista prático, modelos desse tipo podem:

- Apoiar analistas de e-sports  
- Ajudar equipes competitivas a tomar decisões  
- Identificar sinergias e contra-picks  
- Criar sistemas inteligentes de recomendação de heróis  

---

# 🎯 2. Identificação do Projeto

| Item | Descrição |
|------|-----------|
| **Tema** | Predição de vitória do Radiant usando apenas a composição dos heróis |
| **Tipo de Aprendizagem** | Supervisionada – Classificação Binária |
| **Target** | `radiant_win` |
| **Input** | Lista de 5 heróis por time (Radiant/Dire) |
| **Repositório** | github.com/humbertogfs55/C3018-NP2 |

---

# 🎯 3. Objetivos

## 3.1 Objetivo de Negócio
- Classificar qual time tem maior probabilidade de vencer dado apenas o draft.
- Identificar composições de heróis mais eficazes.
- Apoiar tomada de decisões estratégicas durante drafts competitivos.

## 3.2 Objetivo de Ciência de Dados
- Treinar um modelo capaz de prever `radiant_win` com alta performance.
- Criar pipeline completa: coleta → processamento → ML → avaliação → tracking.
- Avaliar diferentes modelos e hiperparâmetros.
- Registrar experimentos via MLflow.

---

# ❓ 4. Perguntas de Negócio

1. Qual time tem maior chance de vencer com base no draft?  
2. Existem combinações específicas que influenciam significativamente o resultado?  
3. É viável prever o resultado antes da partida começar?  
4. Quais modelos se adaptam melhor a esse tipo de dado categórico de alta cardinalidade?  

---

# 🧩 5. Enquadramento do Problema

| Item | Definição |
|------|-----------|
| Tipo | Classificação Binária (Supervisionada) |
| Target | `radiant_win` |
| Features | IDs dos heróis selecionados (5 Radiant + 5 Dire) |
| Feature Space final | ~290 colunas após One-Hot Encoding |

---

# 📦 6. Dados para Desenvolvimento

## 6.1 Fonte
API **OpenDota**, endpoint `/publicMatches`.

## 6.2 Estrutura dos Dados Brutos (`data/raw`)
- `match_id`
- `radiant_win`
- `radiant_team` (lista com 5 IDs)
- `dire_team`
- metadados diversos

## 6.3 Estrutura dos Dados Processados (`data/processed`)
Após limpeza:

- `radiant_win`
- `radiant_team_sorted`
- `dire_team_sorted`
- `radiant_heroes` (nomes)
- `dire_heroes`
- remoção de duplicados  
- ~110 partidas únicas

---

# 🔄 7. Pipeline do Projeto

fetch_data.py → preprocess.py → train_model.py → notebooks/testing.ipynb

Etapas:

1. **Coleta de dados** via API  
2. **Validação e limpeza**  
3. **Engenharia de Features**  
4. **One-Hot Encoding**  
5. **Treinamento via GridSearchCV**  
6. **Registro no MLflow**  
7. **Predições e análise posterior**  

---

# 🧹 8. Pré-processamento

### Tarefas executadas:
- Conversão de strings para listas
- Ordenamento dos times (`sorted()`)
- Deduplicação por matchup
- Normalização dos nomes dos heróis
- Remoção de colunas irrelevantes
- Detecção e remoção de correlações acima de 0.8
- Filtragem de partidas inválidas

Resultado final: **110 partidas limpas e utilizáveis**.

---

# 🧠 9. Treinamento do Modelo

## 9.1 Conversão dos Times para Features
Cada time vira:

```bash
radiant_1 ... radiant_5
dire_1 ... dire_5
```

## 9.2 Pipeline de ML
Inclui:

- Imputação
- Escalonamento
- One-Hot Encoding
- Classificador no final

## 9.3 Modelos avaliados
- Logistic Regression  
- Random Forest  
- HistGradientBoosting  

## 9.4 Validação
- `StratifiedKFold(5)`
- Métrica principal: **F1 Score**
- Busca de hiperparâmetros via GridSearchCV

## 9.5 MLflow Tracking

Ao executar:

```bash
python -m src.train_model
```

O MLflow cria automaticamente a pasta `mlruns/` e registra:

- métricas
- parâmetros
- modelos
- artefatos

Para visualizar a interface:

```bash
mlflow ui
```

Acesse:

🔗 http://localhost:5000

🔗 Exemplo de experimento real do projeto:
http://localhost:5000/#/experiments/403649128202140705/runs/dbd051c42dff4a68a41053e9fe1885a5

---

# 📊 10. Avaliação dos Modelos

| Modelo              | Accuracy | Precision | Recall   | F1        | ROC AUC | CV F1     |
| ------------------- | -------- | --------- | -------- | --------- | ------- | --------- |
| **Random Forest**   | 68.2%    | 66.7%     | **100%** | **80.0%** | 62.5%   | **77.6%** |
| Logistic Regression | 63.6%    | 66.7%     | 85.7%    | 75.0%     | 56.3%   | 65.8%     |
| Gradient Boosting   | 63.6%    | 68.8%     | 78.6%    | 73.3%     | 60.7%   | 72.3%     |

## Melhor Modelo: Random Forest

Hiperparâmetros:

```bash
n_estimators=200
max_depth=10
min_samples_leaf=1
```
---

# 📈 11. Análises Exploratórias

- Dataset moderadamente balanceado
- Sensível a correlações entre features
- Thresholds alternativos foram testados para otimização da F1
- Exibição dos top-20 matchups mais frequentes

---

# 🔮 12. Próximos Passos

- Expandir dataset para 10k+ partidas
- Adicionar sinergias e counters explícitos
- Testar modelos avançados (XGBoost, LightGBM, CatBoost)
- Criar API REST para predição
- Criar dashboard com Streamlit

---

# 📁 13. Estrutura Atual do Projeto

C3018-NP2/
│
├── data/
│   ├── raw/
│   ├── processed/
│
├── src/
│   ├── fetch_data.py
│   ├── preprocess.py
│   ├── train_model.py
│
├── models/
│   ├── best_pipeline.joblib
│   ├── metrics.json
│
├── notebooks/
│   ├── analyze_matches.ipynb
│   ├── analyze_features.ipynb
│   ├── analyze_thresholds.ipynb
│   ├── testing.ipynb
│
├── mlruns/
│
├── README.md
└── research_doc.md

# 🎓 14. Conclusão

Este projeto demonstra uma pipeline completa de Machine Learning aplicada a dados reais de e-sports, incluindo coleta de dados, pré-processamento, experimentação e avaliação rigorosa. Mesmo com um dataset reduzido, o modelo Random Forest apresentou desempenho consistente e robusto.

O projeto confirma que é possível prever o resultado de partidas usando apenas a composição de heróis, abrindo caminho para estudos com sinergias, counters e modelos mais avançados.