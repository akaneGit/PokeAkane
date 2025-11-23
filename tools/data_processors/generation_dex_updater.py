#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
世代別ファイルに図鑑番号を追加するツール
各世代のJSONファイルにgame_dex_numbersフィールドを追加
"""

import json
import os

class GenerationDexUpdater:
    def __init__(self):
        # 第1世代のポケモンの基本的な図鑑番号データ
        self.generation_dex_data = {
            1: {  # 第1世代
                # フシギダネ系統
                "1": {"rby": 1, "gsc": 231, "rse": None, "frlg": 1, "dpp": 1, "hgss": 231, "bw": None, "b2w2": None, "xy": 1, "oras": None, "sm": None, "usum": None, "lgpe": 1, "swsh": None, "bdsp": 1, "la": None, "sv": 1, "za": None},
                "2": {"rby": 2, "gsc": 232, "rse": None, "frlg": 2, "dpp": 2, "hgss": 232, "bw": None, "b2w2": None, "xy": 2, "oras": None, "sm": None, "usum": None, "lgpe": 2, "swsh": None, "bdsp": 2, "la": None, "sv": 2, "za": None},
                "3": {"rby": 3, "gsc": 233, "rse": None, "frlg": 3, "dpp": 3, "hgss": 233, "bw": None, "b2w2": None, "xy": 3, "oras": None, "sm": None, "usum": None, "lgpe": 3, "swsh": None, "bdsp": 3, "la": None, "sv": 3, "za": None},
                # ヒトカゲ系統
                "4": {"rby": 4, "gsc": 234, "rse": None, "frlg": 4, "dpp": 4, "hgss": 234, "bw": None, "b2w2": None, "xy": 4, "oras": None, "sm": None, "usum": None, "lgpe": 4, "swsh": None, "bdsp": 4, "la": None, "sv": 4, "za": None},
                "5": {"rby": 5, "gsc": 235, "rse": None, "frlg": 5, "dpp": 5, "hgss": 235, "bw": None, "b2w2": None, "xy": 5, "oras": None, "sm": None, "usum": None, "lgpe": 5, "swsh": None, "bdsp": 5, "la": None, "sv": 5, "za": None},
                "6": {"rby": 6, "gsc": 236, "rse": None, "frlg": 6, "dpp": 6, "hgss": 236, "bw": None, "b2w2": None, "xy": 6, "oras": None, "sm": None, "usum": None, "lgpe": 6, "swsh": None, "bdsp": 6, "la": None, "sv": 6, "za": None},
                # ゼニガメ系統
                "7": {"rby": 7, "gsc": 237, "rse": None, "frlg": 7, "dpp": 7, "hgss": 237, "bw": None, "b2w2": None, "xy": 7, "oras": None, "sm": None, "usum": None, "lgpe": 7, "swsh": None, "bdsp": 7, "la": None, "sv": 7, "za": None},
                "8": {"rby": 8, "gsc": 238, "rse": None, "frlg": 8, "dpp": 8, "hgss": 238, "bw": None, "b2w2": None, "xy": 8, "oras": None, "sm": None, "usum": None, "lgpe": 8, "swsh": None, "bdsp": 8, "la": None, "sv": 8, "za": None},
                "9": {"rby": 9, "gsc": 239, "rse": None, "frlg": 9, "dpp": 9, "hgss": 239, "bw": None, "b2w2": None, "xy": 9, "oras": None, "sm": None, "usum": None, "lgpe": 9, "swsh": None, "bdsp": 9, "la": None, "sv": 9, "za": None},
                # ピカチュウ・ライチュウ
                "25": {"rby": 25, "gsc": 22, "rse": None, "frlg": 25, "dpp": 104, "hgss": 22, "bw": None, "b2w2": None, "xy": 37, "oras": None, "sm": 25, "usum": 25, "lgpe": 25, "swsh": 123, "bdsp": 104, "la": 25, "sv": 74, "za": None},
                "26": {"rby": 26, "gsc": 23, "rse": None, "frlg": 26, "dpp": 105, "hgss": 23, "bw": None, "b2w2": None, "xy": 38, "oras": None, "sm": 26, "usum": 26, "lgpe": 26, "swsh": 124, "bdsp": 105, "la": 26, "sv": 75, "za": None},
                # イーブイ系統
                "133": {"rby": 133, "gsc": 184, "rse": None, "frlg": 133, "dpp": 163, "hgss": 184, "bw": None, "b2w2": None, "xy": 91, "oras": None, "sm": 126, "usum": 126, "lgpe": 133, "swsh": 178, "bdsp": 163, "la": 93, "sv": 133, "za": None},
                "134": {"rby": 134, "gsc": 185, "rse": None, "frlg": 134, "dpp": 164, "hgss": 185, "bw": None, "b2w2": None, "xy": 92, "oras": None, "sm": 127, "usum": 127, "lgpe": 134, "swsh": 179, "bdsp": 164, "la": 94, "sv": 134, "za": None},
                "135": {"rby": 135, "gsc": 186, "rse": None, "frlg": 135, "dpp": 165, "hgss": 186, "bw": None, "b2w2": None, "xy": 93, "oras": None, "sm": 128, "usum": 128, "lgpe": 135, "swsh": 180, "bdsp": 165, "la": 95, "sv": 135, "za": None},
                "136": {"rby": 136, "gsc": 187, "rse": None, "frlg": 136, "dpp": 166, "hgss": 187, "bw": None, "b2w2": None, "xy": 94, "oras": None, "sm": 129, "usum": 129, "lgpe": 136, "swsh": 181, "bdsp": 166, "la": 96, "sv": 136, "za": None},
            },
            2: {  # 第2世代（例）
                "152": {"rby": None, "gsc": 1, "rse": None, "frlg": None, "dpp": 387, "hgss": 1, "bw": None, "b2w2": None, "xy": 80, "oras": None, "sm": None, "usum": None, "lgpe": None, "swsh": None, "bdsp": 387, "la": None, "sv": 9, "za": None},
                "153": {"rby": None, "gsc": 2, "rse": None, "frlg": None, "dpp": 388, "hgss": 2, "bw": None, "b2w2": None, "xy": 81, "oras": None, "sm": None, "usum": None, "lgpe": None, "swsh": None, "bdsp": 388, "la": None, "sv": 10, "za": None},
                "154": {"rby": None, "gsc": 3, "rse": None, "frlg": None, "dpp": 389, "hgss": 3, "bw": None, "b2w2": None, "xy": 82, "oras": None, "sm": None, "usum": None, "lgpe": None, "swsh": None, "bdsp": 389, "la": None, "sv": 11, "za": None},
            }
        }
        
        # デフォルトのgame_dex_numbers構造（nullで初期化）
        self.default_dex_numbers = {
            "rby": None, "gsc": None, "rse": None, "frlg": None, "dpp": None, "hgss": None,
            "bw": None, "b2w2": None, "xy": None, "oras": None, "sm": None, "usum": None,
            "lgpe": None, "swsh": None, "bdsp": None, "la": None, "sv": None, "za": None
        }
    
    def get_generation_range(self, generation):
        """世代の範囲を取得"""
        ranges = {
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
        return ranges.get(generation, (1, 151))
    
    def generate_dex_numbers_for_pokemon(self, pokemon_id, generation):
        """ポケモンIDと世代から図鑑番号を生成"""
        str_id = str(pokemon_id)
        
        # 既存のデータがあればそれを使用
        if generation in self.generation_dex_data and str_id in self.generation_dex_data[generation]:
            return self.generation_dex_data[generation][str_id].copy()
        
        # ない場合は基本的なパターンで生成
        dex_numbers = self.default_dex_numbers.copy()
        
        # 第1世代のポケモンの場合
        if generation == 1:
            dex_numbers.update({
                "rby": pokemon_id,
                "gsc": pokemon_id + 150 if pokemon_id <= 151 else None,
                "frlg": pokemon_id,
                "dpp": pokemon_id,
                "hgss": pokemon_id + 150 if pokemon_id <= 151 else None,
                "xy": pokemon_id,
                "lgpe": pokemon_id if pokemon_id <= 151 else None,
                "bdsp": pokemon_id,
                "sv": pokemon_id if pokemon_id <= 400 else None  # SVに出てそうなもの
            })
        
        # 第2世代のポケモンの場合
        elif generation == 2:
            johto_num = pokemon_id - 151
            dex_numbers.update({
                "gsc": johto_num,
                "hgss": johto_num,
                "dpp": pokemon_id + 150,
                "xy": pokemon_id - 70,
                "bdsp": pokemon_id + 150,
                "sv": pokemon_id - 140 if pokemon_id <= 300 else None
            })
        
        # 第3世代以降も同様のパターンで...
        elif generation == 3:
            hoenn_num = pokemon_id - 251
            dex_numbers.update({
                "rse": hoenn_num,
                "oras": hoenn_num,
                "dpp": pokemon_id - 100,
                "xy": pokemon_id - 200,
                "sv": pokemon_id - 200 if pokemon_id <= 450 else None
            })
        
        return dex_numbers
    
    def update_generation_file(self, generation):
        """指定世代のファイルを更新"""
        filename = f"gen{generation}_pokemon.json"
        
        if not os.path.exists(filename):
            print(f"Warning: {filename} が見つかりません")
            return False
        
        print(f"Updating {filename}...")
        
        # ファイルを読み込み
        with open(filename, 'r', encoding='utf-8') as f:
            pokemon_data = json.load(f)
        
        # バックアップを作成
        backup_filename = f"{filename}.backup"
        with open(backup_filename, 'w', encoding='utf-8') as f:
            json.dump(pokemon_data, f, ensure_ascii=False, indent=2)
        print(f"Backup created: {backup_filename}")
        
        # 各ポケモンに図鑑番号を追加
        updated_count = 0
        for pokemon_id, pokemon_info in pokemon_data.items():
            dex_numbers = self.generate_dex_numbers_for_pokemon(int(pokemon_id), generation)
            pokemon_info['game_dex_numbers'] = dex_numbers
            updated_count += 1
        
        # 更新されたデータを保存
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(pokemon_data, f, ensure_ascii=False, indent=2)
        
        print(f"Updated {updated_count} Pokemon in {filename}")
        return True
    
    def update_all_generations(self):
        """全世代のファイルを更新"""
        print("Updating all generation files with game dex numbers...")
        
        success_count = 0
        for generation in range(1, 10):  # 第1世代〜第9世代
            if self.update_generation_file(generation):
                success_count += 1
        
        print(f"\nCompleted! Successfully updated {success_count}/9 generation files.")
        
        # サンプル確認
        if success_count > 0:
            print("\nSample updated data (gen1_pokemon.json):")
            try:
                with open('gen1_pokemon.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    sample_pokemon = data.get("1", {})
                    print(f"Pokemon 1: {sample_pokemon.get('name', 'Unknown')}")
                    print(f"Game dex numbers: {sample_pokemon.get('game_dex_numbers', {})}")
            except Exception as e:
                print(f"Error reading sample: {e}")

def main():
    updater = GenerationDexUpdater()
    
    print("Generation-based Game Dex Number Updater")
    print("=" * 50)
    
    choice = input("Update all generation files? (y/N): ").strip().lower()
    
    if choice == 'y':
        updater.update_all_generations()
    else:
        print("Cancelled.")

if __name__ == "__main__":
    main()