#!/usr/bin/env python3
"""
ナカヌチャン（958番）の色違い画像を取得するスクリプト
"""

import requests
import time
import os
from urllib.parse import urljoin

def download_nakanuchan_shiny():
    """ナカヌチャン（958番）の色違い画像をPokemonDBから取得"""
    
    # 保存ディレクトリ
    save_dir = r"C:\Users\rarur\OneDrive\ドキュメント\GitHub\PokeAkane\pokemon_images\shinies"
    
    # ナカヌチャンの情報
    pokemon_id = 958
    pokemon_name = "tinkatuff"  # 英語名
    
    # PokemonDBのURL
    base_url = "https://img.pokemondb.net/sprites/home/shiny/"
    file_name = f"{pokemon_name}.png"
    image_url = urljoin(base_url, file_name)
    
    print(f"ナカヌチャン (ID: {pokemon_id}) の色違い画像をダウンロード中...")
    print(f"URL: {image_url}")
    
    try:
        # ヘッダーを設定
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(image_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            # 保存ファイル名
            save_path = os.path.join(save_dir, f"{pokemon_id:03d}_shiny.png")
            
            # ファイルを保存
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ 成功: {save_path}")
            
        else:
            print(f"❌ 失敗: HTTP {response.status_code} - {image_url}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ エラー: {e} - {image_url}")
    
    time.sleep(1)  # 1秒待機

if __name__ == "__main__":
    download_nakanuchan_shiny()
    print("\nナカヌチャンの色違い画像取得完了！")