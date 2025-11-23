#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
import time
from urllib.parse import urlparse

def download_image(url, filepath):
    """画像をダウンロードする"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"✅ Downloaded: {os.path.basename(filepath)}")
        return True
    except Exception as e:
        print(f"❌ Failed to download {os.path.basename(filepath)}: {e}")
        return False

def main():
    # 出力ディレクトリ
    patterns_dir = os.path.abspath("../pokemon_images/patterns")
    os.makedirs(patterns_dir, exist_ok=True)
    
    success_count = 0
    fail_count = 0
    
    print("🔄 通常ヒヒダルマのダルマモード画像を取り直し中...")
    print(f"Patterns出力ディレクトリ: {patterns_dir}")
    print("=" * 80)
    
    pokemon_id = 555
    
    # 通常ヒヒダルマ ダルマモード
    print("📝 通常ヒヒダルマ ダルマモード")
    for is_shiny in [False, True]:
        shiny_suffix = "_shiny" if is_shiny else ""
        shiny_path = "shiny" if is_shiny else "normal"
        
        filename = f"{pokemon_id:03d}_darmanitan-zen{shiny_suffix}.png"
        filepath = os.path.join(patterns_dir, filename)
        
        # 指定されたURLパターン
        url = f"https://img.pokemondb.net/sprites/home/{shiny_path}/darmanitan-zen.png"
        
        print(f"🔍 Trying: {url}")
        if download_image(url, filepath):
            success_count += 1
        else:
            fail_count += 1
        print()
        time.sleep(1)
    
    print("=" * 80)
    print(f"🎉 完了！ 成功: {success_count}, 失敗: {fail_count}")
    
    print("\n📋 取得ファイル:")
    print("- patterns/555_darmanitan-zen.png (通常ダルマモード)")
    print("- patterns/555_darmanitan-zen_shiny.png (通常ダルマモード色違い)")

if __name__ == "__main__":
    main()