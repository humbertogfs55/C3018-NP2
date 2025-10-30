import ast
import pandas as pd
from pathlib import Path
from src.utils.heroes import HERO_ID_TO_NAME

RAW_PATH = Path("data/raw/matches.csv")
OUT_PATH = Path("data/processed/matches_clean.csv")

# Converter em lista
def parse_hero_list(cell):
    try:
        if isinstance(cell, list):
            return [int(x) for x in cell]
        if isinstance(cell, str):
            return [int(x) for x in ast.literal_eval(cell)]
    except Exception:
        return None


def clean_matches():
    df = pd.read_csv(RAW_PATH)
    print(f"Dados brutos: {len(df)} linhas")

    # Converter radiant_win pra booleano (padronizar os True/False)
    df["radiant_win"] = df["radiant_win"].map(
        lambda x: True if str(x).lower() in ["true", "1", "t"] 
        else (False if str(x).lower() in ["false", "0", "f"] else None)
    )

    # Converter colunas de heróis em listas
    df["radiant_team"] = df["radiant_team"].apply(parse_hero_list)
    df["dire_team"] = df["dire_team"].apply(parse_hero_list)

    # Filtrar linhas válidas
    valid_mask = (
        # Sem None
        df["radiant_win"].notna() &
        
        # Lista de times com 5 heróis cada
        df["radiant_team"].apply(lambda x: isinstance(x, list) and len(x) == 5) &
        df["dire_team"].apply(lambda x: isinstance(x, list) and len(x) == 5)
    )
    df_clean = df[valid_mask].copy()

    # Criar colunas com IDs dos heróis ordenados
    df_clean["radiant_team_sorted"] = df_clean["radiant_team"].apply(sorted)
    df_clean["dire_team_sorted"] = df_clean["dire_team"].apply(sorted)

    print(f"Linhas válidas: {len(df_clean)} / {len(df)}")

    # Salvar dados limpos em data/processed/matches_clean.csv
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(OUT_PATH, index=False)
    print(f"Dados limpos salvos em: {OUT_PATH}")

if __name__ == "__main__":
    clean_matches()
