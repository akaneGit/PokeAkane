#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ゲームタイトル別図鑑番号取得・更新ツール
各ポケモンデータに各ゲームタイトルの図鑑番号を追加する
"""

import json
import requests
import time
from bs4 import BeautifulSoup
import re

class GameDexNumberUpdater:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # 対象ゲームタイトル（yakkun.comで使用されている名前）
        self.game_titles = {
            'red_green': '赤・緑',
            'gold_silver': '金・銀',
            'ruby_sapphire': 'ルビー・サファイア', 
            'diamond_pearl': 'ダイヤモンド・パール',
            'black_white': 'ブラック・ホワイト',
            'x_y': 'X・Y',
            'sun_moon': 'サン・ムーン',
            'sword_shield': 'ソード・シールド',
            'scarlet_violet': 'スカーレット・バイオレット'
        }
    
    def get_pokemon_dex_numbers(self, pokemon_id, pokemon_name):
        """
        指定されたポケモンの各ゲームタイトルでの図鑑番号を取得
        """
        print(f"🔍 {pokemon_name} (ID: {pokemon_id}) の図鑑番号を取得中...")
        
        try:
            # yakkun.comのポケモン詳細ページにアクセス
            url = f"https://yakkun.com/sv/zukan/n{pokemon_id}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 図鑑番号情報を格納する辞書
            dex_numbers = {}
            
            # 各ゲームタイトルの図鑑番号を初期化（nullで）
            for game_key in self.game_titles.keys():
                dex_numbers[game_key] = None
            
            # 図鑑番号の表を探す
            # yakkun.comの構造に応じて調整が必要
            dex_table = soup.find('table', class_='zukan_table')
            if dex_table:
                rows = dex_table.find_all('tr')
                for row in rows:
                    cols = row.find_all(['td', 'th'])
                    if len(cols) >= 2:
                        game_name = cols[0].get_text(strip=True)
                        dex_num_text = cols[1].get_text(strip=True)
                        
                        # 数字のみ抽出
                        dex_num_match = re.search(r'\d+', dex_num_text)
                        if dex_num_match:
                            dex_num = int(dex_num_match.group())
                            
                            # ゲーム名をキーにマッピング
                            for game_key, game_title in self.game_titles.items():
                                if game_title in game_name or game_name in game_title:
                                    dex_numbers[game_key] = dex_num
                                    break
            
            print(f"✅ {pokemon_name} の図鑑番号取得完了")
            return dex_numbers
            
        except Exception as e:
            print(f"❌ {pokemon_name} の図鑑番号取得に失敗: {e}")
            # エラーの場合は全てNullで返す
            return {game_key: None for game_key in self.game_titles.keys()}
    
    def test_few_pokemon(self, count=3):
        """
        テスト用：少数のポケモンで動作確認
        """
        print(f"🧪 {count}匹のポケモンでテスト開始...")
        
        # pokemon_data.jsonを読み込み
        with open('pokemon_data.json', 'r', encoding='utf-8') as f:
            pokemon_data = json.load(f)
        
        test_results = {}
        processed_count = 0
        
        for pokemon_id, pokemon_info in pokemon_data.items():
            if processed_count >= count:
                break
                
            pokemon_name = pokemon_info['name']
            dex_numbers = self.get_pokemon_dex_numbers(int(pokemon_id), pokemon_name)
            
            test_results[pokemon_id] = {
                'name': pokemon_name,
                'dex_numbers': dex_numbers
            }
            
            processed_count += 1
            time.sleep(1)  # レート制限対策
        
        # テスト結果を保存
        with open('test_dex_numbers.json', 'w', encoding='utf-8') as f:
            json.dump(test_results, f, ensure_ascii=False, indent=2)
        
        print(f"✅ テスト完了！結果をtest_dex_numbers.jsonに保存")
        return test_results
    
    def update_pokemon_data_with_dex_numbers(self, batch_size=50):
        """
        pokemon_data.jsonの全ポケモンに図鑑番号を追加
        """
        print("🚀 全ポケモンデータの更新開始...")
        
        # pokemon_data.jsonを読み込み
        with open('pokemon_data.json', 'r', encoding='utf-8') as f:
            pokemon_data = json.load(f)
        
        total_pokemon = len(pokemon_data)
        processed_count = 0
        
        for pokemon_id, pokemon_info in pokemon_data.items():
            pokemon_name = pokemon_info['name']
            
            # 図鑑番号を取得
            dex_numbers = self.get_pokemon_dex_numbers(int(pokemon_id), pokemon_name)
            
            # pokemon_dataに追加
            pokemon_data[pokemon_id]['game_dex_numbers'] = dex_numbers
            
            processed_count += 1
            
            # 進捗表示
            if processed_count % 10 == 0:
                print(f"📊 進捗: {processed_count}/{total_pokemon} ({processed_count/total_pokemon*100:.1f}%)")
            
            # バッチごとに保存
            if processed_count % batch_size == 0:
                print(f"💾 中間保存中... ({processed_count}匹完了)")
                with open('pokemon_data.json', 'w', encoding='utf-8') as f:
                    json.dump(pokemon_data, f, ensure_ascii=False, indent=2)
            
            time.sleep(1)  # レート制限対策
        
        # 最終保存
        with open('pokemon_data.json', 'w', encoding='utf-8') as f:
            json.dump(pokemon_data, f, ensure_ascii=False, indent=2)
        
        print(f"🎉 全ポケモンデータの更新完了！{total_pokemon}匹処理")

def main():
    updater = GameDexNumberUpdater()
    
    print("🎮 ゲームタイトル別図鑑番号更新ツール")
    print("=" * 50)
    
    while True:
        print("\n選択してください:")
        print("1. テスト実行（3匹のポケモンで確認）")
        print("2. 全ポケモンデータ更新")
        print("3. 終了")
        
        choice = input("選択 (1-3): ").strip()
        
        if choice == "1":
            updater.test_few_pokemon(3)
        elif choice == "2":
            confirm = input("⚠️  全ポケモンデータを更新します。続行しますか？ (y/N): ").strip().lower()
            if confirm == 'y':
                updater.update_pokemon_data_with_dex_numbers()
            else:
                print("キャンセルされました。")
        elif choice == "3":
            print("終了します。")
            break
        else:
            print("無効な選択です。")

if __name__ == "__main__":
    main()