#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
図鑑ベース構造への再構築ツール
ポケモン個別の図鑑番号から、図鑑ごとの番号管理に変更
"""

import json
import os
from collections import defaultdict

def load_all_pokemon_data():
    """全世代のポケモンデータを読み込み"""
    all_pokemon = {}
    
    for gen in range(1, 10):
        filename = f"gen{gen}_pokemon.json"
        if os.path.exists(filename):
            print(f"読み込み中: {filename}")
            with open(filename, 'r', encoding='utf-8') as f:
                gen_data = json.load(f)
                all_pokemon.update(gen_data)
    
    print(f"総ポケモン数: {len(all_pokemon)}")
    return all_pokemon

def create_dex_based_structure(pokemon_data):
    """図鑑ベースの構造を作成"""
    # 図鑑名のマッピング
    dex_mapping = {
        "rby": {"id": 1, "name": "全国図鑑（赤・緑・青・ピカチュウ）"},
        "gsc": {"id": 2, "name": "全国図鑑（金・銀・クリスタル）"},
        "rse": {"id": 3, "name": "ホウエン図鑑（ルビー・サファイア・エメラルド）"},
        "frlg": {"id": 4, "name": "全国図鑑（ファイアレッド・リーフグリーン）"},
        "dpp": {"id": 5, "name": "シンオウ図鑑（ダイヤモンド・パール・プラチナ）"},
        "hgss": {"id": 6, "name": "ジョウト図鑑（ハートゴールド・ソウルシルバー）"},
        "bw": {"id": 7, "name": "イッシュ図鑑（ブラック・ホワイト）"},
        "b2w2": {"id": 8, "name": "イッシュ図鑑（ブラック2・ホワイト2）"},
        "xy": {"id": 9, "name": "セントラルカロス図鑑（X・Y）"},
        "oras": {"id": 10, "name": "ホウエン図鑑（オメガルビー・アルファサファイア）"},
        "sm": {"id": 11, "name": "アローラ図鑑（サン・ムーン）"},
        "usum": {"id": 12, "name": "アローラ図鑑（ウルトラサン・ウルトラムーン）"},
        "lgpe": {"id": 13, "name": "カントー図鑑（Let's Go! ピカチュウ・イーブイ）"},
        "swsh": {"id": 14, "name": "ガラル図鑑（ソード・シールド）"},
        "bdsp": {"id": 15, "name": "シンオウ図鑑（ブリリアントダイヤモンド・シャイニングパール）"},
        "la": {"id": 16, "name": "ヒスイ図鑑（レジェンドアルセウス）"},
        "sv": {"id": 17, "name": "パルデア図鑑（スカーレット・バイオレット）"},
        "za": {"id": 34, "name": "ミアレシティ図鑑（レジェンド Z-A）"}
    }
    
    # 図鑑ベースの構造を初期化
    dex_structure = {}
    
    # 各図鑑に対して処理
    for dex_key, dex_info in dex_mapping.items():
        dex_id = dex_info["id"]
        dex_name = dex_info["name"]
        
        dex_structure[dex_id] = {
            "id": dex_id,
            "name": dex_name,
            "key": dex_key,
            "pokemon": {}
        }
        
        # この図鑑に登録されているポケモンを抽出
        pokemon_in_dex = []
        for pokemon_id, pokemon_info in pokemon_data.items():
            if "game_dex_numbers" in pokemon_info:
                if dex_key in pokemon_info["game_dex_numbers"]:
                    dex_number = pokemon_info["game_dex_numbers"][dex_key]
                    if dex_number is not None:
                        pokemon_in_dex.append({
                            "pokemon_id": int(pokemon_id),
                            "dex_number": dex_number,
                            "name": pokemon_info["name"],
                            "name_en": pokemon_info["name_en"]
                        })
        
        # 図鑑番号順にソート
        pokemon_in_dex.sort(key=lambda x: x["dex_number"])
        
        # 図鑑構造に追加
        for pokemon in pokemon_in_dex:
            dex_structure[dex_id]["pokemon"][pokemon["dex_number"]] = {
                "pokemon_id": pokemon["pokemon_id"],
                "name": pokemon["name"],
                "name_en": pokemon["name_en"]
            }
        
        print(f"{dex_name}: {len(pokemon_in_dex)}匹")
    
    return dex_structure

def save_dex_structure(dex_structure):
    """図鑑構造をJSONファイルに保存"""
    with open("pokedex_structure.json", 'w', encoding='utf-8') as f:
        json.dump(dex_structure, f, ensure_ascii=False, indent=2)
    
    print(f"図鑑構造を pokedex_structure.json に保存しました")

def create_simplified_pokemon_data(pokemon_data):
    """簡略化されたポケモンデータを作成（図鑑番号を除去）"""
    simplified_data = {}
    
    for pokemon_id, pokemon_info in pokemon_data.items():
        # game_dex_numbersを除去したコピーを作成
        simplified_pokemon = {k: v for k, v in pokemon_info.items() if k != "game_dex_numbers"}
        simplified_data[pokemon_id] = simplified_pokemon
    
    return simplified_data

def backup_current_data():
    """現在のデータをバックアップ"""
    backup_suffix = "_before_restructure"
    
    for gen in range(1, 10):
        filename = f"gen{gen}_pokemon.json"
        if os.path.exists(filename):
            backup_filename = f"gen{gen}_pokemon.json{backup_suffix}"
            os.rename(filename, backup_filename)
            print(f"バックアップ: {filename} -> {backup_filename}")

def main():
    print("=== 図鑑ベース構造への再構築 ===\n")
    
    # 現在のデータをバックアップ
    print("現在のデータをバックアップ中...")
    backup_current_data()
    print()
    
    # バックアップファイルからデータを読み込み
    print("バックアップファイルからデータを読み込み中...")
    all_pokemon = {}
    
    for gen in range(1, 10):
        backup_filename = f"gen{gen}_pokemon.json_before_restructure"
        if os.path.exists(backup_filename):
            print(f"読み込み中: {backup_filename}")
            with open(backup_filename, 'r', encoding='utf-8') as f:
                gen_data = json.load(f)
                all_pokemon.update(gen_data)
    
    print(f"総ポケモン数: {len(all_pokemon)}\n")
    
    # 図鑑ベースの構造を作成
    print("図鑑ベースの構造を作成中...")
    dex_structure = create_dex_based_structure(all_pokemon)
    print()
    
    # 図鑑構造を保存
    save_dex_structure(dex_structure)
    print()
    
    # 簡略化されたポケモンデータを作成
    print("簡略化されたポケモンデータを作成中...")
    simplified_pokemon = create_simplified_pokemon_data(all_pokemon)
    
    # 世代別に分けて保存
    gen_ranges = {
        1: (1, 151),
        2: (152, 251), 
        3: (252, 386),
        4: (387, 493),
        5: (494, 649),
        6: (650, 721),
        7: (722, 809),
        8: (810, 905),
        9: (906, 1025)
    }
    
    for gen, (start, end) in gen_ranges.items():
        gen_pokemon = {}
        for pokemon_id, pokemon_data in simplified_pokemon.items():
            pid = int(pokemon_id)
            if start <= pid <= end:
                gen_pokemon[pokemon_id] = pokemon_data
        
        if gen_pokemon:
            filename = f"gen{gen}_pokemon.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(gen_pokemon, f, ensure_ascii=False, indent=2)
            print(f"保存: {filename} ({len(gen_pokemon)}匹)")
    
    print("\n=== 再構築完了 ===")
    print("新しい構造:")
    print("- pokedex_structure.json: 図鑑ベースの構造")
    print("- gen*_pokemon.json: 簡略化されたポケモンデータ（図鑑番号なし）")
    print("- gen*_pokemon.json_before_restructure: バックアップファイル")

if __name__ == "__main__":
    main()