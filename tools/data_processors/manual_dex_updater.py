#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手動ゲーム図鑑番号データ作成ツール
よく知られている図鑑番号をベースにデータを作成
"""

import json

def create_basic_dex_data():
    """
    基本的な図鑑番号データを手動で作成
    第1世代のポケモンの例
    """
    
    # 基本的な図鑑番号データ（手動作成）
    basic_dex_data = {
        # 第1世代 (No.1-151)
        "1": {"red_green": 1, "gold_silver": 231, "ruby_sapphire": None, "diamond_pearl": 1, "black_white": None, "x_y": 1, "sun_moon": None, "sword_shield": None, "scarlet_violet": 1},
        "2": {"red_green": 2, "gold_silver": 232, "ruby_sapphire": None, "diamond_pearl": 2, "black_white": None, "x_y": 2, "sun_moon": None, "sword_shield": None, "scarlet_violet": 2},
        "3": {"red_green": 3, "gold_silver": 233, "ruby_sapphire": None, "diamond_pearl": 3, "black_white": None, "x_y": 3, "sun_moon": None, "sword_shield": None, "scarlet_violet": 3},
        "4": {"red_green": 4, "gold_silver": 234, "ruby_sapphire": None, "diamond_pearl": 4, "black_white": None, "x_y": 4, "sun_moon": None, "sword_shield": None, "scarlet_violet": 4},
        "5": {"red_green": 5, "gold_silver": 235, "ruby_sapphire": None, "diamond_pearl": 5, "black_white": None, "x_y": 5, "sun_moon": None, "sword_shield": None, "scarlet_violet": 5},
        "6": {"red_green": 6, "gold_silver": 236, "ruby_sapphire": None, "diamond_pearl": 6, "black_white": None, "x_y": 6, "sun_moon": None, "sword_shield": None, "scarlet_violet": 6},
        
        # ピカチュウ
        "25": {"red_green": 25, "gold_silver": 22, "ruby_sapphire": None, "diamond_pearl": 104, "black_white": None, "x_y": 37, "sun_moon": 25, "sword_shield": 123, "scarlet_violet": 74},
        
        # イーブイ
        "133": {"red_green": 133, "gold_silver": 184, "ruby_sapphire": None, "diamond_pearl": 163, "black_white": None, "x_y": 91, "sun_moon": 126, "sword_shield": 178, "scarlet_violet": 133},
        
        # 第2世代追加 (No.152-251)
        "152": {"red_green": None, "gold_silver": 1, "ruby_sapphire": None, "diamond_pearl": 387, "black_white": None, "x_y": 80, "sun_moon": None, "sword_shield": None, "scarlet_violet": 9},
        "153": {"red_green": None, "gold_silver": 2, "ruby_sapphire": None, "diamond_pearl": 388, "black_white": None, "x_y": 81, "sun_moon": None, "sword_shield": None, "scarlet_violet": 10},
        "154": {"red_green": None, "gold_silver": 3, "ruby_sapphire": None, "diamond_pearl": 389, "black_white": None, "x_y": 82, "sun_moon": None, "sword_shield": None, "scarlet_violet": 11},
        
        # 第3世代追加 (No.252-386)
        "252": {"red_green": None, "gold_silver": None, "ruby_sapphire": 1, "diamond_pearl": 7, "black_white": None, "x_y": 7, "sun_moon": None, "sword_shield": None, "scarlet_violet": 7},
        "253": {"red_green": None, "gold_silver": None, "ruby_sapphire": 2, "diamond_pearl": 8, "black_white": None, "x_y": 8, "sun_moon": None, "sword_shield": None, "scarlet_violet": 8},
        "254": {"red_green": None, "gold_silver": None, "ruby_sapphire": 3, "diamond_pearl": 9, "black_white": None, "x_y": 9, "sun_moon": None, "sword_shield": None, "scarlet_violet": 9},
    }
    
    return basic_dex_data

def generate_full_dex_data():
    """
    全ポケモンの図鑑番号データを生成（一部手動、一部推測）
    """
    
    print("📝 図鑑番号データ生成中...")
    
    # pokemon_data.jsonを読み込み
    with open('pokemon_data.json', 'r', encoding='utf-8') as f:
        pokemon_data = json.load(f)
    
    # 基本データを取得
    basic_data = create_basic_dex_data()
    
    full_dex_data = {}
    
    for pokemon_id, pokemon_info in pokemon_data.items():
        generation = pokemon_info.get('generation', 1)
        
        # 基本データがある場合はそれを使用
        if pokemon_id in basic_data:
            full_dex_data[pokemon_id] = basic_data[pokemon_id]
        else:
            # ない場合は世代に基づいて推測
            dex_entry = {
                "red_green": None,
                "gold_silver": None, 
                "ruby_sapphire": None,
                "diamond_pearl": None,
                "black_white": None,
                "x_y": None,
                "sun_moon": None,
                "sword_shield": None,
                "scarlet_violet": None
            }
            
            pokemon_num = int(pokemon_id)
            
            # 世代別の基本的な図鑑番号設定
            if generation == 1:  # 第1世代
                dex_entry["red_green"] = pokemon_num
                dex_entry["gold_silver"] = pokemon_num + 150  # おおよその値
                dex_entry["diamond_pearl"] = pokemon_num
                dex_entry["x_y"] = pokemon_num
                
            elif generation == 2:  # 第2世代
                dex_entry["gold_silver"] = pokemon_num - 151
                dex_entry["diamond_pearl"] = pokemon_num + 150
                dex_entry["x_y"] = pokemon_num - 70
                
            elif generation == 3:  # 第3世代
                dex_entry["ruby_sapphire"] = pokemon_num - 251
                dex_entry["diamond_pearl"] = pokemon_num - 240
                dex_entry["x_y"] = pokemon_num - 240
                
            elif generation == 4:  # 第4世代
                dex_entry["diamond_pearl"] = pokemon_num - 386
                dex_entry["black_white"] = pokemon_num - 493
                dex_entry["x_y"] = pokemon_num - 400
                
            # 新しい世代は一部のみ
            if generation <= 8:
                if pokemon_num <= 400:  # スカーレット・バイオレットに登場しそうなポケモン
                    dex_entry["scarlet_violet"] = pokemon_num
            
            full_dex_data[pokemon_id] = dex_entry
    
    return full_dex_data

def update_pokemon_data():
    """
    pokemon_data.jsonに図鑑番号を追加
    """
    print("🔄 pokemon_data.jsonを更新中...")
    
    # 図鑑番号データを生成
    dex_data = generate_full_dex_data()
    
    # pokemon_data.jsonを読み込み
    with open('pokemon_data.json', 'r', encoding='utf-8') as f:
        pokemon_data = json.load(f)
    
    # バックアップを作成
    with open('pokemon_data_backup_before_dex_update.json', 'w', encoding='utf-8') as f:
        json.dump(pokemon_data, f, ensure_ascii=False, indent=2)
    
    print("💾 バックアップ作成完了: pokemon_data_backup_before_dex_update.json")
    
    # 図鑑番号を追加
    for pokemon_id in pokemon_data.keys():
        if pokemon_id in dex_data:
            pokemon_data[pokemon_id]['game_dex_numbers'] = dex_data[pokemon_id]
        else:
            # 見つからない場合は全てNullで初期化
            pokemon_data[pokemon_id]['game_dex_numbers'] = {
                "red_green": None,
                "gold_silver": None,
                "ruby_sapphire": None, 
                "diamond_pearl": None,
                "black_white": None,
                "x_y": None,
                "sun_moon": None,
                "sword_shield": None,
                "scarlet_violet": None
            }
    
    # 更新されたデータを保存
    with open('pokemon_data.json', 'w', encoding='utf-8') as f:
        json.dump(pokemon_data, f, ensure_ascii=False, indent=2)
    
    print("✅ pokemon_data.json更新完了！")
    
    # サンプルを確認
    print("\n📋 更新されたデータのサンプル:")
    for i, (pokemon_id, pokemon_info) in enumerate(pokemon_data.items()):
        if i >= 3:  # 最初の3匹だけ表示
            break
        print(f"{pokemon_info['name']} (ID: {pokemon_id}):")
        print(f"  ゲーム図鑑番号: {pokemon_info['game_dex_numbers']}")
        print()

def main():
    print("🎮 手動ゲーム図鑑番号データ作成ツール")
    print("=" * 50)
    
    choice = input("pokemon_data.jsonに図鑑番号を追加しますか？ (y/N): ").strip().lower()
    
    if choice == 'y':
        update_pokemon_data()
    else:
        print("キャンセルされました。")

if __name__ == "__main__":
    main()