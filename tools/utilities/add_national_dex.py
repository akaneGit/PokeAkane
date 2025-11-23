#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全国図鑑追加ツール
全ポケモン（1025匹）を含む全国図鑑を図鑑構造に追加
"""

import json
import os

def add_national_dex():
    """全国図鑑を図鑑構造に追加"""
    
    # 図鑑構造を読み込み
    with open("pokedex_structure.json", 'r', encoding='utf-8') as f:
        pokedex_data = json.load(f)
    
    # 全ポケモンデータを読み込み
    all_pokemon = {}
    for gen in range(1, 10):
        filename = f"gen{gen}_pokemon.json"
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                gen_data = json.load(f)
                all_pokemon.update(gen_data)
    
    print(f"総ポケモン数: {len(all_pokemon)}")
    
    # 全国図鑑を作成（ID: 0 で最初に表示されるように）
    national_dex = {
        "id": 0,
        "name": "全国図鑑（全ポケモン）",
        "key": "national",
        "pokemon": {}
    }
    
    # 全ポケモンを全国図鑑番号順に追加
    for pokemon_id in sorted(all_pokemon.keys(), key=int):
        pokemon = all_pokemon[pokemon_id]
        national_dex["pokemon"][pokemon_id] = {
            "pokemon_id": int(pokemon_id),
            "name": pokemon["name"],
            "name_en": pokemon["name_en"]
        }
    
    # 図鑑構造に追加
    pokedex_data["0"] = national_dex
    
    print(f"全国図鑑に {len(national_dex['pokemon'])} 匹のポケモンを追加しました")
    
    # 保存
    with open("pokedex_structure.json", 'w', encoding='utf-8') as f:
        json.dump(pokedex_data, f, ensure_ascii=False, indent=2)
    
    print("全国図鑑を pokedex_structure.json に追加しました")

if __name__ == "__main__":
    add_national_dex()