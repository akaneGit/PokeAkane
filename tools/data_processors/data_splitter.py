#!/usr/bin/env python3
"""
ポケモンデータを世代別に分割するスクリプト

使用方法:
python data_splitter.py

出力:
- gen1_pokemon.json (第1世代: #001-151)
- gen2_pokemon.json (第2世代: #152-251)
- gen3_pokemon.json (第3世代: #252-386)
- gen4_pokemon.json (第4世代: #387-493)
- gen5_pokemon.json (第5世代: #494-649)
- gen6_pokemon.json (第6世代: #650-721)
- gen7_pokemon.json (第7世代: #722-809)
- gen8_pokemon.json (第8世代: #810-905)
- gen9_pokemon.json (第9世代: #906-1025)
"""

import json
import os

def split_pokemon_data():
    """ポケモンデータを世代別に分割"""
    
    # 世代別のID範囲を定義
    generations = {
        'gen1': (1, 151),       # 第1世代: フシギダネ〜ミュウ
        'gen2': (152, 251),     # 第2世代: チコリータ〜セレビィ
        'gen3': (252, 386),     # 第3世代: キモリ〜デオキシス
        'gen4': (387, 493),     # 第4世代: ナエトル〜アルセウス
        'gen5': (494, 649),     # 第5世代: ツタージャ〜ゲノセクト
        'gen6': (650, 721),     # 第6世代: ハリマロン〜ボルケニオン
        'gen7': (722, 809),     # 第7世代: モクロー〜メルメタル
        'gen8': (810, 905),     # 第8世代: サルノリ〜エレザード
        'gen9': (906, 1025)     # 第9世代: ニャオハ〜ペラッパ
    }
    
    # メインデータを読み込み
    print("pokemon_data.jsonを読み込み中...")
    with open('pokemon_data.json', 'r', encoding='utf-8') as f:
        all_pokemon = json.load(f)
    
    print(f"全ポケモン数: {len(all_pokemon)}")
    
    # 世代別に分割
    for gen_name, (start_id, end_id) in generations.items():
        gen_data = {}
        count = 0
        
        # 該当する世代のポケモンを抽出
        for pokemon_id_str, pokemon_data in all_pokemon.items():
            pokemon_id = int(pokemon_id_str)
            if start_id <= pokemon_id <= end_id:
                gen_data[pokemon_id_str] = pokemon_data
                count += 1
        
        # ファイルに保存
        filename = f"{gen_name}_pokemon.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(gen_data, f, ensure_ascii=False, indent=2)
        
        print(f"{gen_name}: {count}匹のポケモンを {filename} に保存")
        print(f"  範囲: #{start_id:03d} - #{end_id:03d}")
        
        # サンプルポケモンを表示
        if gen_data:
            first_pokemon = next(iter(gen_data.values()))
            last_pokemon_id = max(int(k) for k in gen_data.keys())
            last_pokemon = gen_data[str(last_pokemon_id)]
            print(f"  例: {first_pokemon['name']} 〜 {last_pokemon['name']}")
        print()
    
    # 統計情報
    total_split = sum(len(json.load(open(f"{gen}_pokemon.json", 'r', encoding='utf-8'))) 
                     for gen in generations.keys())
    print(f"分割完了!")
    print(f"元データ: {len(all_pokemon)}匹")
    print(f"分割後合計: {total_split}匹")
    print(f"整合性: {'✅ OK' if len(all_pokemon) == total_split else '❌ エラー'}")
    
    # ファイルサイズ比較
    original_size = os.path.getsize('pokemon_data.json')
    split_total_size = sum(os.path.getsize(f"{gen}_pokemon.json") for gen in generations.keys())
    
    print(f"\nファイルサイズ比較:")
    print(f"元ファイル: {original_size:,} bytes ({original_size/1024/1024:.1f} MB)")
    print(f"分割後合計: {split_total_size:,} bytes ({split_total_size/1024/1024:.1f} MB)")
    print(f"個別ファイル平均: {split_total_size/len(generations)/1024:.1f} KB")

if __name__ == "__main__":
    try:
        split_pokemon_data()
        print("\n✅ 世代別データ分割が完了しました！")
    except FileNotFoundError:
        print("❌ pokemon_data.json が見つかりません。")
        print("このスクリプトは pokemon_data.json と同じディレクトリで実行してください。")
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")