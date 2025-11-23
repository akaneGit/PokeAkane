#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
33個の図鑑の詳細情報を取得してボタン用データを作成
"""

import requests
import json

def get_all_pokedex_info():
    """全図鑑の詳細情報を取得"""
    base_url = "https://pokeapi.co/api/v2"
    
    # 33個の図鑑リストを取得
    response = requests.get(f"{base_url}/pokedex/?limit=33")
    pokedex_list = response.json()["results"]
    
    pokedex_info = []
    
    for pokedex in pokedex_list:
        name = pokedex["name"]
        
        # 各図鑑の詳細情報を取得
        detail_response = requests.get(pokedex["url"])
        detail = detail_response.json()
        
        # 日本語名を作成（適当に翻訳）
        japanese_names = {
            "national": "全国図鑑",
            "kanto": "カントー図鑑",
            "original-johto": "ジョウト図鑑(金銀)",
            "hoenn": "ホウエン図鑑(RSE)",
            "original-sinnoh": "シンオウ図鑑(DP)",
            "extended-sinnoh": "シンオウ図鑑(Pt)",
            "updated-johto": "ジョウト図鑑(HGSS)",
            "original-unova": "イッシュ図鑑(BW)",
            "updated-unova": "イッシュ図鑑(B2W2)",
            "conquest-gallery": "ノブナガ図鑑",
            "kalos-central": "カロス中央図鑑",
            "kalos-coastal": "カロス海岸図鑑",
            "kalos-mountain": "カロス山岳図鑑",
            "updated-hoenn": "ホウエン図鑑(ORAS)",
            "original-alola": "アローラ図鑑(SM)",
            "original-melemele": "メレメレ図鑑(SM)",
            "original-akala": "アーカラ図鑑(SM)",
            "original-ulaula": "ウラウラ図鑑(SM)",
            "original-poni": "ポニ図鑑(SM)",
            "updated-alola": "アローラ図鑑(USUM)",
            "updated-melemele": "メレメレ図鑑(USUM)",
            "updated-akala": "アーカラ図鑑(USUM)",
            "updated-ulaula": "ウラウラ図鑑(USUM)",
            "updated-poni": "ポニ図鑑(USUM)",
            "letsgo-kanto": "カントー図鑑(LGPE)",
            "galar": "ガラル図鑑",
            "isle-of-armor": "ヨロイ島図鑑",
            "crown-tundra": "カンムリ雪原図鑑",
            "hisui": "ヒスイ図鑑",
            "paldea": "パルデア図鑑",
            "kitakami": "キタカミ図鑑",
            "blueberry": "ブルーベリー図鑑",
            "lumiose-city": "ミアレシティ図鑑"
        }
        
        pokemon_count = len(detail.get("pokemon_entries", []))
        
        info = {
            "id": detail["id"],
            "name": name,
            "japanese_name": japanese_names.get(name, name),
            "pokemon_count": pokemon_count,
            "is_main_series": detail.get("is_main_series", True)
        }
        
        pokedex_info.append(info)
        print(f"✅ {name}: {pokemon_count}匹")
    
    # ファイルに保存
    with open("pokedex_button_data.json", "w", encoding="utf-8") as f:
        json.dump(pokedex_info, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 pokedex_button_data.json に保存しました")
    return pokedex_info

if __name__ == "__main__":
    print("🚀 図鑑ボタン用データ作成開始！")
    pokedex_info = get_all_pokedex_info()
    
    print("\n📊 図鑑一覧:")
    for info in pokedex_info:
        print(f"  {info['id']:2d}. {info['japanese_name']} ({info['name']}) - {info['pokemon_count']}匹")