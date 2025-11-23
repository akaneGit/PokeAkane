#!/usr/bin/env python3
"""
PokemonDB内を詳しく探索して失敗したフォルム画像を取得するスクリプト
"""

import requests
import time
import os
from pathlib import Path
from urllib.parse import urljoin

class PokemonDBExplorer:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.patterns_path = self.base_path / "pokemon_images" / "patterns"
        self.forms_path = self.base_path / "pokemon_images" / "forms"
        
        # 保存フォルダ作成
        self.patterns_path.mkdir(parents=True, exist_ok=True)
        self.forms_path.mkdir(parents=True, exist_ok=True)
        
        self.delay = 1
        
        # 詳細検索対象
        self.target_forms = [
            # パルデアケンタロス
            {
                "pokemon_id": 128,
                "pokemon_name": "tauros", 
                "forms": [
                    {"form_name": "combat", "jp": "パルデア（コンバット）", "full_name": "tauros-combat", "save_to": "forms"},
                    {"form_name": "blaze", "jp": "パルデア（ブレイズ）", "full_name": "tauros-blaze", "save_to": "forms"},
                    {"form_name": "aqua", "jp": "パルデア（アクア）", "full_name": "tauros-aqua", "save_to": "forms"}
                ]
            },
            # ガラルペルシアン
            {
                "pokemon_id": 53,
                "pokemon_name": "persian",
                "forms": [
                    {"form_name": "galar", "jp": "ガラルペルシアン", "full_name": "persian-galar", "save_to": "forms"}
                ]
            },
            # ネクロズマ
            {
                "pokemon_id": 800,
                "pokemon_name": "necrozma",
                "forms": [
                    {"form_name": "dusk", "jp": "ネクロズマ（たそがれ）", "full_name": "necrozma-dusk-mane", "save_to": "patterns"},
                    {"form_name": "dawn", "jp": "ネクロズマ（あかつき）", "full_name": "necrozma-dawn-wings", "save_to": "patterns"}
                ]
            }
        ]

    def download_image(self, url, filepath, description):
        """画像をダウンロードして保存"""
        try:
            print(f"ダウンロード中: {description}")
            print(f"URL: {url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                print(f"✅ 成功: {filepath}")
                time.sleep(self.delay)
                return True
            else:
                print(f"❌ 失敗: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ エラー: {e}")
            return False

    def try_pokemondb_variants(self, form_info, pokemon_info, description, save_path, is_shiny=False):
        """PokemonDBの様々なURL形式を試す"""
        
        pokemon_name = pokemon_info["pokemon_name"]
        form_name = form_info["form_name"]
        full_name = form_info["full_name"]
        pokemon_id = pokemon_info["pokemon_id"]
        
        # 試すURL形式のリスト
        url_patterns = []
        
        if is_shiny:
            base_paths = [
                "https://img.pokemondb.net/sprites/home/shiny/",
                "https://img.pokemondb.net/artwork/shiny/",
                "https://img.pokemondb.net/sprites/sword-shield/shiny/",
                "https://img.pokemondb.net/sprites/scarlet-violet/shiny/",
                "https://img.pokemondb.net/sprites/legends-arceus/shiny/",
                "https://img.pokemondb.net/sprites/go/shiny/"
            ]
            extensions = [".png", ".jpg", ".gif"]
            
            # 様々な名前形式を試す
            name_variants = [
                full_name,
                f"{pokemon_name}-{form_name}",
                f"{pokemon_name}_{form_name}",
                f"{form_name}-{pokemon_name}",
                f"{pokemon_id:03d}-{form_name}",
                f"{pokemon_name}-paldea-{form_name}" if form_name in ["combat", "blaze", "aqua"] else f"{pokemon_name}-{form_name}",
                f"paldea-{pokemon_name}-{form_name}" if form_name in ["combat", "blaze", "aqua"] else f"{pokemon_name}-{form_name}"
            ]
        else:
            base_paths = [
                "https://img.pokemondb.net/sprites/home/normal/",
                "https://img.pokemondb.net/artwork/",
                "https://img.pokemondb.net/sprites/sword-shield/normal/",
                "https://img.pokemondb.net/sprites/scarlet-violet/normal/",
                "https://img.pokemondb.net/sprites/legends-arceus/normal/",
                "https://img.pokemondb.net/sprites/go/normal/",
                "https://img.pokemondb.net/sprites/bank/"
            ]
            extensions = [".png", ".jpg", ".gif"]
            
            name_variants = [
                full_name,
                f"{pokemon_name}-{form_name}",
                f"{pokemon_name}_{form_name}",
                f"{form_name}-{pokemon_name}",
                f"{pokemon_id:03d}-{form_name}",
                f"{pokemon_name}-paldea-{form_name}" if form_name in ["combat", "blaze", "aqua"] else f"{pokemon_name}-{form_name}",
                f"paldea-{pokemon_name}-{form_name}" if form_name in ["combat", "blaze", "aqua"] else f"{pokemon_name}-{form_name}"
            ]
        
        # URL組み立て
        for base_path in base_paths:
            for name_variant in name_variants:
                for ext in extensions:
                    url_patterns.append(f"{base_path}{name_variant}{ext}")
        
        # URL試行
        for url in url_patterns:
            print(f"  試行中: {url}")
            
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                response = requests.head(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    print(f"  ✅ 発見: {url}")
                    # 実際にダウンロード
                    if self.download_image(url, save_path, description):
                        return True
                
            except:
                pass
                
            time.sleep(0.3)  # 短い間隔
        
        return False

    def explore_pokemondb(self):
        """PokemonDB内を詳しく探索"""
        print("🔍 PokemonDB内詳細探索開始")
        
        success_count = 0
        total_count = 0
        
        for pokemon_info in self.target_forms:
            pokemon_id = pokemon_info["pokemon_id"]
            pokemon_name = pokemon_info["pokemon_name"]
            
            print(f"\n=== {pokemon_name.upper()} (ID: {pokemon_id}) ===")
            
            for form_info in pokemon_info["forms"]:
                form_name = form_info["form_name"]
                jp_name = form_info["jp"]
                save_to = form_info["save_to"]
                
                # ファイル名を決定
                if save_to == "forms":
                    normal_filename = f"{pokemon_id:03d}_{pokemon_name}_{form_name}.png"
                    shiny_filename = f"{pokemon_id:03d}_{pokemon_name}_{form_name}_shiny.png"
                    normal_path = self.forms_path / normal_filename
                    shiny_path = self.forms_path / shiny_filename
                else:  # patterns
                    normal_filename = f"{pokemon_id:03d}_{pokemon_name}_{form_name}.png"
                    shiny_filename = f"{pokemon_id:03d}_{pokemon_name}_{form_name}_shiny.png"
                    normal_path = self.patterns_path / normal_filename
                    shiny_path = self.patterns_path / shiny_filename
                
                # 通常画像を探索
                total_count += 1
                print(f"\n--- {jp_name} (通常) ---")
                if self.try_pokemondb_variants(form_info, pokemon_info, f"{jp_name} (通常)", normal_path, False):
                    success_count += 1
                else:
                    print(f"  ❌ 通常画像が見つかりませんでした")
                
                # 色違い画像を探索
                total_count += 1
                print(f"\n--- {jp_name} (色違い) ---")
                if self.try_pokemondb_variants(form_info, pokemon_info, f"{jp_name} (色違い)", shiny_path, True):
                    success_count += 1
                else:
                    print(f"  ❌ 色違い画像が見つかりませんでした")
        
        print(f"\n✅ PokemonDB探索完了: {success_count}/{total_count}個発見")
        return success_count

def main():
    base_path = r"C:\Users\rarur\OneDrive\ドキュメント\GitHub\PokeAkane"
    explorer = PokemonDBExplorer(base_path)
    
    # PokemonDBを詳しく探索
    explorer.explore_pokemondb()
    
    print("\n🌟 PokemonDB詳細探索完了！")

if __name__ == "__main__":
    main()