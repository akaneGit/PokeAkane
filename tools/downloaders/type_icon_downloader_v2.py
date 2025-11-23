#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改良版タイプアイコンダウンローダー
より高品質なポケモンタイプアイコンを取得
"""

import requests
import os
from PIL import Image, ImageDraw, ImageFont
import io

# タイプ名とより良いURLソースのマッピング
TYPE_SOURCES = {
    'ノーマル': {
        'name': 'normal',
        'urls': [
            'https://raw.githubusercontent.com/duiker101/pokemon-type-svg-icons/master/icons/normal.svg',
            'https://archives.bulbagarden.net/media/upload/9/95/NormalIC_Big.png',
            'https://img.pokemondb.net/images/typedx/normal.png'
        ],
        'color': '#A8A878'
    },
    'ほのお': {
        'name': 'fire',
        'urls': [
            'https://raw.githubusercontent.com/duiker101/pokemon-type-svg-icons/master/icons/fire.svg',
            'https://archives.bulbagarden.net/media/upload/5/56/FireIC_Big.png',
            'https://img.pokemondb.net/images/typedx/fire.png'
        ],
        'color': '#F08030'
    },
    'みず': {
        'name': 'water',
        'urls': [
            'https://raw.githubusercontent.com/duiker101/pokemon-type-svg-icons/master/icons/water.svg',
            'https://archives.bulbagarden.net/media/upload/0/0b/WaterIC_Big.png',
            'https://img.pokemondb.net/images/typedx/water.png'
        ],
        'color': '#6890F0'
    },
    'でんき': {
        'name': 'electric',
        'urls': [
            'https://raw.githubusercontent.com/duiker101/pokemon-type-svg-icons/master/icons/electric.svg',
            'https://archives.bulbagarden.net/media/upload/a/a9/ElectricIC_Big.png',
            'https://img.pokemondb.net/images/typedx/electric.png'
        ],
        'color': '#F8D030'
    },
    'くさ': {
        'name': 'grass',
        'urls': [
            'https://raw.githubusercontent.com/duiker101/pokemon-type-svg-icons/master/icons/grass.svg',
            'https://archives.bulbagarden.net/media/upload/f/f6/GrassIC_Big.png',
            'https://img.pokemondb.net/images/typedx/grass.png'
        ],
        'color': '#78C850'
    },
    'こおり': {
        'name': 'ice',
        'urls': [
            'https://raw.githubusercontent.com/duiker101/pokemon-type-svg-icons/master/icons/ice.svg',
            'https://archives.bulbagarden.net/media/upload/8/88/IceIC_Big.png',
            'https://img.pokemondb.net/images/typedx/ice.png'
        ],
        'color': '#98D8D8'
    },
    'かくとう': {
        'name': 'fighting',
        'urls': [
            'https://raw.githubusercontent.com/duiker101/pokemon-type-svg-icons/master/icons/fighting.svg',
            'https://archives.bulbagarden.net/media/upload/b/be/FightingIC_Big.png',
            'https://img.pokemondb.net/images/typedx/fighting.png'
        ],
        'color': '#C03028'
    },
    'どく': {
        'name': 'poison',
        'urls': [
            'https://raw.githubusercontent.com/duiker101/pokemon-type-svg-icons/master/icons/poison.svg',
            'https://archives.bulbagarden.net/media/upload/c/c4/PoisonIC_Big.png',
            'https://img.pokemondb.net/images/typedx/poison.png'
        ],
        'color': '#A040A0'
    },
    'じめん': {
        'name': 'ground',
        'urls': [
            'https://raw.githubusercontent.com/duiker101/pokemon-type-svg-icons/master/icons/ground.svg',
            'https://archives.bulbagarden.net/media/upload/8/8a/GroundIC_Big.png',
            'https://img.pokemondb.net/images/typedx/ground.png'
        ],
        'color': '#E0C068'
    },
    'ひこう': {
        'name': 'flying',
        'urls': [
            'https://raw.githubusercontent.com/duiker101/pokemon-type-svg-icons/master/icons/flying.svg',
            'https://archives.bulbagarden.net/media/upload/e/e0/FlyingIC_Big.png',
            'https://img.pokemondb.net/images/typedx/flying.png'
        ],
        'color': '#A890F0'
    },
    'エスパー': {
        'name': 'psychic',
        'urls': [
            'https://raw.githubusercontent.com/duiker101/pokemon-type-svg-icons/master/icons/psychic.svg',
            'https://archives.bulbagarden.net/media/upload/a/ab/PsychicIC_Big.png',
            'https://img.pokemondb.net/images/typedx/psychic.png'
        ],
        'color': '#F85888'
    },
    'むし': {
        'name': 'bug',
        'urls': [
            'https://raw.githubusercontent.com/duiker101/pokemon-type-svg-icons/master/icons/bug.svg',
            'https://archives.bulbagarden.net/media/upload/3/3c/BugIC_Big.png',
            'https://img.pokemondb.net/images/typedx/bug.png'
        ],
        'color': '#A8B820'
    },
    'いわ': {
        'name': 'rock',
        'urls': [
            'https://raw.githubusercontent.com/duiker101/pokemon-type-svg-icons/master/icons/rock.svg',
            'https://archives.bulbagarden.net/media/upload/b/bb/RockIC_Big.png',
            'https://img.pokemondb.net/images/typedx/rock.png'
        ],
        'color': '#B8A038'
    },
    'ゴースト': {
        'name': 'ghost',
        'urls': [
            'https://raw.githubusercontent.com/duiker101/pokemon-type-svg-icons/master/icons/ghost.svg',
            'https://archives.bulbagarden.net/media/upload/a/a0/GhostIC_Big.png',
            'https://img.pokemondb.net/images/typedx/ghost.png'
        ],
        'color': '#705898'
    },
    'ドラゴン': {
        'name': 'dragon',
        'urls': [
            'https://raw.githubusercontent.com/duiker101/pokemon-type-svg-icons/master/icons/dragon.svg',
            'https://archives.bulbagarden.net/media/upload/a/a6/DragonIC_Big.png',
            'https://img.pokemondb.net/images/typedx/dragon.png'
        ],
        'color': '#7038F8'
    },
    'あく': {
        'name': 'dark',
        'urls': [
            'https://raw.githubusercontent.com/duiker101/pokemon-type-svg-icons/master/icons/dark.svg',
            'https://archives.bulbagarden.net/media/upload/0/07/DarkIC_Big.png',
            'https://img.pokemondb.net/images/typedx/dark.png'
        ],
        'color': '#705848'
    },
    'はがね': {
        'name': 'steel',
        'urls': [
            'https://raw.githubusercontent.com/duiker101/pokemon-type-svg-icons/master/icons/steel.svg',
            'https://archives.bulbagarden.net/media/upload/3/38/SteelIC_Big.png',
            'https://img.pokemondb.net/images/typedx/steel.png'
        ],
        'color': '#B8B8D0'
    },
    'フェアリー': {
        'name': 'fairy',
        'urls': [
            'https://raw.githubusercontent.com/duiker101/pokemon-type-svg-icons/master/icons/fairy.svg',
            'https://archives.bulbagarden.net/media/upload/0/08/FairyIC_Big.png',
            'https://img.pokemondb.net/images/typedx/fairy.png'
        ],
        'color': '#EE99AC'
    }
}

def download_image(url, filename):
    """URLから画像をダウンロード"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"  ❌ ダウンロードエラー: {e}")
    return False

def create_improved_backup(type_name, color, filename):
    """改良版バックアップアイコン作成"""
    try:
        # より大きなサイズで作成
        size = 64
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # グラデーション効果のための複数の円
        for i in range(5):
            offset = i * 2
            alpha = 200 - i * 30
            color_with_alpha = tuple(int(color[j:j+2], 16) for j in (1, 3, 5)) + (alpha,)
            draw.ellipse([offset, offset, size-offset, size-offset], 
                        fill=color_with_alpha, outline=None)
        
        # 中央に白い円で立体感
        center_size = size // 3
        center_offset = (size - center_size) // 2
        draw.ellipse([center_offset, center_offset, center_offset + center_size, center_offset + center_size],
                    fill=(255, 255, 255, 100))
        
        # フォントサイズを調整
        font_size = max(8, size // 8)
        try:
            # システムフォントを試す
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("meiryo.ttc", font_size)
            except:
                font = ImageFont.load_default()
        
        # テキストを中央に配置
        text_bbox = draw.textbbox((0, 0), type_name[0], font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = (size - text_width) // 2
        text_y = (size - text_height) // 2
        
        # 影付きテキスト
        draw.text((text_x + 1, text_y + 1), type_name[0], fill=(0, 0, 0, 150), font=font)
        draw.text((text_x, text_y), type_name[0], fill=(255, 255, 255, 255), font=font)
        
        img.save(filename)
        return True
    except Exception as e:
        print(f"  ❌ バックアップ作成エラー: {e}")
        return False

def main():
    print("🚀 改良版タイプアイコンダウンローダー起動！")
    
    # ディレクトリ作成
    os.makedirs('type_images', exist_ok=True)
    
    success_count = 0
    total_count = len(TYPE_SOURCES)
    
    for type_name, type_info in TYPE_SOURCES.items():
        print(f"🔄 {type_name}タイプアイコン取得中...")
        
        # 複数のURLソースを試す
        downloaded = False
        for i, url in enumerate(type_info['urls']):
            filename = f"type_images/{type_name}.png"
            print(f"  📥 ソース{i+1}を試行中... {url[:50]}...")
            
            if download_image(url, filename):
                print(f"  ✅ {type_name}タイプ取得成功！")
                success_count += 1
                downloaded = True
                break
            else:
                print(f"  ⚠️ ソース{i+1}失敗")
        
        # ダウンロードに失敗した場合は改良版バックアップを作成
        if not downloaded:
            print(f"  🔧 {type_name}タイプ用改良版バックアップ作成中...")
            backup_filename = f"type_images/{type_name}_backup.png"
            if create_improved_backup(type_name, type_info['color'], backup_filename):
                print(f"  ✅ {type_name}バックアップ作成成功")
    
    print(f"\n🎉 タイプアイコン取得完了！ {success_count}/{total_count}")
    
    # 現在のファイル状況を確認
    print("\n📂 取得済みファイル:")
    for type_name in TYPE_SOURCES.keys():
        regular_file = f"type_images/{type_name}.png"
        backup_file = f"type_images/{type_name}_backup.png"
        
        if os.path.exists(regular_file):
            print(f"  ✅ {type_name}.png (メイン)")
        elif os.path.exists(backup_file):
            print(f"  🔧 {type_name}_backup.png (バックアップ)")
        else:
            print(f"  ❌ {type_name} ファイルなし")
    
    print("\n✨ 改良版タイプアイコン準備完了！")

if __name__ == "__main__":
    main()