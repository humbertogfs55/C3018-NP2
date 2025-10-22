# 🧠 Projeto C318 – Fundamentos de Machine Learning

## 🎯 Descrição do Projeto

Este projeto faz parte da disciplina **C318 - Fundamentos de Machine Learning (Tópicos Especiais II)** do Instituto Nacional de Telecomunicações (INATEL).  
O objetivo é **desenvolver modelos de aprendizado de máquina** aplicados a um problema de negócio escolhido livremente pelos alunos, permitindo a prática dos conceitos aprendidos em aula.

---

## 📦 Entregáveis

1. **Scripts Computacionais**
   - Código-fonte em **Python**, implementando todas as etapas do pipeline de Machine Learning.

2. **Documentação do Projeto**
   - Registro das atividades, decisões e resultados obtidos.  
   - O formato é livre (Markdown, Jupyter Notebook, Docs, etc).

3. **Apresentação Final**
   - Síntese do projeto e dos resultados obtidos, voltada para o público técnico e de negócio.

---

## 🧭 Etapas do Projeto

### 1. Contexto do Projeto

- Definir o **tema** e os **objetivos** do projeto (de negócio e técnicos).  
- Contextualizar o problema e justificar sua relevância.  
- Registrar as metas iniciais na documentação (podem evoluir durante o projeto).

---

### 2. Pesquisa e Enquadramento do Problema

- Formular as **perguntas de negócio** alinhadas aos objetivos.  
- Definir o tipo de **aprendizado de máquina**:
  - Supervisionado – Regressão  
  - Supervisionado – Classificação  
  - Não Supervisionado – Clusterização ou Redução de Dimensionalidade  
  - Análise Exploratória de Dados  
- Escolher métricas adequadas ao tipo de problema.

---

### 3. Coleta de Dados

- Identificar e acessar as **fontes de dados** necessárias.  
- Avaliar **disponibilidade**, **qualidade** e **quantidade** de dados.  
- Aplicar boas práticas de **engenharia de dados**.

---

### 4. Desenvolvimento do Projeto Computacional

*(Item Entregável)*  
Implementar o pipeline completo de Machine Learning:

1. **Análise e Pré-processamento**
   - Exploração de dados (EDA)  
   - Limpeza, normalização e seleção de variáveis relevantes  

2. **Modelagem**
   - Treinamento de modelos supervisionados ou não supervisionados  
   - Ajuste de hiperparâmetros e comparação de desempenho  

3. **Avaliação**
   - Uso de métricas adequadas (acurácia, precisão, recall, RMSE, etc)  
   - Interpretação de resultados e validação do modelo  

---

### 5. Assessoria e Acompanhamento

- Participar das **sessões de mentoria** com o professor.  
- Tirar dúvidas, revisar resultados e atualizar a documentação.  
- Resolver problemas técnicos e garantir o progresso do projeto.

---

### 6. Geração de Análises e Resultados

- Produzir visualizações e relatórios claros sobre os resultados.  
- Analisar o impacto das descobertas do modelo.  
- Preparar a **comunicação dos resultados** para públicos técnicos e de negócio.

---

### 7. Apresentação do Projeto *(Item Entregável)*  

- Criar uma apresentação concisa e visualmente clara.  
- Apresentar o **contexto**, **metodologia**, **resultados** e **conclusões**.  
- Adaptar o conteúdo conforme o público-alvo (professor, colegas, avaliadores).

---

## 🧩 Recomendações Gerais

- O projeto pode ser feito **individualmente ou em grupo** (máx. 4 pessoas).  
- Mantenha um repositório organizado:

---

## Development Setup

### 1. Create a virtual environment

```bash

python -m venv .venv

```

### 2. Activate venv

```bash linux
source .venv/bin/activate
```

```cmd windows
.venv\Scripts\activate
```

```powershell windows
.venv\scripts\Activate.ps1
```

### 3. Install dependencies

1. install pip tools

    ```bash
    pip install pip-tools
    ```

2. compile and install dependencies

    ```bash
    pip-compile requirements.in
    pip install -r requirements.txt
    ```
