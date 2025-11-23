"""
PokeAkane データ収集ツール - 最強版 🔥
PokeAPIから全ポケモンの詳細データを収集してJSONデータベースを構築
"""

import requests
import json
import time
from urllib.parse import urljoin
import os

class PokemonDataCollector:
    def __init__(self):
        self.base_url = "https://pokeapi.co/api/v2/"
        self.pokemon_data = {}
        self.type_data = {}
        self.evolution_chains = {}
        
        # 世代別範囲定義
        self.generations = {
            1: (1, 151),      # カントー
            2: (152, 251),    # ジョウト  
            3: (252, 386),    # ホウエン
            4: (387, 493),    # シンオウ
            5: (494, 649),    # イッシュ
            6: (650, 721),    # カロス
            7: (722, 809),    # アローラ
            8: (810, 905),    # ガラル
            9: (906, 1025)    # パルデア
        }
        
        # 外部サイトURLテンプレート
        self.external_links = {
            "kouryaku": "https://pokemon.gamewith.jp/article/show/{id}",
            "gamewith": "https://gamewith.jp/pokemon-go/article/show/{id}",
            "game8": "https://game8.jp/pokemon-sv/pokemon/{id}"
        }

    def get_pokemon_basic_data(self, pokemon_id):
        """基本ポケモンデータ取得"""
        print(f"🔄 #{pokemon_id:03d} のデータ取得中...")
        
        try:
            # 基本情報取得
            url = f"{self.base_url}pokemon/{pokemon_id}"
            response = requests.get(url, timeout=30)
            if response.status_code != 200:
                print(f"❌ #{pokemon_id:03d} 取得失敗: {response.status_code}")
                return None
                
            pokemon = response.json()
            
            # ポケモン種族情報取得
            species_url = pokemon['species']['url']
            species_response = requests.get(species_url, timeout=30)
            species = species_response.json()
            
            # 日本語名取得
            japanese_name = "Unknown"
            for name in species['names']:
                if name['language']['name'] == 'ja-Hrkt':
                    japanese_name = name['name']
                    break
            
            # タイプ情報
            types = [t['type']['name'] for t in pokemon['types']]
            types_jp = self.translate_types(types)
            
            # 特性情報
            abilities = []
            for ability in pokemon['abilities']:
                ability_name = self.get_ability_japanese_name(ability['ability']['url'])
                if ability['is_hidden']:
                    abilities.append(f"{ability_name}(隠れ)")
                else:
                    abilities.append(ability_name)
            
            # 種族値
            stats = {}
            stat_names = {
                'hp': 'hp',
                'attack': 'attack', 
                'defense': 'defense',
                'special-attack': 'special_attack',
                'special-defense': 'special_defense',
                'speed': 'speed'
            }
            
            for stat in pokemon['stats']:
                stat_key = stat_names.get(stat['stat']['name'])
                if stat_key:
                    stats[stat_key] = stat['base_stat']
            
            # 世代判定
            generation = self.get_generation(pokemon_id)
            
            # 進化チェーン取得
            evolution_chain_url = species['evolution_chain']['url']
            evolution_data = self.get_evolution_data(evolution_chain_url, pokemon_id)
            
            pokemon_data = {
                "id": pokemon_id,
                "name": japanese_name,
                "name_en": pokemon['name'],
                "types": types_jp,
                "types_en": types,
                "abilities": abilities,
                "stats": stats,
                "height": pokemon['height'] / 10,  # デシメートルをメートルに
                "weight": pokemon['weight'] / 10,  # ヘクトグラムをキログラムに
                "generation": generation,
                "evolution": evolution_data,
                "external_links": {
                    "kouryaku": self.external_links["kouryaku"].format(id=pokemon_id),
                    "gamewith": self.external_links["gamewith"].format(id=pokemon_id),
                    "game8": self.external_links["game8"].format(id=pokemon_id)
                }
            }
            
            print(f"✅ #{pokemon_id:03d} {japanese_name} 完了")
            return pokemon_data
            
        except Exception as e:
            print(f"❌ #{pokemon_id:03d} エラー: {str(e)}")
            return None

    def translate_types(self, types_en):
        """タイプ名を英語から日本語に変換"""
        type_translation = {
            'normal': 'ノーマル', 'fire': 'ほのお', 'water': 'みず',
            'electric': 'でんき', 'grass': 'くさ', 'ice': 'こおり',
            'fighting': 'かくとう', 'poison': 'どく', 'ground': 'じめん',
            'flying': 'ひこう', 'psychic': 'エスパー', 'bug': 'むし',
            'rock': 'いわ', 'ghost': 'ゴースト', 'dragon': 'ドラゴン',
            'dark': 'あく', 'steel': 'はがね', 'fairy': 'フェアリー'
        }
        return [type_translation.get(t, t) for t in types_en]

    def get_ability_japanese_name(self, ability_url):
        """特性の日本語名取得"""
        try:
            response = requests.get(ability_url, timeout=10)
            ability_data = response.json()
            
            for name in ability_data['names']:
                if name['language']['name'] == 'ja-Hrkt':
                    return name['name']
            return ability_data['name']  # フォールバック
        except:
            return "Unknown"

    def get_generation(self, pokemon_id):
        """ポケモンIDから世代を判定"""
        for gen, (start, end) in self.generations.items():
            if start <= pokemon_id <= end:
                return gen
        return 9  # デフォルト

    def get_evolution_data(self, evolution_chain_url, pokemon_id):
        """進化チェーンデータ取得"""
        try:
            response = requests.get(evolution_chain_url, timeout=10)
            chain_data = response.json()
            
            # 進化チェーンを平坦化
            evolution_list = []
            self.flatten_evolution_chain(chain_data['chain'], evolution_list)
            
            # 該当ポケモンの前後を特定
            prev_pokemon = None
            next_pokemon = []
            
            for i, evo in enumerate(evolution_list):
                if evo['id'] == pokemon_id:
                    if i > 0:
                        prev_pokemon = evolution_list[i-1]['id']
                    if i < len(evolution_list) - 1:
                        next_pokemon = [evolution_list[i+1]['id']]
                    break
            
            return {
                "prev": prev_pokemon,
                "next": next_pokemon
            }
            
        except Exception as e:
            print(f"進化データ取得エラー: {e}")
            return {"prev": None, "next": []}

    def flatten_evolution_chain(self, chain, result):
        """進化チェーンを再帰的に平坦化"""
        # ポケモンIDを取得
        pokemon_url = chain['species']['url']
        pokemon_id = int(pokemon_url.split('/')[-2])
        
        result.append({
            'id': pokemon_id,
            'name': chain['species']['name']
        })
        
        # 次の進化があれば再帰
        for evolution in chain['evolves_to']:
            self.flatten_evolution_chain(evolution, result)

    def collect_all_pokemon_data(self, start=1, end=1025):
        """全ポケモンデータ収集"""
        print(f"🚀 ポケモンデータ収集開始 (#{start:03d} ～ #{end:03d})")
        
        for pokemon_id in range(start, end + 1):
            # 既にデータがあればスキップ
            if str(pokemon_id) in self.pokemon_data:
                print(f"⏭️ #{pokemon_id:03d} は既に存在 - スキップ")
                continue
                
            # リトライロジック
            for attempt in range(3):  # 3回まで試行
                try:
                    pokemon_data = self.get_pokemon_basic_data(pokemon_id)
                    if pokemon_data:
                        self.pokemon_data[str(pokemon_id)] = pokemon_data
                        break
                except Exception as e:
                    print(f"⚠️ #{pokemon_id:03d} 試行{attempt+1}回目失敗: {e}")
                    if attempt < 2:  # 最後の試行でなければ待機
                        time.sleep(2)
                    else:
                        print(f"❌ #{pokemon_id:03d} 3回試行して失敗 - スキップ")
            
            # API制限対策
            time.sleep(0.2)
            
            # 100件ごとに中間保存
            if pokemon_id % 100 == 0:
                self.save_data(f"pokemon_data_backup_{pokemon_id}.json")
                print(f"💾 #{pokemon_id} まで中間保存完了")
        
        print("🎉 全ポケモンデータ収集完了！")

    def save_data(self, filename="pokemon_data.json"):
        """データをJSONファイルに保存"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.pokemon_data, f, ensure_ascii=False, indent=2)
        print(f"💾 {filename} に保存完了")

    def load_existing_data(self, filename="pokemon_data.json"):
        """既存データの読み込み"""
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                self.pokemon_data = json.load(f)
            print(f"📂 既存データ {len(self.pokemon_data)} 件読み込み完了")

def main():
    print("🌟 PokeAkane 最強データ収集ツール起動！")
    
    collector = PokemonDataCollector()
    
    # 既存データがあれば読み込み
    collector.load_existing_data()
    
    # データ収集実行
    collector.collect_all_pokemon_data(1, 1025)  # 全ポケモン収集！
    
    # 最終保存
    collector.save_data()
    
    print("✨ データ収集完了！pokemon_data.json をチェックしてね〜")

if __name__ == "__main__":
    main()