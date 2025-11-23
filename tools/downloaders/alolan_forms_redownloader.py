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
    # アローラフォームのポケモンリスト
    alolan_pokemon = [
        # ID, Pokemon名, フォーム名
        (19, "rattata", "alola"),
        (20, "raticate", "alola"),
        (26, "raichu", "alola"),
        (27, "sandshrew", "alola"),
        (28, "sandslash", "alola"),
        (37, "vulpix", "alola"),
        (38, "ninetales", "alola"),
        (50, "diglett", "alola"),
        (51, "dugtrio", "alola"),
        (52, "meowth", "alola"),
        (53, "persian", "alola"),
        (74, "geodude", "alola"),
        (75, "graveler", "alola"),
        (76, "golem", "alola"),
        (88, "grimer", "alola"),
        (89, "muk", "alola"),
        (103, "exeggutor", "alola"),
        (105, "marowak", "alola"),
    ]
    
    # 出力ディレクトリ
    output_dir = os.path.abspath("../pokemon_images/forms")
    os.makedirs(output_dir, exist_ok=True)
    
    success_count = 0
    fail_count = 0
    
    print("🔄 アローラフォームポケモンの画像を取得中...")
    print(f"出力ディレクトリ: {output_dir}")
    print("=" * 80)
    
    for pokemon_id, pokemon_name, form_name in alolan_pokemon:
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
                f"https://img.pokemondb.net/sprites/home/{shiny_path}/alolan-{pokemon_name}.png",
                f"https://img.pokemondb.net/sprites/home/{shiny_path}/{pokemon_name}-alolan.png",
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