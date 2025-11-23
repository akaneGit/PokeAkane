#!/usr/bin/env python3
"""
成功したフォルム違いの色違い画像を取得するスクリプト
"""

import requests
import os
import time
from pathlib import Path

class FormShinyDownloader:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.patterns_path = self.base_path / "pokemon_images" / "patterns"
        
        # リクエスト間隔（秒）
        self.delay = 1

    def download_image(self, url, filepath):
        """画像をダウンロードして保存"""
        try:
            print(f"ダウンロード中: {url}")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✅ 保存完了: {filepath}")
            time.sleep(self.delay)
            return True
            
        except Exception as e:
            print(f"❌ エラー: {url} -> {e}")
            return False

    def get_successful_forms(self):
        """成功してダウンロードされたフォルム画像のリストを取得"""
        successful_forms = []
        
        # patternsフォルダ内の画像ファイルをチェック
        for filepath in self.patterns_path.glob("*.png"):
            filename = filepath.name
            if not filename.endswith("_shiny.png"):  # 色違いでない通常フォルム
                # ファイル名から情報を抽出
                parts = filename.replace(".png", "").split("_", 1)
                if len(parts) >= 2:
                    pokemon_id = parts[0]
                    form_name = parts[1]
                    successful_forms.append((pokemon_id, form_name))
        
        return successful_forms

    def download_form_shinies(self):
        """成功したフォルムの色違い画像をダウンロード"""
        print("🔄 成功したフォルムの色違い画像ダウンロード開始")
        
        successful_forms = self.get_successful_forms()
        print(f"ダウンロード対象: {len(successful_forms)}個のフォルム")
        
        success_count = 0
        
        for pokemon_id, form_name in successful_forms:
            # 色違いファイルが既に存在するかチェック
            shiny_filename = f"{pokemon_id}_{form_name}_shiny.png"
            shiny_filepath = self.patterns_path / shiny_filename
            
            if shiny_filepath.exists():
                print(f"⏭️ スキップ (既存): {shiny_filename}")
                continue
                
            # PokemonDBのURL構築
            # form_nameから適切なURL名を作成
            url_form_name = form_name.replace("_", "-")
            shiny_url = f"https://img.pokemondb.net/sprites/home/shiny/{url_form_name}.png"
            
            # ダウンロード実行
            if self.download_image(shiny_url, shiny_filepath):
                success_count += 1
        
        print(f"\n✅ 色違い画像ダウンロード完了: {success_count}個成功")
        return success_count

def main():
    base_path = r"C:\Users\rarur\OneDrive\ドキュメント\GitHub\PokeAkane"
    downloader = FormShinyDownloader(base_path)
    
    # 成功したフォルムの色違いをダウンロード
    downloader.download_form_shinies()
    
    print("\n🌟 全ての色違い画像ダウンロード完了！")

if __name__ == "__main__":
    main()