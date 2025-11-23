#!/usr/bin/env python3
"""
テラパゴスとモモワロウの色違い画像を正しいものと比較確認するスクリプト
"""

import requests
import os
from PIL import Image
import hashlib

def get_file_hash(filepath):
    """ファイルのSHA256ハッシュを取得"""
    with open(filepath, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def download_and_compare():
    """正しい画像をダウンロードして現在のファイルと比較"""
    
    # 保存ディレクトリ
    shinies_dir = r"C:\Users\rarur\OneDrive\ドキュメント\GitHub\PokeAkane\pokemon_images\shinies"
    
    # テスト用ディレクトリ
    test_dir = r"C:\Users\rarur\OneDrive\ドキュメント\GitHub\PokeAkane\tools\temp_test"
    os.makedirs(test_dir, exist_ok=True)
    
    # ダウンロード対象
    pokemon_data = [
        {"id": 1024, "name": "terapagos", "jp_name": "テラパゴス"},
        {"id": 1025, "name": "pecharunt", "jp_name": "モモワロウ"}
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for pokemon in pokemon_data:
        print(f"\n=== {pokemon['jp_name']} (ID: {pokemon['id']}) ===")
        
        # PokemonDBから正しい画像をダウンロード
        url = f"https://img.pokemondb.net/sprites/home/shiny/{pokemon['name']}.png"
        test_path = os.path.join(test_dir, f"correct_{pokemon['id']}_shiny.png")
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                with open(test_path, 'wb') as f:
                    f.write(response.content)
                print(f"✅ 正しい画像をダウンロード: {test_path}")
                
                # 現在のファイルと比較
                current_path = os.path.join(shinies_dir, f"{pokemon['id']:03d}_shiny.png")
                
                if os.path.exists(current_path):
                    current_hash = get_file_hash(current_path)
                    correct_hash = get_file_hash(test_path)
                    
                    print(f"現在のファイル: {current_path}")
                    print(f"現在のハッシュ: {current_hash[:16]}...")
                    print(f"正しいハッシュ: {correct_hash[:16]}...")
                    
                    if current_hash == correct_hash:
                        print(f"✅ 画像は正しい")
                    else:
                        print(f"❌ 画像が間違っている！")
                        
                        # 画像サイズも確認
                        try:
                            current_img = Image.open(current_path)
                            correct_img = Image.open(test_path)
                            print(f"現在のサイズ: {current_img.size}")
                            print(f"正しいサイズ: {correct_img.size}")
                        except Exception as e:
                            print(f"画像サイズ確認エラー: {e}")
                else:
                    print(f"❌ 現在のファイルが存在しない: {current_path}")
                    
            else:
                print(f"❌ ダウンロード失敗: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ エラー: {e}")

if __name__ == "__main__":
    download_and_compare()
    print("\n比較完了！")