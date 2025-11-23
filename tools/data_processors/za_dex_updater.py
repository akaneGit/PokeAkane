#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ポケモンレジェンズZ-A の図鑑番号を実装するツール
カロス地方（XY）のポケモンを基準にZA図鑑を作成
"""

import json
import os
from typing import Dict, Any

class ZADexUpdater:
    def __init__(self):
        self.generation_files = [
            'gen1_pokemon.json', 'gen2_pokemon.json', 'gen3_pokemon.json',
            'gen4_pokemon.json', 'gen5_pokemon.json', 'gen6_pokemon.json',
            'gen7_pokemon.json', 'gen8_pokemon.json', 'gen9_pokemon.json'
        ]
        
    def create_za_dex_mapping(self) -> Dict[int, int]:
        """XYのポケモンを基準にZA図鑑番号を作成"""
        za_dex_mapping = {}
        dex_number = 1
        
        # 全世代のデータを読み込み
        all_pokemon = {}
        for gen_file in self.generation_files:
            if os.path.exists(gen_file):
                with open(gen_file, 'r', encoding='utf-8') as f:
                    gen_data = json.load(f)
                    all_pokemon.update(gen_data)
        
        print(f"読み込み完了: {len(all_pokemon)}匹のポケモン")
        
        # XYに登場するポケモンを収集（カロス3図鑑のいずれかに登録されているポケモン）
        xy_pokemon = []
        for pokemon_id, pokemon_data in all_pokemon.items():
            game_dex = pokemon_data.get('game_dex_numbers', {})
            xy_dex_num = game_dex.get('xy')
            
            if xy_dex_num is not None:
                xy_pokemon.append((int(pokemon_id), xy_dex_num, pokemon_data['name']))
        
        # XYの図鑑番号順にソート
        xy_pokemon.sort(key=lambda x: x[1])
        
        print(f"XYに登場するポケモン数: {len(xy_pokemon)}")
        print("最初の10匹:")
        for i, (pid, xy_num, name) in enumerate(xy_pokemon[:10]):
            print(f"  {i+1:3d}. {name} (ID: {pid}, XY: {xy_num})")
        
        # ZA図鑑番号を割り当て
        for i, (pokemon_id, xy_num, name) in enumerate(xy_pokemon):
            za_dex_mapping[pokemon_id] = i + 1
        
        return za_dex_mapping
    
    def update_pokemon_data(self, za_mapping: Dict[int, int]):
        """全ポケモンデータにZA図鑑番号を追加"""
        total_updated = 0
        
        for gen_file in self.generation_files:
            if not os.path.exists(gen_file):
                continue
                
            # バックアップ作成
            backup_file = gen_file + '.backup_before_za_update'
            if not os.path.exists(backup_file):
                with open(gen_file, 'r', encoding='utf-8') as f:
                    backup_data = f.read()
                with open(backup_file, 'w', encoding='utf-8') as f:
                    f.write(backup_data)
                print(f"バックアップ作成: {backup_file}")
            
            # データ読み込み
            with open(gen_file, 'r', encoding='utf-8') as f:
                pokemon_data = json.load(f)
            
            updated_count = 0
            for pokemon_id, data in pokemon_data.items():
                pid = int(pokemon_id)
                
                # game_dex_numbersが存在しない場合は作成
                if 'game_dex_numbers' not in data:
                    data['game_dex_numbers'] = {}
                
                # ZA図鑑番号を設定
                if pid in za_mapping:
                    data['game_dex_numbers']['za'] = za_mapping[pid]
                    updated_count += 1
                else:
                    # XYに登場しないポケモンはnull
                    data['game_dex_numbers']['za'] = None
            
            # ファイル保存
            with open(gen_file, 'w', encoding='utf-8') as f:
                json.dump(pokemon_data, f, ensure_ascii=False, indent=2)
            
            print(f"{gen_file}: {updated_count}匹更新")
            total_updated += updated_count
        
        return total_updated
    
    def run(self):
        """ZA図鑑データ更新を実行"""
        print("=== ポケモンレジェンズZ-A 図鑑番号実装ツール ===")
        print()
        
        # ZA図鑑マッピング作成
        print("1. XYのポケモンを基準にZA図鑑番号を作成中...")
        za_mapping = self.create_za_dex_mapping()
        
        print(f"\nZA図鑑に登録されるポケモン数: {len(za_mapping)}")
        
        # 確認
        response = input("\nポケモンデータを更新しますか？ (y/n): ")
        if response.lower() != 'y':
            print("キャンセルしました。")
            return
        
        # データ更新
        print("\n2. ポケモンデータを更新中...")
        total_updated = self.update_pokemon_data(za_mapping)
        
        print(f"\n=== 更新完了 ===")
        print(f"合計 {total_updated} 匹のポケモンにZA図鑑番号を設定しました")
        print(f"ZAに登場しないポケモンはnullに設定されました")
        
        # サンプル表示
        print("\n=== ZA図鑑サンプル ===")
        with open('gen6_pokemon.json', 'r', encoding='utf-8') as f:
            gen6_data = json.load(f)
        
        za_pokemon = []
        for pid, data in gen6_data.items():
            za_num = data.get('game_dex_numbers', {}).get('za')
            if za_num is not None:
                za_pokemon.append((za_num, data['name']))
        
        za_pokemon.sort()
        print("最初の10匹:")
        for za_num, name in za_pokemon[:10]:
            print(f"  {za_num:3d}. {name}")

if __name__ == "__main__":
    updater = ZADexUpdater()
    updater.run()