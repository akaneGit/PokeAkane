import json
import os
import re
import unicodedata
from typing import Dict, Tuple, Optional, List

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
GEN_FILES = [
    'gen1_pokemon.json',
    'gen2_pokemon.json',
    'gen3_pokemon.json',
    'gen4_pokemon.json',
    'gen5_pokemon.json',
    'gen6_pokemon.json',
    'gen7_pokemon.json',
    'gen8_pokemon.json',
    'gen9_pokemon.json',
]

def load_gen_data() -> List[Dict]:
    datasets = []
    for fname in GEN_FILES:
        path = os.path.join(DATA_DIR, fname)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                try:
                    datasets.append(json.load(f))
                except json.JSONDecodeError:
                    pass
    return datasets

# Build name mappings: Japanese -> (id, english)
# Assume each dataset is a dict keyed by national dex number or similar, with fields name/name_en/pokemon_id

def build_name_index(datasets: List[Dict]) -> Dict[str, Tuple[Optional[int], Optional[str]]]:
    index: Dict[str, Tuple[Optional[int], Optional[str]]] = {}
    for data in datasets:
        for key, entry in data.items():
            name = entry.get('name') or entry.get('name_ja')
            name_en = entry.get('name_en')
            pid = entry.get('pokemon_id') or entry.get('id')
            if not name:
                continue
            # Normalize common forms parentheses to match gallery style
            normalized_name = normalize_form_name(name)
            # Prefer first seen
            if normalized_name not in index:
                index[normalized_name] = (pid, name_en)
    return index

FORM_REPLACEMENTS = [
    (r"（オスのすがた）", "(Male)"),
    (r"（メスのすがた）", "(Female)"),
]

REGIONAL_PREFIXES = ["アローラ", "ガラル", "ヒスイ", "パルデア"]


def normalize_form_name(name: str) -> str:
    # Standardize full-width parentheses to half-width for matching variety
    # Normalize unicode to NFKC to convert full-width ascii (e.g., Ｚ) to half-width
    n = unicodedata.normalize('NFKC', name)
    for pat, rep in FORM_REPLACEMENTS:
        n = re.sub(pat, rep, n)
    return n


def enrich_23(za_path: str, index: Dict[str, Tuple[Optional[int], Optional[str]]]) -> Dict:
    with open(za_path, 'r', encoding='utf-8') as f:
        za = json.load(f)
    pokemon = za.get('pokemon', {})

    for key, entry in pokemon.items():
        name = entry.get('name')
        if not name:
            continue
        # Skip regional forms by prefix
        if any(name.startswith(pref) for pref in REGIONAL_PREFIXES):
            continue
        normalized = normalize_form_name(name)
        pid, en = index.get(normalized, (None, None))
        if pid is not None:
            entry['pokemon_id'] = pid
        if en is not None:
            entry['name_en'] = en
    return za


def main():
    za_path = os.path.join(DATA_DIR, 'pokedex_structures', '23.json')
    datasets = load_gen_data()
    index = build_name_index(datasets)
    enriched = enrich_23(za_path, index)
    with open(za_path, 'w', encoding='utf-8') as f:
        json.dump(enriched, f, ensure_ascii=False, indent=2)
    print(f"Enriched {za_path}")

if __name__ == '__main__':
    main()
