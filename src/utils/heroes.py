import json
from pathlib import Path

HEROES_JSON = Path("data/raw/heroes.json")

with open(HEROES_JSON, "r", encoding="utf-8") as f:
    heroes = json.load(f)

# Mapa {id: nome}
HERO_ID_TO_NAME = {hero["id"]: hero["localized_name"] for hero in heroes}

def hero_id_to_name(hero_id: int) -> str:
    """Converte ID único em nome do herói"""
    return HERO_ID_TO_NAME.get(hero_id, f"UNKNOWN_{hero_id}")

def hero_list_to_names(hero_list: list[int]) -> list[str]:
    """Converte lista de IDs em lista de nomes"""
    return [hero_id_to_name(h) for h in hero_list]
