"""
fetch_data.py
----------------
Responsável por coletar dados de partidas públicas da OpenDota API
e armazená-los localmente, com tratamento de exceções e tolerância a falhas.
"""

import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

# load vars
load_dotenv()

API_BASE_URL = os.getenv("OPENDOTA_API_URL", "https://api.opendota.com/api")
OUTPUT_PATH = os.getenv("DATA_PATH", "./data/raw/matches.csv")

def fetch_public_matches(n_batches: int = 5, batch_size: int = 1000, max_retries: int = 3) -> pd.DataFrame:
    """
    Scrape random public matches from OpenDota.

    Args:
        n_batches (int): number of batches to request.
        batch_size (int): number of matches per request (API returns default).
        max_retries (int): request retry attempts in case of failure.

    Returns:
        DataFrame with collected matches (may be partially filled if API errors occur).
    """

    all_matches = []
    url = f"{API_BASE_URL}/publicMatches"

    for i in range(n_batches):
        success = False

        for attempt in range(1, max_retries + 1):
            try:
                response = requests.get(url, timeout=8)
                response.raise_for_status()  # dispara exceção se for erro HTTP
                data = response.json()

                all_matches.extend(data)
                print(f"Batch {i+1} coletado ({len(data)} matches)")
                success = True
                break  # sair do retry loop se deu certo

            except requests.exceptions.Timeout:
                print(f"Timeout no batch {i+1} (tentativa {attempt}/{max_retries})")

            except requests.exceptions.RequestException as e:
                print(f"Erro na API no batch {i+1}: {e} (tentativa {attempt}/{max_retries})")

            time.sleep(2)  # pausa antes de tentar de novo

        if not success:
            print(f"Falha definitiva no batch {i+1}. Pulando para o próximo...")

    df = pd.DataFrame(all_matches)
    print(f"\nTotal coletado: {len(df)} partidas")
    return df


def save_matches(df: pd.DataFrame, path: str = OUTPUT_PATH):
    """
    Salva o DataFrame em formato CSV.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Dados salvos em: {path}")


def main():
    df = fetch_public_matches(n_batches=100)
    save_matches(df)

if __name__ == "__main__":
    main()
