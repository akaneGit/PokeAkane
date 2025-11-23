#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PokeAPIから全地方図鑑データを取得するツール
33個の図鑑から地方図鑑番号を収集し、既存のgame_dex_numbers形式で保存
"""

import json
import requests
import time
from typing import Dict, Any, Optional

class PokeAPICollector:
    def __init__(self):
        self.base_url = "https://pokeapi.co/api/v2"
        
        # PokeAPI図鑑名 → 既存ソフト略称のマッピング
        self.pokedex_mapping = {
            # 第1世代
            "kanto": "rby",
            "letsgo-kanto": "lgpe",
            
            # 第2世代
            "original-johto": "gsc",
            "updated-johto": "hgss",
            
            # 第3世代
            "hoenn": "rse",
            "updated-hoenn": "oras",
            
            # 第4世代
            "original-sinnoh": "dpp",
            "extended-sinnoh": "dpp",  # プラチナも同じ略称にする
            
            # 第5世代
            "original-unova": "bw",
            "updated-unova": "b2w2",
            
            # 第6世代
            "kalos-central": "xy",
            "kalos-coastal": "xy",
            "kalos-mountain": "xy",
            
            # 第7世代
            "original-alola": "sm",
            "original-melemele": "sm",
            "original-akala": "sm", 
            "original-ulaula": "sm",
            "original-poni": "sm",
            "updated-alola": "usum",
            "updated-melemele": "usum",
            "updated-akala": "usum",
            "updated-ulaula": "usum", 
            "updated-poni": "usum",
            
            # 第8世代
            "galar": "swsh",
            "isle-of-armor": "swsh",
            "crown-tundra": "swsh",
            
            # 第9世代
            "paldea": "sv",
            "kitakami": "sv",
            "blueberry": "sv",
            
            # その他
            "hisui": "la",
            # "national": None,  # 全国図鑑は除外
            # "conquest-gallery": None,  # ポケモン+ノブナガは除外
            # "lumiose-city": None,  # ミアレシティは除外
        }
        
        # 収集した地方図鑑データ
        self.regional_dex_data = {}
        
        # API呼び出し間の待機時間（秒）
        self.request_delay = 0.1
    
    def get_pokedex_list(self) -> list:
        """利用可能な図鑑リストを取得"""
        try:
            response = requests.get(f"{self.base_url}/pokedex/?limit=33")
            response.raise_for_status()
            data = response.json()
            return data["results"]
        except requests.RequestException as e:
            print(f"❌ 図鑑リスト取得エラー: {e}")
            return []
    
    def get_pokedex_data(self, pokedex_name: str) -> Optional[Dict[str, Any]]:
        """指定された図鑑のデータを取得"""
        try:
            print(f"🔄 {pokedex_name} 図鑑データを取得中...")
            response = requests.get(f"{self.base_url}/pokedex/{pokedex_name}/")
            response.raise_for_status()
            data = response.json()
            
            time.sleep(self.request_delay)  # API負荷軽減
            return data
        except requests.RequestException as e:
            print(f"❌ {pokedex_name} 図鑑データ取得エラー: {e}")
            return None
    
    def extract_pokemon_entries(self, pokedex_data: Dict[str, Any]) -> Dict[str, int]:
        """図鑑データからポケモンエントリを抽出"""
        entries = {}
        
        for entry in pokedex_data.get("pokemon_entries", []):
            entry_number = entry.get("entry_number")
            pokemon_species = entry.get("pokemon_species", {})
            pokemon_url = pokemon_species.get("url", "")
            
            # URLから全国図鑑番号を抽出
            if pokemon_url:
                national_number = pokemon_url.rstrip("/").split("/")[-1]
                entries[national_number] = entry_number
        
        return entries
    
    def collect_all_regional_data(self):
        """全地方図鑑データを収集"""
        print("🚀 PokeAPIから地方図鑑データ収集開始！")
        
        # 図鑑リストを取得
        pokedex_list = self.get_pokedex_list()
        if not pokedex_list:
            print("❌ 図鑑リスト取得に失敗")
            return
        
        print(f"📋 {len(pokedex_list)}個の図鑑を発見")
        
        # 各図鑑からデータを収集
        for pokedex_info in pokedex_list:
            pokedex_name = pokedex_info["name"]
            
            # マッピング対象外の図鑑はスキップ
            if pokedex_name not in self.pokedex_mapping:
                print(f"⏭️  {pokedex_name} をスキップ（マッピング対象外）")
                continue
            
            # 図鑑データを取得
            pokedex_data = self.get_pokedex_data(pokedex_name)
            if not pokedex_data:
                continue
            
            # ポケモンエントリを抽出
            entries = self.extract_pokemon_entries(pokedex_data)
            if not entries:
                print(f"⚠️  {pokedex_name} にはエントリが見つかりませんでした")
                continue
            
            # ソフト略称を取得
            software_key = self.pokedex_mapping[pokedex_name]
            
            print(f"✅ {pokedex_name} → {software_key}: {len(entries)}匹のポケモン")
            
            # データを統合
            for national_num, regional_num in entries.items():
                if national_num not in self.regional_dex_data:
                    self.regional_dex_data[national_num] = {}
                
                # 既存のデータがある場合は警告
                if software_key in self.regional_dex_data[national_num]:
                    existing = self.regional_dex_data[national_num][software_key]
                    if existing != regional_num:
                        print(f"⚠️  #{national_num} {software_key}: {existing} → {regional_num} に更新")
                
                self.regional_dex_data[national_num][software_key] = regional_num
        
        print(f"\n🎉 データ収集完了！{len(self.regional_dex_data)}匹のポケモンデータを取得")
    
    def save_collected_data(self, filename: str = "pokeapi_regional_dex_data.json"):
        """収集したデータをJSONファイルに保存"""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.regional_dex_data, f, ensure_ascii=False, indent=2)
            print(f"💾 データを {filename} に保存しました")
        except Exception as e:
            print(f"❌ データ保存エラー: {e}")
    
    def print_summary(self):
        """収集データの統計を表示"""
        if not self.regional_dex_data:
            print("📊 データがありません")
            return
        
        print("\n📊 収集データ統計:")
        print(f"  全ポケモン数: {len(self.regional_dex_data)}")
        
        # ソフト別統計
        software_stats = {}
        for pokemon_data in self.regional_dex_data.values():
            for software in pokemon_data.keys():
                software_stats[software] = software_stats.get(software, 0) + 1
        
        print("  ソフト別登録数:")
        for software, count in sorted(software_stats.items()):
            print(f"    {software}: {count}匹")
        
        # サンプルデータ表示
        print("\n📝 サンプルデータ (最初の5匹):")
        for i, (national_num, data) in enumerate(list(self.regional_dex_data.items())[:5]):
            print(f"  #{national_num}: {data}")

def main():
    """メイン処理"""
    collector = PokeAPICollector()
    
    print("=" * 60)
    print("🌟 PokeAPI 地方図鑑データコレクター")
    print("=" * 60)
    
    # データ収集実行
    collector.collect_all_regional_data()
    
    # 統計表示
    collector.print_summary()
    
    # データ保存
    collector.save_collected_data()
    
    print("\n✨ 処理完了！")

if __name__ == "__main__":
    main()