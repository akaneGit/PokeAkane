#!/usr/bin/env python3
"""
失敗したフォルム画像を再取得するスクリプト
PokemonDBの別のURL形式も試す
"""

import requests
import time
import os
from pathlib import Path

class FailedFormsRetriever:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.patterns_path = self.base_path / "pokemon_images" / "patterns"
        self.forms_path = self.base_path / "pokemon_images" / "forms"
        
        # 保存フォルダ作成
        self.patterns_path.mkdir(parents=True, exist_ok=True)
        self.forms_path.mkdir(parents=True, exist_ok=True)
        
        # リクエスト間隔（秒）
        self.delay = 1
        
        # 失敗したフォルムの再取得リスト
        self.failed_forms = [
            # パルデアケンタロス
            {
                "pokemon_id": 128,
                "forms": [
                    {"name": "tauros-paldea-combat", "jp": "パルデア（コンバット）", "save_to": "forms"},
                    {"name": "tauros-paldea-blaze", "jp": "パルデア（ブレイズ）", "save_to": "forms"},
                    {"name": "tauros-paldea-aqua", "jp": "パルデア（アクア）", "save_to": "forms"}
                ]
            },
            # ガラルペルシアン
            {
                "pokemon_id": 53,
                "forms": [
                    {"name": "persian-galar", "jp": "ガラルペルシアン", "save_to": "forms"}
                ]
            },
            # ネクロズマ
            {
                "pokemon_id": 800,
                "forms": [
                    {"name": "necrozma-dusk", "jp": "ネクロズマ（たそがれ）", "save_to": "patterns"},
                    {"name": "necrozma-dawn", "jp": "ネクロズマ（あかつき）", "save_to": "patterns"}
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

    def try_multiple_urls(self, form_name, pokemon_id, description, save_path, is_shiny=False):
        """複数のURL形式を試す"""
        
        # 試すURL形式リスト
        base_urls = [
            "https://img.pokemondb.net/artwork/",
            "https://img.pokemondb.net/sprites/home/normal/",
            "https://serebii.net/pokemon/art/",
            "https://archives.bulbagarden.net/media/upload/"
        ]
        
        if is_shiny:
            base_urls = [
                "https://img.pokemondb.net/artwork/shiny/",
                "https://img.pokemondb.net/sprites/home/shiny/"
            ]
        
        # 試すファイル拡張子
        extensions = [".jpg", ".png", ".gif"]
        
        for base_url in base_urls:
            for ext in extensions:
                if "serebii.net" in base_url:
                    # Serebii形式: 3桁番号
                    url = f"{base_url}{pokemon_id:03d}.png"
                elif "bulbagarden.net" in base_url:
                    # Bulbapedia形式は複雑なのでスキップ
                    continue
                else:
                    # 通常形式
                    url = f"{base_url}{form_name}{ext}"
                
                print(f"  試行中: {url}")
                
                try:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }
                    
                    response = requests.head(url, headers=headers, timeout=10)
                    
                    if response.status_code == 200:
                        # 実際にダウンロード
                        if self.download_image(url, save_path, description):
                            return True
                    
                except:
                    continue
                    
                time.sleep(0.5)  # 短い間隔
        
        return False

    def retrieve_failed_forms(self):
        """失敗したフォルム画像を再取得"""
        print("🔄 失敗したフォルム画像の再取得開始")
        
        success_count = 0
        total_count = 0
        
        for pokemon_data in self.failed_forms:
            pokemon_id = pokemon_data["pokemon_id"]
            
            print(f"\n=== ポケモンID {pokemon_id} ===")
            
            for form_info in pokemon_data["forms"]:
                form_name = form_info["name"]
                jp_name = form_info["jp"]
                save_to = form_info["save_to"]
                
                # ファイル名を決定
                if save_to == "forms":
                    normal_filename = f"{pokemon_id:03d}_{form_name.replace('-', '_')}.png"
                    shiny_filename = f"{pokemon_id:03d}_{form_name.replace('-', '_')}_shiny.png"
                    normal_path = self.forms_path / normal_filename
                    shiny_path = self.forms_path / shiny_filename
                else:  # patterns
                    normal_filename = f"{pokemon_id:03d}_{form_name.replace('-', '_')}.png"
                    shiny_filename = f"{pokemon_id:03d}_{form_name.replace('-', '_')}_shiny.png"
                    normal_path = self.patterns_path / normal_filename
                    shiny_path = self.patterns_path / shiny_filename
                
                # 通常画像を取得
                total_count += 1
                print(f"\n--- {jp_name} (通常) ---")
                if self.try_multiple_urls(form_name, pokemon_id, f"{jp_name} (通常)", normal_path, False):
                    success_count += 1
                
                # 色違い画像を取得
                total_count += 1
                print(f"\n--- {jp_name} (色違い) ---")
                if self.try_multiple_urls(form_name, pokemon_id, f"{jp_name} (色違い)", shiny_path, True):
                    success_count += 1
        
        print(f"\n✅ 失敗フォルム再取得完了: {success_count}/{total_count}個成功")
        return success_count

def main():
    base_path = r"C:\Users\rarur\OneDrive\ドキュメント\GitHub\PokeAkane"
    retriever = FailedFormsRetriever(base_path)
    
    # 失敗したフォルムを再取得
    retriever.retrieve_failed_forms()
    
    print("\n🌟 失敗フォルム再取得完了！")

if __name__ == "__main__":
    main()