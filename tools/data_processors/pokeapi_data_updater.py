#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PokeAPIデータを使用して全世代ファイルのgame_dex_numbersを更新するツール
pokeapi_regional_dex_data.jsonから取得したデータで全ポケモンファイルを一括更新
"""

import json
import os
from typing import Dict, Any

class PokeAPIDataUpdater:
    def __init__(self):
        self.pokeapi_data_file = "pokeapi_regional_dex_data.json"
        self.generation_files = [
            "gen1_pokemon.json", "gen2_pokemon.json", "gen3_pokemon.json",
            "gen4_pokemon.json", "gen5_pokemon.json", "gen6_pokemon.json", 
            "gen7_pokemon.json", "gen8_pokemon.json", "gen9_pokemon.json"
        ]
        
        # 基本のgame_dex_numbers構造（全てnullで初期化）
        self.base_game_dex_numbers = {
            "rby": None, "gsc": None, "rse": None, "frlg": None, "dpp": None, "hgss": None,
            "bw": None, "b2w2": None, "xy": None, "oras": None, "sm": None, "usum": None,
            "lgpe": None, "swsh": None, "bdsp": None, "la": None, "sv": None, "za": None
        }
        
        # PokeAPIから取得したデータ
        self.pokeapi_data = {}
        
        # 統計情報
        self.stats = {
            "updated_pokemon": 0,
            "total_updates": 0,
            "files_processed": 0,
            "software_stats": {}
        }
    
    def load_pokeapi_data(self) -> bool:
        """PokeAPIから取得したデータを読み込み"""
        try:
            if not os.path.exists(self.pokeapi_data_file):
                print(f"❌ {self.pokeapi_data_file} が見つかりません")
                return False
            
            with open(self.pokeapi_data_file, "r", encoding="utf-8") as f:
                self.pokeapi_data = json.load(f)
            
            print(f"✅ {len(self.pokeapi_data)}匹のPokeAPIデータを読み込みました")
            return True
        except Exception as e:
            print(f"❌ PokeAPIデータ読み込みエラー: {e}")
            return False
    
    def update_pokemon_file(self, filename: str) -> bool:
        """指定されたポケモンファイルを更新"""
        try:
            if not os.path.exists(filename):
                print(f"⚠️  {filename} が見つかりません")
                return False
            
            # ファイルを読み込み
            with open(filename, "r", encoding="utf-8") as f:
                pokemon_data = json.load(f)
            
            updated_count = 0
            
            # 各ポケモンを更新（辞書形式）
            for pokemon_id, pokemon in pokemon_data.items():
                
                if pokemon_id in self.pokeapi_data:
                    # 基本構造をコピー
                    updated_game_dex = self.base_game_dex_numbers.copy()
                    
                    # PokeAPIデータでnullでない値を上書き
                    pokeapi_pokemon_data = self.pokeapi_data[pokemon_id]
                    for software, dex_num in pokeapi_pokemon_data.items():
                        if software in updated_game_dex and dex_num is not None:
                            updated_game_dex[software] = dex_num
                            
                            # 統計更新
                            if software not in self.stats["software_stats"]:
                                self.stats["software_stats"][software] = 0
                            self.stats["software_stats"][software] += 1
                            self.stats["total_updates"] += 1
                    
                    # game_dex_numbersを更新
                    pokemon["game_dex_numbers"] = updated_game_dex
                    updated_count += 1
            
            # ファイルに書き戻し
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(pokemon_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ {filename}: {updated_count}匹のポケモンを更新")
            self.stats["updated_pokemon"] += updated_count
            self.stats["files_processed"] += 1
            return True
            
        except Exception as e:
            print(f"❌ {filename} 更新エラー: {e}")
            return False
    
    def update_all_files(self):
        """全世代ファイルを更新"""
        print("🚀 全世代ファイルのgame_dex_numbers更新開始！")
        
        success_count = 0
        
        for filename in self.generation_files:
            print(f"\n🔄 {filename} を処理中...")
            
            if self.update_pokemon_file(filename):
                success_count += 1
        
        print(f"\n🎉 処理完了！{success_count}/{len(self.generation_files)}ファイルを更新")
    
    def print_statistics(self):
        """更新統計を表示"""
        print("\n" + "="*60)
        print("📊 更新統計情報")
        print("="*60)
        print(f"処理ファイル数: {self.stats['files_processed']}")
        print(f"更新ポケモン数: {self.stats['updated_pokemon']}")
        print(f"総更新エントリ数: {self.stats['total_updates']}")
        
        print("\n🎮 ソフト別更新エントリ数:")
        for software, count in sorted(self.stats["software_stats"].items()):
            print(f"  {software}: {count}エントリ")
        
        # 平均エントリ数計算
        if self.stats["updated_pokemon"] > 0:
            avg_entries = self.stats["total_updates"] / self.stats["updated_pokemon"]
            print(f"\n📈 1匹あたり平均エントリ数: {avg_entries:.1f}")
    
    def verify_sample_updates(self):
        """サンプル更新結果を確認"""
        print("\n🔍 サンプル更新結果確認 (フシギダネ、ピカチュウ、イーブイ):")
        
        sample_ids = ["1", "25", "133"]  # フシギダネ、ピカチュウ、イーブイ
        
        for pokemon_id in sample_ids:
            if pokemon_id in self.pokeapi_data:
                print(f"\n  #{pokemon_id} PokeAPIデータ:")
                for software, dex_num in self.pokeapi_data[pokemon_id].items():
                    if dex_num is not None:
                        print(f"    {software}: {dex_num}")

def main():
    """メイン処理"""
    updater = PokeAPIDataUpdater()
    
    print("=" * 60)
    print("🌟 PokeAPI地方図鑑データ一括更新ツール")
    print("=" * 60)
    
    # PokeAPIデータ読み込み
    if not updater.load_pokeapi_data():
        return
    
    # サンプル確認
    updater.verify_sample_updates()
    
    # 確認プロンプト
    print("\n" + "="*60)
    response = input("🚨 全世代ファイルを更新しますか？ (y/N): ").strip().lower()
    
    if response == 'y':
        # 全ファイル更新
        updater.update_all_files()
        
        # 統計表示
        updater.print_statistics()
        
        print("\n✨ 全ての更新が完了しました！")
        print("💡 pokemon_gallery.htmlでソフト別フィルタリングが完璧に動作します！")
    else:
        print("❌ 更新をキャンセルしました")

if __name__ == "__main__":
    main()