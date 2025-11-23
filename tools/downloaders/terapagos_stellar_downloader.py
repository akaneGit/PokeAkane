#!/usr/bin/env python3
"""
テラパゴスのステラフォルム画像を取得するスクリプト
"""

import requests
import time
import os
from urllib.parse import urljoin

def download_terapagos_stellar():
    """テラパゴスのステラフォルム画像をダウンロード"""
    
    # 保存ディレクトリ
    patterns_dir = r"C:\Users\rarur\OneDrive\ドキュメント\GitHub\PokeAkane\pokemon_images\patterns"
    
    # ダウンロード対象
    downloads = [
        {
            "url": "https://img.pokemondb.net/sprites/home/normal/terapagos-stellar.png",
            "filename": "1024_terapagos-stellar.png",
            "desc": "テラパゴス ステラフォルム（通常）"
        },
        {
            "url": "https://img.pokemondb.net/sprites/home/shiny/terapagos-stellar.png", 
            "filename": "1024_terapagos-stellar_shiny.png",
            "desc": "テラパゴス ステラフォルム（色違い）"
        }
    ]
    
    print(f"🔄 テラパゴス ステラフォルム画像ダウンロード開始")
    
    success_count = 0
    
    for download_info in downloads:
        url = download_info["url"]
        filename = download_info["filename"] 
        desc = download_info["desc"]
        filepath = os.path.join(patterns_dir, filename)
        
        print(f"\nダウンロード中: {desc}")
        print(f"URL: {url}")
        
        try:
            # ヘッダーを設定
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                # ファイルを保存
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                print(f"✅ 成功: {filepath}")
                success_count += 1
                
            else:
                print(f"❌ 失敗: HTTP {response.status_code} - {url}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ エラー: {e} - {url}")
        
        time.sleep(1)  # 1秒待機
    
    print(f"\n✅ テラパゴス ステラフォルム取得完了: {success_count}/2個成功")
    return success_count

if __name__ == "__main__":
    download_terapagos_stellar()
    print("\n🌟 テラパゴス ステラフォルム取得完了！")