#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ポケモンレジェンズZ-Aの実際の図鑑データを収集するツール
複数のソースから最新データを取得
"""

import json
import requests
import time
from typing import Dict, Any, Optional

class ZADataCollector:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def check_pokeapi_za_data(self):
        """PokeAPIでZA図鑑データをチェック"""
        print("=== PokeAPI でZA図鑑データをチェック ===")
        
        try:
            # 図鑑一覧を取得
            response = self.session.get("https://pokeapi.co/api/v2/pokedex/")
            pokedex_list = response.json()
            
            print(f"利用可能な図鑑数: {pokedex_list['count']}")
            
            # ZA関連の図鑑を探す
            za_pokedexes = []
            for pokedex in pokedex_list['results']:
                if 'za' in pokedex['name'].lower() or 'legends' in pokedex['name'].lower() or 'kalos' in pokedex['name'].lower():
                    za_pokedexes.append(pokedex)
            
            print("ZA/カロス関連の図鑑:")
            for pokedex in za_pokedexes:
                print(f"  - {pokedex['name']}: {pokedex['url']}")
            
            # 特定の図鑑の詳細をチェック
            if za_pokedexes:
                pokedex_url = za_pokedexes[0]['url']
                response = self.session.get(pokedex_url)
                pokedex_data = response.json()
                
                print(f"\n{pokedex_data['name']} の詳細:")
                print(f"  ポケモン数: {len(pokedex_data['pokemon_entries'])}")
                print("  最初の10匹:")
                for entry in pokedex_data['pokemon_entries'][:10]:
                    print(f"    {entry['entry_number']:3d}. {entry['pokemon_species']['name']}")
        
        except Exception as e:
            print(f"PokeAPIエラー: {e}")
    
    def check_bulbapedia_data(self):
        """Bulbapediaから情報を取得（参考用）"""
        print("\n=== Bulbapedia 参考情報 ===")
        
        # BulbapediaのZA図鑑ページをチェック（実際のスクレイピングは避ける）
        za_urls = [
            "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_Kalos_Pok%C3%A9dex_number",
            "https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_Legends:_Z-A"
        ]
        
        print("参考URL:")
        for url in za_urls:
            print(f"  - {url}")
    
    def check_serebii_reference(self):
        """Serebii.net の参考情報"""
        print("\n=== Serebii.net 参考情報 ===")
        
        serebii_urls = [
            "https://www.serebii.net/legendsza/",
            "https://www.serebii.net/pokedex-xy/"
        ]
        
        print("参考URL:")
        for url in serebii_urls:
            print(f"  - {url}")
    
    def create_za_from_xy_plus_new(self):
        """XYベース + 新ポケモンでZA図鑑を作成"""
        print("\n=== XY + 新ポケモンベースのZA図鑑作成 ===")
        
        # 現在のデータを読み込み
        all_pokemon = {}
        generation_files = [
            'gen1_pokemon.json', 'gen2_pokemon.json', 'gen3_pokemon.json',
            'gen4_pokemon.json', 'gen5_pokemon.json', 'gen6_pokemon.json',
            'gen7_pokemon.json', 'gen8_pokemon.json', 'gen9_pokemon.json'
        ]
        
        for gen_file in generation_files:
            try:
                with open(gen_file, 'r', encoding='utf-8') as f:
                    gen_data = json.load(f)
                    all_pokemon.update(gen_data)
            except FileNotFoundError:
                continue
        
        # XYに登場するポケモンを収集
        xy_pokemon = []
        new_pokemon = []  # 第7世代以降の一部を含める可能性
        
        for pokemon_id, pokemon_data in all_pokemon.items():
            game_dex = pokemon_data.get('game_dex_numbers', {})
            pid = int(pokemon_id)
            
            # XYに登場
            if game_dex.get('xy') is not None:
                xy_pokemon.append((pid, game_dex.get('xy'), pokemon_data['name']))
            # 第7世代以降の人気ポケモンも含める可能性（例：ミミッキュなど）
            elif pid >= 778 and pid <= 781:  # ミミッキュ周辺
                new_pokemon.append((pid, pokemon_data['name']))
        
        xy_pokemon.sort(key=lambda x: x[1])  # XY図鑑番号順
        
        print(f"XYポケモン: {len(xy_pokemon)}匹")
        print(f"追加候補: {len(new_pokemon)}匹")
        
        # ZA図鑑作成（XY + α）
        za_mapping = {}
        dex_num = 1
        
        # XYポケモンを先に追加
        for pid, xy_num, name in xy_pokemon:
            za_mapping[pid] = dex_num
            dex_num += 1
        
        # 新ポケモンを追加
        for pid, name in new_pokemon:
            za_mapping[pid] = dex_num
            dex_num += 1
        
        print(f"\nZA図鑑予想ポケモン数: {len(za_mapping)}")
        
        return za_mapping
    
    def run(self):
        """データ収集実行"""
        print("=== ポケモンレジェンズZ-A 図鑑データ収集 ===")
        
        self.check_pokeapi_za_data()
        self.check_bulbapedia_data()
        self.check_serebii_reference()
        
        print("\n" + "="*50)
        print("実際のZA図鑑データが見つからない場合、")
        print("XYベース + 新ポケモンで暫定図鑑を作成することもできます。")
        
        response = input("\n暫定ZA図鑑を作成しますか？ (y/n): ")
        if response.lower() == 'y':
            za_mapping = self.create_za_from_xy_plus_new()
            
            # 現在のZA図鑑と比較
            with open('gen6_pokemon.json', 'r', encoding='utf-8') as f:
                gen6_data = json.load(f)
            
            current_za_count = 0
            for pokemon_data in gen6_data.values():
                if pokemon_data.get('game_dex_numbers', {}).get('za') is not None:
                    current_za_count += 1
            
            print(f"\n現在のZA図鑑: {current_za_count}匹")
            print(f"新しいZA図鑑: {len(za_mapping)}匹")

if __name__ == "__main__":
    collector = ZADataCollector()
    collector.run()