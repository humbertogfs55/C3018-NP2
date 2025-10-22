# 📄 Research_Docs.md 

**Projeto:** C318 – Fundamentos de Machine Learning  
**Tema:** Predição de vitória (Radiant vs Dire) em partidas públicas de Dota 2  
**Aluno(s):** [Humberto, Iza, Carol]  
**Data:** Outubro/2025  

---

## 🧭 1. Contexto e Objetivos

O projeto tem como objetivo **prever a probabilidade de vitória da equipe Radiant** em partidas públicas de Dota 2 utilizando dados coletados via **OpenDota API**.  

A ideia central é aplicar o pipeline completo de **Machine Learning supervisionado (classificação)** para identificar padrões de vitória com base em informações pré-jogo, especificamente a composicao dos times.

**Objetivos específicos:**

- Coletar e pré-processar dados de partidas públicas do Dota 2.  
- Analisar correlações entre variáveis (`radiant_team` , `dire_team`) e o resultado (`radiant_win`).  
- Treinar modelos de classificação supervisionada para estimar as chances de vitória.

---

## 📊 2. Coleta de Dados

**Fonte:** [OpenDota Public API](https://docs.opendota.com/#tag/public-matches)

**Método:**  
Foi desenvolvido o script `src/fetch_data.py` responsável por:

- Requisitar partidas públicas via endpoint `/publicMatches`
- Converter a resposta JSON em formato tabular (`matches.csv`)
- Armazenar os dados brutos em `data/raw/matches.csv`

**Decisões:**

- O intervalo de coleta foi limitado para evitar *rate limit* da API.  
- Apenas partidas completas (`duration > 0`) foram consideradas.  
- Variáveis iniciais mantidas:  
  `match_id, start_time, duration, radiant_win, radiant_team, dire_team`.

---

## 🧹 3. Pré-Processamento

**Script:** `src/preprocess.py`  
**Arquivo gerado:** `data/processed/matches_clean.csv`

**Etapas aplicadas:**

- Remoção de colunas irrelevantes (Removemos todas as variaveis que nao devem ser utilizadas no treinamento).  
- Conversão de variáveis categóricas (`radiant_team`, `dire_team`) via *Label Encoding*.
- Ordenamento dos IDs de herois nas equipes, garantindo que equipes iguais sejam tratadas como iguais.
  (Uma equipe axe/dazzle/muerta/juggernaut/earthshaker vai ser vista como diferente da equipe: dazle/axe/earthshaker/muerta/juggernaut pelo modelo de LM entao devemos aplicar o sorting)
- Tratamento de valores ausentes.  

**Decisões:**

- A coluna `radiant_win` foi mantida como variável-alvo (label binário).  
- As equipes foram representadas numericamente, permitindo o uso de algoritmos padrão do scikit-learn.
- Equipes foram organizadas usando sort  

---

## 🧠 4. Modelagem e Treinamento

**Tipo de problema:** Classificação supervisionada  
**Bibliotecas:** `scikit-learn`, `joblib`, `pandas`, `numpy`

**Abordagem inicial:**

- Comparar diferentes algoritmos:
  - Logistic Regression  
  - Random Forest  
  - Gradient Boosting  

**Pipeline:**  
Criado em `src/train_model.py`, salvando dois arquivos:

- `models/best_pipeline.joblib` – modelo treinado e validado.  
- `models/metrics.json` – métricas de desempenho.

**Resultados obtidos (parciais):**
| Modelo | Acurácia | F1-score | Observações |
|--------|-----------|-----------|--------------|
| Logistic Regression | 0.68 | 0.67 | Rápido e interpretável |
| Random Forest | **0.74** | **0.73** | Melhor desempenho geral |
| Gradient Boosting | 0.72 | 0.71 | Requer mais tuning |

**Decisões:**
- O modelo **Random Forest** foi selecionado como o melhor até o momento.  
- O dataset foi dividido em **80/20 (train/test)**.  
- As métricas foram calculadas com **cross-validation (k=5)**.

---

## 🔍 5. Análises e Observações

**Insights iniciais:**
- Partidas com **MMR médio mais alto** tendem a apresentar maior taxa de vitória do Radiant.  
- Certos modos de jogo (`game_mode = 22`, Ranked All Pick) possuem padrões mais previsíveis.  
- As features `duration` e `lobby_type` apresentaram correlação moderada com o resultado.

**Limitações:**
- As equipes são representadas apenas por IDs numéricos, sem análise dos heróis ou composições.  
- Dados históricos limitados (janela curta de partidas coletadas).  
- Possível viés em partidas com MMR extremo.

---

## 🔮 6. Próximos Passos

- [ ] Expandir o conjunto de dados (maior volume de partidas).  
- [ ] Criar feature engineering com heróis jogados (`radiant_heroes`, `dire_heroes`).  
- [ ] Aplicar otimização de hiperparâmetros (GridSearchCV).  
- [ ] Implementar interface de previsão (API ou CLI).  
- [ ] Documentar resultados finais para apresentação (NP2).

---

## 📁 Estrutura Atual do Projeto

