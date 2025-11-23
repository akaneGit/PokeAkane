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
    output_dir = os.path.abspath("../pokemon_images/forms")
    patterns_dir = os.path.abspath("../pokemon_images/patterns")
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(patterns_dir, exist_ok=True)
    
    success_count = 0
    fail_count = 0
    
    print("🔄 ガラルヒヒダルマ（通常モード・ダルマモード）の画像を取得中...")
    print(f"Forms出力ディレクトリ: {output_dir}")
    print(f"Patterns出力ディレクトリ: {patterns_dir}")
    print("=" * 80)
    
    pokemon_id = 555
    pokemon_name = "darmanitan"
    
    # 1. ガラルヒヒダルマ 通常モード (forms フォルダ)
    print("📝 ガラルヒヒダルマ 通常モード")
    for is_shiny in [False, True]:
        shiny_suffix = "_shiny" if is_shiny else ""
        shiny_path = "shiny" if is_shiny else "normal"
        
        filename = f"{pokemon_id:03d}_{pokemon_name}-galar{shiny_suffix}.png"
        filepath = os.path.join(output_dir, filename)
        
        url_patterns = [
            f"https://img.pokemondb.net/sprites/home/{shiny_path}/galarian-{pokemon_name}.png",
            f"https://img.pokemondb.net/sprites/home/{shiny_path}/{pokemon_name}-galarian.png",
            f"https://img.pokemondb.net/sprites/home/{shiny_path}/{pokemon_name}-galar.png",
            f"https://img.pokemondb.net/sprites/home/{shiny_path}/{pokemon_name}-galar-standard.png",
        ]
        
        downloaded = False
        for url in url_patterns:
            print(f"🔍 Trying: {url}")
            if download_image(url, filepath):
                downloaded = True
                success_count += 1
                break
            time.sleep(1)
        
        if not downloaded:
            print(f"❌ All URLs failed for: {filename}")
            fail_count += 1
        print()
    
    # 2. ガラルヒヒダルマ ダルマモード (patterns フォルダ)
    print("📝 ガラルヒヒダルマ ダルマモード")
    for is_shiny in [False, True]:
        shiny_suffix = "_shiny" if is_shiny else ""
        shiny_path = "shiny" if is_shiny else "normal"
        
        filename = f"{pokemon_id:03d}_{pokemon_name}_zen_galar{shiny_suffix}.png"
        filepath = os.path.join(patterns_dir, filename)
        
        url_patterns = [
            f"https://img.pokemondb.net/sprites/home/{shiny_path}/{pokemon_name}-zen-galar.png",
            f"https://img.pokemondb.net/sprites/home/{shiny_path}/galarian-{pokemon_name}-zen.png",
            f"https://img.pokemondb.net/sprites/home/{shiny_path}/{pokemon_name}-zen-galarian.png",
            f"https://img.pokemondb.net/sprites/home/{shiny_path}/{pokemon_name}-galar-zen.png",
            f"https://img.pokemondb.net/sprites/home/{shiny_path}/{pokemon_name}-zen.png",
        ]
        
        downloaded = False
        for url in url_patterns:
            print(f"🔍 Trying: {url}")
            if download_image(url, filepath):
                downloaded = True
                success_count += 1
                break
            time.sleep(1)
        
        if not downloaded:
            print(f"❌ All URLs failed for: {filename}")
            fail_count += 1
        print()
    
    # 3. 通常のヒヒダルマ ダルマモード (比較用)
    print("📝 通常のヒヒダルマ ダルマモード（比較用）")
    for is_shiny in [False, True]:
        shiny_suffix = "_shiny" if is_shiny else ""
        shiny_path = "shiny" if is_shiny else "normal"
        
        filename = f"{pokemon_id:03d}_{pokemon_name}_zen{shiny_suffix}.png"
        filepath = os.path.join(patterns_dir, filename)
        
        url_patterns = [
            f"https://img.pokemondb.net/sprites/home/{shiny_path}/{pokemon_name}-zen.png",
            f"https://img.pokemondb.net/sprites/home/{shiny_path}/{pokemon_name}-daruma.png",
        ]
        
        downloaded = False
        for url in url_patterns:
            print(f"🔍 Trying: {url}")
            if download_image(url, filepath):
                downloaded = True
                success_count += 1
                break
            time.sleep(1)
        
        if not downloaded:
            print(f"❌ All URLs failed for: {filename}")
            fail_count += 1
        print()
    
    print("=" * 80)
    print(f"🎉 完了！ 成功: {success_count}, 失敗: {fail_count}")
    
    if fail_count > 0:
        print("\n⚠️ 失敗したファイルについて、手動でURLを確認することをお勧めします。")
    
    print("\n📋 取得予定ファイル:")
    print("- forms/555_darmanitan-galar.png (ガラル通常モード)")
    print("- forms/555_darmanitan-galar_shiny.png (ガラル通常モード色違い)")
    print("- patterns/555_darmanitan_zen_galar.png (ガラルダルマモード)")
    print("- patterns/555_darmanitan_zen_galar_shiny.png (ガラルダルマモード色違い)")
    print("- patterns/555_darmanitan_zen.png (通常ダルマモード)")
    print("- patterns/555_darmanitan_zen_shiny.png (通常ダルマモード色違い)")

if __name__ == "__main__":
    main()