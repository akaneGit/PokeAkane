#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
進化データ修正スクリプト
PokeAPIから正しい分岐進化データを取得して修正する
"""

import json
import requests
import time
from typing import Dict, List, Optional, Any

def get_evolution_chain_data(chain_id: int) -> Optional[Dict]:
    """進化チェーンデータを取得"""
    try:
        url = f"https://pokeapi.co/api/v2/evolution-chain/{chain_id}/"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"進化チェーン {chain_id} の取得に失敗: {e}")
        return None

def extract_pokemon_id_from_url(url: str) -> int:
    """URLからポケモンIDを抽出"""
    return int(url.strip('/').split('/')[-1])

def parse_evolution_chain(chain_data: Dict) -> Dict[int, Dict]:
    """進化チェーンデータを解析して各ポケモンの進化情報を抽出"""
    evolution_map = {}
    
    def process_chain_node(node: Dict, prev_id: Optional[int] = None):
        # 現在のポケモンのIDを取得
        current_id = extract_pokemon_id_from_url(node['species']['url'])
        
        # 進化先のIDリストを取得
        next_ids = []
        for evolution in node.get('evolves_to', []):
            next_id = extract_pokemon_id_from_url(evolution['species']['url'])
            next_ids.append(next_id)
        
        # 進化情報を記録
        evolution_map[current_id] = {
            'prev': prev_id,
            'next': next_ids
        }
        
        # 進化先も再帰的に処理
        for evolution in node.get('evolves_to', []):
            process_chain_node(evolution, current_id)
    
    # ルートノードから処理開始
    process_chain_node(chain_data['chain'])
    return evolution_map

def main():
    print("進化データ修正を開始...")
    
    # 既存のポケモンデータを読み込み
    with open('pokemon_data.json', 'r', encoding='utf-8') as f:
        pokemon_data = json.load(f)
    
    print(f"ポケモンデータ読み込み完了: {len(pokemon_data)}匹")
    
    # 全進化チェーンを取得（1-600くらいまである）
    all_evolution_data = {}
    
    # 主要な分岐進化を含む進化チェーンを追加
    known_chains = [
        67,   # イーブイファミリー
        42,   # ニョロモファミリー  
        35,   # クサイハナファミリー
        31,   # ピチューファミリー（ピカチュウ）
        32,   # クレッフィファミリー
        41,   # ヒトデマンファミリー
        50,   # ヤドンファミリー
        80,   # コダックファミリー
        # 他の主要な分岐進化チェーンを追加
        20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
        33, 34, 36, 37, 38, 39, 40, 43, 44, 45, 46, 47, 48, 49,
        51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66,
        68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79,
        81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100
    ]
    
    for chain_id in known_chains:
        print(f"進化チェーン {chain_id} を処理中...")
        chain_data = get_evolution_chain_data(chain_id)
        if chain_data:
            evolution_map = parse_evolution_chain(chain_data)
            all_evolution_data.update(evolution_map)
            print(f"  {len(evolution_map)}匹の進化データを取得")
        time.sleep(0.1)  # API制限対策
    
    # ポケモンデータを更新
    updated_count = 0
    for pokemon_id, evolution_info in all_evolution_data.items():
        pokemon_id_str = str(pokemon_id)
        if pokemon_id_str in pokemon_data:
            # 既存の進化データを更新
            pokemon_data[pokemon_id_str]['evolution'] = evolution_info
            updated_count += 1
            print(f"ID {pokemon_id}: {pokemon_data[pokemon_id_str]['name']} の進化データを更新")
    
    print(f"\n{updated_count}匹の進化データを更新しました")
    
    # 特殊ケースの手動修正
    print("\n=== 特殊ケースの手動修正 ===")
    
    # クサイハナ系統の修正 (43: ナゾノクサ → 44: クサイハナ → 45: ラフレシア & 182: キレイハナ)
    if '43' in pokemon_data and '44' in pokemon_data and '45' in pokemon_data and '182' in pokemon_data:
        # ナゾノクサ: 進化前 → クサイハナ
        pokemon_data['43']['evolution'] = {'prev': None, 'next': [44]}
        # クサイハナ: 中間進化（分岐） → ラフレシア & キレイハナ
        pokemon_data['44']['evolution'] = {'prev': 43, 'next': [45, 182]}
        # ラフレシア: 最終進化
        pokemon_data['45']['evolution'] = {'prev': 44, 'next': []}
        # キレイハナ: 最終進化
        pokemon_data['182']['evolution'] = {'prev': 44, 'next': []}
        print("クサイハナ系統の分岐進化を修正: ナゾノクサ → クサイハナ → ラフレシア & キレイハナ")
    
    # コイル系統の修正 (81: コイル → 82: レアコイル → 462: ジバコイル)
    if '81' in pokemon_data and '82' in pokemon_data and '462' in pokemon_data:
        # コイル: 進化前 → レアコイル
        pokemon_data['81']['evolution'] = {'prev': None, 'next': [82]}
        # レアコイル: 中間進化 → ジバコイル
        pokemon_data['82']['evolution'] = {'prev': 81, 'next': [462]}
        # ジバコイル: 最終進化
        pokemon_data['462']['evolution'] = {'prev': 82, 'next': []}
        print("コイル系統の進化を修正: コイル → レアコイル → ジバコイル")
    
    # キルリア系統の修正 (280: ラルトス → 281: キルリア → 282: サーナイト & 475: エルレイド)
    if '280' in pokemon_data and '281' in pokemon_data and '282' in pokemon_data and '475' in pokemon_data:
        # ラルトス: 進化前 → キルリア
        pokemon_data['280']['evolution'] = {'prev': None, 'next': [281]}
        # キルリア: 中間進化（分岐） → サーナイト & エルレイド
        pokemon_data['281']['evolution'] = {'prev': 280, 'next': [282, 475]}
        # サーナイト: 最終進化
        pokemon_data['282']['evolution'] = {'prev': 281, 'next': []}
        # エルレイド: 最終進化
        pokemon_data['475']['evolution'] = {'prev': 281, 'next': []}
        print("キルリア系統の分岐進化を修正: ラルトス → キルリア → サーナイト & エルレイド")
    
    # ユキワラシ系統の修正 (361: ユキワラシ → 362: オニゴーリ & 478: ユキメノコ)
    if '361' in pokemon_data and '362' in pokemon_data and '478' in pokemon_data:
        # ユキワラシ: 分岐進化 → オニゴーリ & ユキメノコ
        pokemon_data['361']['evolution'] = {'prev': None, 'next': [362, 478]}
        # オニゴーリ: 最終進化
        pokemon_data['362']['evolution'] = {'prev': 361, 'next': []}
        # ユキメノコ: 最終進化
        pokemon_data['478']['evolution'] = {'prev': 361, 'next': []}
        print("ユキワラシ系統の分岐進化を修正: ユキワラシ → オニゴーリ & ユキメノコ")
    
    # デスマス系統の修正 (562: デスマス → 563: デスカーン & 867: デスバーン)
    if '562' in pokemon_data and '563' in pokemon_data and '867' in pokemon_data:
        # デスマス: 分岐進化 → デスカーン & デスバーン
        pokemon_data['562']['evolution'] = {'prev': None, 'next': [563, 867]}
        # デスカーン: 最終進化
        pokemon_data['563']['evolution'] = {'prev': 562, 'next': []}
        # デスバーン: 最終進化
        pokemon_data['867']['evolution'] = {'prev': 562, 'next': []}
        print("デスマス系統の分岐進化を修正: デスマス → デスカーン & デスバーン")
    
    # コスモウム系統の修正 (789: コスモッグ → 790: コスモウム → 791: ソルガレオ & 792: ルナアーラ)
    if '789' in pokemon_data and '790' in pokemon_data and '791' in pokemon_data and '792' in pokemon_data:
        # コスモッグ: 進化前 → コスモウム
        pokemon_data['789']['evolution'] = {'prev': None, 'next': [790]}
        # コスモウム: 中間進化（分岐） → ソルガレオ & ルナアーラ
        pokemon_data['790']['evolution'] = {'prev': 789, 'next': [791, 792]}
        # ソルガレオ: 最終進化
        pokemon_data['791']['evolution'] = {'prev': 790, 'next': []}
        # ルナアーラ: 最終進化
        pokemon_data['792']['evolution'] = {'prev': 790, 'next': []}
        print("コスモウム系統の分岐進化を修正: コスモッグ → コスモウム → ソルガレオ & ルナアーラ")
    
    # カジッチュ系統の修正 (840: カジッチュ → 841: アップリュー & 842: タルップル & 1011: カミッチュ)
    if '840' in pokemon_data and '841' in pokemon_data and '842' in pokemon_data and '1011' in pokemon_data:
        # カジッチュ: 分岐進化 → アップリュー & タルップル & カミッチュ
        pokemon_data['840']['evolution'] = {'prev': None, 'next': [841, 842, 1011]}
        # アップリュー: 最終進化
        pokemon_data['841']['evolution'] = {'prev': 840, 'next': []}
        # タルップル: 最終進化
        pokemon_data['842']['evolution'] = {'prev': 840, 'next': []}
        # カミッチュ: 最終進化
        pokemon_data['1011']['evolution'] = {'prev': 840, 'next': []}
        print("カジッチュ系統の分岐進化を修正: カジッチュ → アップリュー & タルップル & カミッチュ")
    
    # ケムッソ系統の修正 (265: ケムッソ → 266: カラサリス → 267: アゲハント & 268: マユルド → 269: ドクケイル)
    if all(str(i) in pokemon_data for i in [265, 266, 267, 268, 269]):
        # ケムッソ: 分岐進化 → カラサリス & マユルド
        pokemon_data['265']['evolution'] = {'prev': None, 'next': [266, 268]}
        # カラサリス: 中間進化 → アゲハント
        pokemon_data['266']['evolution'] = {'prev': 265, 'next': [267]}
        # アゲハント: 最終進化
        pokemon_data['267']['evolution'] = {'prev': 266, 'next': []}
        # マユルド: 中間進化 → ドクケイル
        pokemon_data['268']['evolution'] = {'prev': 265, 'next': [269]}
        # ドクケイル: 最終進化
        pokemon_data['269']['evolution'] = {'prev': 268, 'next': []}
        print("ケムッソ系統の分岐進化を修正: ケムッソ → カラサリス → アゲハント & マユルド → ドクケイル")
    
    # ツチニン系統の修正 (290: ツチニン → 291: テッカニン & 292: ヌケニン)
    if '290' in pokemon_data and '291' in pokemon_data and '292' in pokemon_data:
        # ツチニン: 分岐進化 → テッカニン & ヌケニン
        pokemon_data['290']['evolution'] = {'prev': None, 'next': [291, 292]}
        # テッカニン: 最終進化
        pokemon_data['291']['evolution'] = {'prev': 290, 'next': []}
        # ヌケニン: 最終進化
        pokemon_data['292']['evolution'] = {'prev': 290, 'next': []}
        print("ツチニン系統の分岐進化を修正: ツチニン → テッカニン & ヌケニン")
    
    # ニューラ系統の修正 (215: ニューラ → 461: マニューラ → 903: オオニューラ)
    if '215' in pokemon_data and '461' in pokemon_data and '903' in pokemon_data:
        # ニューラ: 進化前 → マニューラ
        pokemon_data['215']['evolution'] = {'prev': None, 'next': [461]}
        # マニューラ: 中間進化 → オオニューラ
        pokemon_data['461']['evolution'] = {'prev': 215, 'next': [903]}
        # オオニューラ: 最終進化
        pokemon_data['903']['evolution'] = {'prev': 461, 'next': []}
        print("ニューラ系統の進化を修正: ニューラ → マニューラ → オオニューラ")
    
    # メルタン系統の修正 (808: メルタン → 809: メルメタル)
    if '808' in pokemon_data and '809' in pokemon_data:
        # メルタン: 進化前 → メルメタル
        pokemon_data['808']['evolution'] = {'prev': None, 'next': [809]}
        # メルメタル: 最終進化
        pokemon_data['809']['evolution'] = {'prev': 808, 'next': []}
        print("メルタン系統の進化を修正: メルタン → メルメタル")
    
    updated_count += 36  # 特殊ケース分を追加
    
    # バックアップと保存
    import shutil
    shutil.copy('pokemon_data.json', 'pokemon_data_backup_before_evolution_fix.json')
    print("バックアップを作成: pokemon_data_backup_before_evolution_fix.json")
    
    with open('pokemon_data.json', 'w', encoding='utf-8') as f:
        json.dump(pokemon_data, f, ensure_ascii=False, indent=2)
    
    print("修正されたデータを保存しました")
    
    # 修正結果を確認
    print("\n修正結果の確認:")
    for pokemon_id in [133, 44, 61]:  # イーブイ、クサイハナ、ニョロゾ
        if str(pokemon_id) in pokemon_data:
            pokemon = pokemon_data[str(pokemon_id)]
            evolution = pokemon.get('evolution', {})
            print(f"ID {pokemon_id}: {pokemon['name']} - {evolution}")

if __name__ == "__main__":
    main()