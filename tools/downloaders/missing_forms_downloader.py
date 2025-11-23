#!/usr/bin/env python3
"""
不足フォルムポケモン画像ダウンローダー
PokemonDBから不足しているフォルム画像を取得して既存の命名規則で保存
"""

import requests
import os
import time
from pathlib import Path

class MissingFormsDownloader:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.pokemon_images_path = self.base_path / "pokemon_images"
        self.forms_path = self.pokemon_images_path / "forms"
        self.patterns_path = self.pokemon_images_path / "patterns"
        
        # 保存フォルダ作成
        self.forms_path.mkdir(parents=True, exist_ok=True)
        self.patterns_path.mkdir(parents=True, exist_ok=True)
        
        # PokemonDB base URL
        self.pokemondb_base = "https://img.pokemondb.net/artwork"
        
        # リクエスト間隔（秒）
        self.delay = 1

    def download_image(self, url, filepath):
        """画像をダウンロードして保存"""
        try:
            print(f"ダウンロード中: {url}")
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"保存完了: {filepath}")
            time.sleep(self.delay)
            return True
            
        except Exception as e:
            print(f"エラー: {url} -> {e}")
            return False

    def download_regional_forms(self):
        """地域フォルム画像をダウンロード"""
        print("=== 地域フォルム画像ダウンロード開始 ===")
        
        regional_forms = [
            # パルデアタウロス
            {
                "dex": "128",
                "name": "tauros-paldea-combat",
                "filename": "128_tauros-paldea-combat.png",
                "shiny": "128_tauros-paldea-combat_shiny.png"
            },
            {
                "dex": "128",
                "name": "tauros-paldea-blaze",
                "filename": "128_tauros-paldea-blaze.png",
                "shiny": "128_tauros-paldea-blaze_shiny.png"
            },
            {
                "dex": "128",
                "name": "tauros-paldea-aqua",
                "filename": "128_tauros-paldea-aqua.png",
                "shiny": "128_tauros-paldea-aqua_shiny.png"
            },
            # ガラルペルシアン
            {
                "dex": "53",
                "name": "persian-galar",
                "filename": "053_persian-galar.png",
                "shiny": "053_persian-galar_shiny.png"
            }
        ]
        
        for pokemon in regional_forms:
            # 通常版
            normal_url = f"{self.pokemondb_base}/{pokemon['name']}.jpg"
            normal_path = self.forms_path / pokemon['filename']
            self.download_image(normal_url, normal_path)
            
            # 色違い版
            shiny_url = f"{self.pokemondb_base}/shiny/{pokemon['name']}.jpg"
            shiny_path = self.forms_path / pokemon['shiny']
            self.download_image(shiny_url, shiny_path)

    def download_battle_forms(self):
        """バトルフォルム画像をダウンロード"""
        print("=== バトルフォルム画像ダウンロード開始 ===")
        
        battle_forms = [
            # ギルガルド
            {
                "dex": "681",
                "forms": [
                    {"name": "aegislash-shield", "filename": "681_aegislash-shield.png"},
                    {"name": "aegislash-blade", "filename": "681_aegislash-blade.png"}
                ]
            },
            # ヒヒダルマ
            {
                "dex": "555",
                "forms": [
                    {"name": "darmanitan-standard", "filename": "555_darmanitan-standard.png"},
                    {"name": "darmanitan-zen", "filename": "555_darmanitan-zen.png"}
                ]
            },
            # メロエッタ
            {
                "dex": "648",
                "forms": [
                    {"name": "meloetta-aria", "filename": "648_meloetta-aria.png"},
                    {"name": "meloetta-pirouette", "filename": "648_meloetta-pirouette.png"}
                ]
            },
            # ギラティナ
            {
                "dex": "487",
                "forms": [
                    {"name": "giratina-altered", "filename": "487_giratina-altered.png"},
                    {"name": "giratina-origin", "filename": "487_giratina-origin.png"}
                ]
            },
            # シェイミ
            {
                "dex": "492",
                "forms": [
                    {"name": "shaymin-land", "filename": "492_shaymin-land.png"},
                    {"name": "shaymin-sky", "filename": "492_shaymin-sky.png"}
                ]
            }
        ]
        
        for pokemon in battle_forms:
            for form in pokemon['forms']:
                # 通常版
                normal_url = f"{self.pokemondb_base}/{form['name']}.jpg"
                normal_path = self.patterns_path / form['filename']
                self.download_image(normal_url, normal_path)
                
                # 色違い版
                shiny_filename = form['filename'].replace('.png', '_shiny.png')
                shiny_url = f"{self.pokemondb_base}/shiny/{form['name']}.jpg"
                shiny_path = self.patterns_path / shiny_filename
                self.download_image(shiny_url, shiny_path)

    def download_modern_forms(self):
        """現代ポケモンフォルム画像をダウンロード"""
        print("=== 現代ポケモンフォルム画像ダウンロード開始 ===")
        
        modern_forms = [
            # オドリドリ
            {
                "dex": "741",
                "forms": [
                    {"name": "oricorio-baile", "filename": "741_oricorio-baile.png"},
                    {"name": "oricorio-pom-pom", "filename": "741_oricorio-pom-pom.png"},
                    {"name": "oricorio-pau", "filename": "741_oricorio-pau.png"},
                    {"name": "oricorio-sensu", "filename": "741_oricorio-sensu.png"}
                ]
            },
            # ルガルガン
            {
                "dex": "745",
                "forms": [
                    {"name": "lycanroc-midday", "filename": "745_lycanroc-midday.png"},
                    {"name": "lycanroc-midnight", "filename": "745_lycanroc-midnight.png"},
                    {"name": "lycanroc-dusk", "filename": "745_lycanroc-dusk.png"}
                ]
            },
            # ストリンダー
            {
                "dex": "849",
                "forms": [
                    {"name": "toxtricity-amped", "filename": "849_toxtricity-amped.png"},
                    {"name": "toxtricity-low-key", "filename": "849_toxtricity-low-key.png"}
                ]
            },
            # ウーラオス
            {
                "dex": "892",
                "forms": [
                    {"name": "urshifu-single-strike", "filename": "892_urshifu-single-strike.png"},
                    {"name": "urshifu-rapid-strike", "filename": "892_urshifu-rapid-strike.png"}
                ]
            }
        ]
        
        for pokemon in modern_forms:
            for form in pokemon['forms']:
                # 通常版
                normal_url = f"{self.pokemondb_base}/{form['name']}.jpg"
                normal_path = self.patterns_path / form['filename']
                self.download_image(normal_url, normal_path)
                
                # 色違い版
                shiny_filename = form['filename'].replace('.png', '_shiny.png')
                shiny_url = f"{self.pokemondb_base}/shiny/{form['name']}.jpg"
                shiny_path = self.patterns_path / shiny_filename
                self.download_image(shiny_url, shiny_path)

    def download_legendary_forms(self):
        """伝説ポケモンフォルム画像をダウンロード"""
        print("=== 伝説ポケモンフォルム画像ダウンロード開始 ===")
        
        legendary_forms = [
            # ゲンシカイキ
            {
                "dex": "382",
                "forms": [
                    {"name": "kyogre-primal", "filename": "382_kyogre-primal.png"}
                ]
            },
            {
                "dex": "383", 
                "forms": [
                    {"name": "groudon-primal", "filename": "383_groudon-primal.png"}
                ]
            },
            # ネクロズマ
            {
                "dex": "800",
                "forms": [
                    {"name": "necrozma-dusk", "filename": "800_necrozma-dusk.png"},
                    {"name": "necrozma-dawn", "filename": "800_necrozma-dawn.png"},
                    {"name": "necrozma-ultra", "filename": "800_necrozma-ultra.png"}
                ]
            },
            # ジガルデ
            {
                "dex": "718",
                "forms": [
                    {"name": "zygarde-10", "filename": "718_zygarde-10.png"},
                    {"name": "zygarde-50", "filename": "718_zygarde-50.png"},
                    {"name": "zygarde-complete", "filename": "718_zygarde-complete.png"}
                ]
            },
            # テラパゴス
            {
                "dex": "1024",
                "forms": [
                    {"name": "terapagos-normal", "filename": "1024_terapagos-normal.png"},
                    {"name": "terapagos-terastal", "filename": "1024_terapagos-terastal.png"},
                    {"name": "terapagos-stellar", "filename": "1024_terapagos-stellar.png"}
                ]
            }
        ]
        
        for pokemon in legendary_forms:
            for form in pokemon['forms']:
                # 通常版
                normal_url = f"{self.pokemondb_base}/{form['name']}.jpg"
                normal_path = self.patterns_path / form['filename']
                self.download_image(normal_url, normal_path)
                
                # 色違い版
                shiny_filename = form['filename'].replace('.png', '_shiny.png')
                shiny_url = f"{self.pokemondb_base}/shiny/{form['name']}.jpg"
                shiny_path = self.patterns_path / shiny_filename
                self.download_image(shiny_url, shiny_path)

    def download_size_variants(self):
        """サイズバリエーション画像をダウンロード"""
        print("=== サイズバリエーション画像ダウンロード開始 ===")
        
        size_variants = [
            # バケッチャ
            {
                "dex": "710",
                "forms": [
                    {"name": "pumpkaboo-small", "filename": "710_pumpkaboo-small.png"},
                    {"name": "pumpkaboo-average", "filename": "710_pumpkaboo-average.png"},
                    {"name": "pumpkaboo-large", "filename": "710_pumpkaboo-large.png"},
                    {"name": "pumpkaboo-super", "filename": "710_pumpkaboo-super.png"}
                ]
            },
            # パンプジン
            {
                "dex": "711",
                "forms": [
                    {"name": "gourgeist-small", "filename": "711_gourgeist-small.png"},
                    {"name": "gourgeist-average", "filename": "711_gourgeist-average.png"},
                    {"name": "gourgeist-large", "filename": "711_gourgeist-large.png"},
                    {"name": "gourgeist-super", "filename": "711_gourgeist-super.png"}
                ]
            }
        ]
        
        for pokemon in size_variants:
            for form in pokemon['forms']:
                # 通常版
                normal_url = f"{self.pokemondb_base}/{form['name']}.jpg"
                normal_path = self.patterns_path / form['filename']
                self.download_image(normal_url, normal_path)
                
                # 色違い版
                shiny_filename = form['filename'].replace('.png', '_shiny.png')
                shiny_url = f"{self.pokemondb_base}/shiny/{form['name']}.jpg"
                shiny_path = self.patterns_path / shiny_filename
                self.download_image(shiny_url, shiny_path)

    def run(self):
        """全ての不足フォルム画像をダウンロード"""
        print("🔄 不足フォルム画像ダウンロード開始")
        print(f"保存先: {self.pokemon_images_path}")
        
        try:
            # 地域フォルム
            self.download_regional_forms()
            
            # バトルフォルム
            self.download_battle_forms()
            
            # 現代ポケモンフォルム
            self.download_modern_forms()
            
            # 伝説ポケモンフォルム
            self.download_legendary_forms()
            
            # サイズバリエーション
            self.download_size_variants()
            
            print("\n✅ 全ての不足フォルム画像ダウンロード完了!")
            
        except KeyboardInterrupt:
            print("\n⚠️ ダウンロードが中断されました")
        except Exception as e:
            print(f"\n❌ エラーが発生しました: {e}")

def main():
    # ベースパスを設定（PokeAkaneプロジェクトのルート）
    base_path = Path(__file__).parent.parent
    
    downloader = MissingFormsDownloader(base_path)
    downloader.run()

if __name__ == "__main__":
    main()