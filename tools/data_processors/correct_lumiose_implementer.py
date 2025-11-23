#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PokeAPIのlumiose-city図鑑を使ってZA図鑑を正確に実装（修正版）
IDベースでマッピング
"""

import json
import requests
import os
from typing import Dict, Any

class CorrectLumioseDexImplementer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.generation_files = [
            'gen1_pokemon.json', 'gen2_pokemon.json', 'gen3_pokemon.json',
            'gen4_pokemon.json', 'gen5_pokemon.json', 'gen6_pokemon.json',
            'gen7_pokemon.json', 'gen8_pokemon.json', 'gen9_pokemon.json'
        ]
    
    def fetch_lumiose_city_dex_correct(self) -> Dict[int, int]:
        """PokeAPIからlumiose-city図鑑データを正確に取得（IDベース）"""
        print("=== PokeAPIからミアレシティ図鑑データを取得（IDベース） ===")
        
        try:
            response = self.session.get("https://pokeapi.co/api/v2/pokedex/lumiose-city/")
            lumiose_data = response.json()
            
            print(f"図鑑名: {lumiose_data['name']}")
            print(f"ポケモン数: {len(lumiose_data['pokemon_entries'])}")
            
            # 全ポケモンデータを読み込み
            all_pokemon = {}
            for gen_file in self.generation_files:
                if os.path.exists(gen_file):
                    with open(gen_file, 'r', encoding='utf-8') as f:
                        gen_data = json.load(f)
                        all_pokemon.update(gen_data)
            
            print(f"ローカルポケモンデータ: {len(all_pokemon)}匹")
            
            # ミアレシティ図鑑のマッピング作成（IDベース）
            lumiose_mapping = {}
            successful_mappings = 0
            failed_mappings = []
            
            for entry in lumiose_data['pokemon_entries']:
                pokemon_url = entry['pokemon_species']['url']
                dex_number = entry['entry_number']
                pokemon_name = entry['pokemon_species']['name']
                
                # URLからIDを抽出
                pokemon_id = int(pokemon_url.split('/')[-2])
                
                # ローカルデータに存在するかチェック
                if str(pokemon_id) in all_pokemon:
                    lumiose_mapping[pokemon_id] = dex_number
                    successful_mappings += 1
                else:
                    failed_mappings.append(f"{dex_number:3d}. {pokemon_name} (ID: {pokemon_id})")
            
            print(f"成功したマッピング: {successful_mappings}匹")
            print(f"失敗したマッピング: {len(failed_mappings)}匹")
            
            if failed_mappings:
                print("失敗したポケモン（最初の10匹）:")
                for failed in failed_mappings[:10]:
                    print(f"  {failed}")
                
                # 第5世代のポケモンが見つからない理由をチェック
                gen5_missing = [f for f in failed_mappings if '498' in f or '499' in f or '500' in f]
                if gen5_missing:
                    print("\n第5世代ポケモンが見つからない可能性があります。")
                    print("gen5_pokemon.jsonファイルを確認してください。")
            
            # サンプル表示
            print("\nミアレシティ図鑑サンプル（最初の10匹）:")
            sample_entries = sorted(lumiose_mapping.items(), key=lambda x: x[1])[:10]
            for pokemon_id, dex_num in sample_entries:
                if str(pokemon_id) in all_pokemon:
                    pokemon_name = all_pokemon[str(pokemon_id)]['name']
                    print(f"  {dex_num:3d}. {pokemon_name} (ID: {pokemon_id})")
            
            return lumiose_mapping
            
        except Exception as e:
            print(f"エラー: {e}")
            return {}
    
    def update_pokemon_data_with_lumiose_correct(self, lumiose_mapping: Dict[int, int]):
        """ポケモンデータにミアレシティ図鑑番号を正確に追加"""
        total_updated = 0
        
        for gen_file in self.generation_files:
            if not os.path.exists(gen_file):
                continue
            
            # データ読み込み
            with open(gen_file, 'r', encoding='utf-8') as f:
                pokemon_data = json.load(f)
            
            updated_count = 0
            for pokemon_id, data in pokemon_data.items():
                pid = int(pokemon_id)
                
                if 'game_dex_numbers' not in data:
                    data['game_dex_numbers'] = {}
                
                # ミアレシティ図鑑番号（ZA図鑑として）を設定
                if pid in lumiose_mapping:
                    data['game_dex_numbers']['za'] = lumiose_mapping[pid]
                    updated_count += 1
                else:
                    data['game_dex_numbers']['za'] = None
            
            # ファイル保存
            with open(gen_file, 'w', encoding='utf-8') as f:
                json.dump(pokemon_data, f, ensure_ascii=False, indent=2)
            
            if updated_count > 0:
                print(f"{gen_file}: {updated_count}匹更新")
                total_updated += updated_count
        
        return total_updated
    
    def verify_za_implementation(self):
        """ZA図鑑実装の検証"""
        print("\n=== ZA図鑑実装検証 ===")
        
        all_pokemon = {}
        for gen_file in self.generation_files:
            if os.path.exists(gen_file):
                with open(gen_file, 'r', encoding='utf-8') as f:
                    gen_data = json.load(f)
                    all_pokemon.update(gen_data)
        
        za_pokemon = []
        for pokemon_id, pokemon_data in all_pokemon.items():
            za_num = pokemon_data.get('game_dex_numbers', {}).get('za')
            if za_num is not None:
                za_pokemon.append((za_num, pokemon_data['name'], int(pokemon_id)))
        
        za_pokemon.sort()
        
        print(f"ZA図鑑に登録されたポケモン数: {len(za_pokemon)}")
        print("\nZA図鑑の最初の15匹:")
        for za_num, name, pid in za_pokemon[:15]:
            print(f"  {za_num:3d}. {name} (ID: {pid})")
    
    def run(self):
        """実行"""
        print("=== PokeAPI ミアレシティ図鑑によるZA図鑑正確実装 ===")
        print()
        
        # ミアレシティ図鑑データ取得
        lumiose_mapping = self.fetch_lumiose_city_dex_correct()
        
        if not lumiose_mapping:
            print("ミアレシティ図鑑データの取得に失敗しました。")
            return
        
        print(f"\nミアレシティ図鑑マッピング完了: {len(lumiose_mapping)}匹")
        
        # 確認
        response = input("\nポケモンデータをミアレシティ図鑑で更新しますか？ (y/n): ")
        if response.lower() != 'y':
            print("キャンセルしました。")
            return
        
        # データ更新
        print("\nポケモンデータを更新中...")
        total_updated = self.update_pokemon_data_with_lumiose_correct(lumiose_mapping)
        
        print(f"\n=== 更新完了 ===")
        print(f"合計 {total_updated} 匹のポケモンにミアレシティ図鑑番号（ZA図鑑）を設定しました")
        
        # 検証
        self.verify_za_implementation()

if __name__ == "__main__":
    implementer = CorrectLumioseDexImplementer()
    implementer.run()