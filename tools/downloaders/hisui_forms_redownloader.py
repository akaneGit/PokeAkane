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
    # ヒスイフォームのポケモンリスト
    hisui_pokemon = [
        # ID, Pokemon名, フォーム名
        (58, "growlithe", "hisui"),
        (59, "arcanine", "hisui"),
        (100, "voltorb", "hisui"),
        (101, "electrode", "hisui"),
        (157, "typhlosion", "hisui"),
        (211, "qwilfish", "hisui"),
        (215, "sneasel", "hisui"),
        (503, "samurott", "hisui"),
        (549, "lilligant", "hisui"),
        (570, "zorua", "hisui"),
        (571, "zoroark", "hisui"),
        (628, "braviary", "hisui"),
        (705, "sliggoo", "hisui"),
        (706, "goodra", "hisui"),
        (713, "avalugg", "hisui"),
        (724, "decidueye", "hisui"),
    ]
    
    # 出力ディレクトリ
    output_dir = os.path.abspath("../pokemon_images/forms")
    os.makedirs(output_dir, exist_ok=True)
    
    success_count = 0
    fail_count = 0
    
    print("🔄 ヒスイフォームポケモンの画像を取得中...")
    print(f"出力ディレクトリ: {output_dir}")
    print("=" * 80)
    
    for pokemon_id, pokemon_name, form_name in hisui_pokemon:
        # 通常版とシャイニー版の両方をダウンロード
        for is_shiny in [False, True]:
            shiny_suffix = "_shiny" if is_shiny else ""
            shiny_path = "shiny" if is_shiny else "normal"
            
            # ファイル名を生成
            filename = f"{pokemon_id:03d}_{pokemon_name}-{form_name}{shiny_suffix}.png"
            filepath = os.path.join(output_dir, filename)
            
            # PokemonDBのURL候補を生成
            url_patterns = [
                f"https://img.pokemondb.net/sprites/home/{shiny_path}/{pokemon_name}-{form_name}.png",
                f"https://img.pokemondb.net/sprites/home/{shiny_path}/hisuian-{pokemon_name}.png",
                f"https://img.pokemondb.net/sprites/home/{shiny_path}/{pokemon_name}-hisuian.png",
            ]
            
            downloaded = False
            for url in url_patterns:
                print(f"🔍 Trying: {url}")
                if download_image(url, filepath):
                    downloaded = True
                    success_count += 1
                    break
                time.sleep(1)  # APIレート制限対策
            
            if not downloaded:
                print(f"❌ All URLs failed for: {filename}")
                fail_count += 1
            
            print()  # 空行
    
    print("=" * 80)
    print(f"🎉 完了！ 成功: {success_count}, 失敗: {fail_count}")
    
    if fail_count > 0:
        print("\n⚠️ 失敗したファイルについて、手動でURLを確認することをお勧めします。")

if __name__ == "__main__":
    main()