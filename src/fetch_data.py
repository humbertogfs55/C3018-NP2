"""fetch_data.py
----------------
Responsavel por coletar dados de partidas publicas da openDota API
e armazena-los localmente.
"""

import os
import requests
import pandas as pd
from dotenv import load_dotenv

#load vars
load_dotenv()

API_BASE_URL = os.getenv("OPENDOTA_API_URL", "https://api.opendota.com/api")
OUTPUT_PATH = os.getenv("DATA_PATH", "./data/raw/matches.csv")

def fetch_public_matches(n_batches : int = 5, batch_size: int = 1000) -> pd.DataFrame:
    """
    Screpe random public matches from OpenDota.
    
    Args:
        n_batches (int): number of batches to request in a row.
        batch_size (int): how many matches per batch should return.

    Returns:
        Dataframe of collected matches.
    """

    all_matches = []

    url = f"{API_BASE_URL}/publicMatches"

    for i in range(n_batches):
        response = requests.get(url)
        if response.status_code != 200: 
            print(f"Error at Request {i+1}: {response.status_code}")
            continue

        data = response.json()
        all_matches.extend(data)
        print(f"batch {i+1} colected ({len(data)} matches)")

    df = pd.DataFrame(all_matches)
    print(f"\n Total Colected matches: {len(df)}")
    return df

def save_matches(df: pd.DataFrame, path: str = OUTPUT_PATH):
    """
    Salva o DataFrame em formato CSV.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"💾 Dados salvos em: {path}")


def main():
    df = fetch_public_matches(n_batches=100)
    save_matches(df)

if __name__ == "__main__":
    main()