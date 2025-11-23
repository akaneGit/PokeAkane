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
    patterns_dir = os.path.abspath("../pokemon_images/patterns")
    os.makedirs(forms_dir, exist_ok=True)
    os.makedirs(patterns_dir, exist_ok=True)
    
    success_count = 0
    fail_count = 0
    
    print("🔄 ガラルヒヒダルマの正しい画像を取得中...")
    print(f"Forms出力ディレクトリ: {forms_dir}")
    print(f"Patterns出力ディレクトリ: {patterns_dir}")
    print("=" * 80)
    
    pokemon_id = 555
    
    # 1. ガラルヒヒダルマ 通常モード (forms フォルダ)
    print("📝 ガラルヒヒダルマ 通常モード (Standard Mode)")
    for is_shiny in [False, True]:
        shiny_suffix = "_shiny" if is_shiny else ""
        shiny_path = "shiny" if is_shiny else "normal"
        
        filename = f"{pokemon_id:03d}_darmanitan-galar{shiny_suffix}.png"
        filepath = os.path.join(forms_dir, filename)
        
        # 正しいURLパターン
        url = f"https://img.pokemondb.net/sprites/home/{shiny_path}/darmanitan-galarian-standard.png"
        
        print(f"🔍 Trying: {url}")
        if download_image(url, filepath):
            success_count += 1
        else:
            fail_count += 1
        print()
        time.sleep(1)
    
    # 2. ガラルヒヒダルマ ダルマモード (patterns フォルダ)
    print("📝 ガラルヒヒダルマ ダルマモード (Zen Mode)")
    for is_shiny in [False, True]:
        shiny_suffix = "_shiny" if is_shiny else ""
        shiny_path = "shiny" if is_shiny else "normal"
        
        filename = f"{pokemon_id:03d}_darmanitan_zen_galar{shiny_suffix}.png"
        filepath = os.path.join(patterns_dir, filename)
        
        # 正しいURLパターン
        url = f"https://img.pokemondb.net/sprites/home/{shiny_path}/darmanitan-galarian-zen.png"
        
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
    print("- forms/555_darmanitan-galar.png (ガラル通常モード)")
    print("- forms/555_darmanitan-galar_shiny.png (ガラル通常モード色違い)")
    print("- patterns/555_darmanitan_zen_galar.png (ガラルダルマモード)")
    print("- patterns/555_darmanitan_zen_galar_shiny.png (ガラルダルマモード色違い)")

if __name__ == "__main__":
    main()