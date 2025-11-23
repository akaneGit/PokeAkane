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
    forms_dir = os.path.abspath("../pokemon_images/forms")
    os.makedirs(forms_dir, exist_ok=True)
    
    success_count = 0
    fail_count = 0
    
    print("🔄 パルデアタウロス コンバット種の画像を取得中...")
    print(f"Forms出力ディレクトリ: {forms_dir}")
    print("=" * 80)
    
    pokemon_id = 128
    
    # パルデアタウロス コンバット種
    print("📝 パルデアタウロス コンバット種")
    for is_shiny in [False, True]:
        shiny_suffix = "_shiny" if is_shiny else ""
        shiny_path = "shiny" if is_shiny else "normal"
        
        filename = f"{pokemon_id:03d}_tauros_combat{shiny_suffix}.png"
        filepath = os.path.join(forms_dir, filename)
        
        # 指定されたURLパターン
        url = f"https://img.pokemondb.net/sprites/home/{shiny_path}/tauros-paldean-combat.png"
        
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
    print("- forms/128_tauros_combat.png (パルデアタウロス コンバット種)")
    print("- forms/128_tauros_combat_shiny.png (パルデアタウロス コンバット種色違い)")

if __name__ == "__main__":
    main()