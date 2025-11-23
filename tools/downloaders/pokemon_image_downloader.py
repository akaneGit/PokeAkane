#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ポケモンZA図鑑 - 姿違い画像取得スクリプト
yakkun.comからポケモンの姿違い画像を自動取得する超かわいいツール♡
"""

import requests
import os
import time
import json
from urllib.parse import urljoin
from pathlib import Path

# 姿違いポケモンの詳細データ
POKEMON_FORMS_DATA = {
    # ニャオニクス（性別違い）
    44: {
        "name": "ニャオニクス",
        "forms": [
            {"name": "ニャオニクス(オス)", "url_suffix": "", "filename": "pokemon_044_male.png"},
            {"name": "ニャオニクス(メス)", "url_suffix": "f", "filename": "pokemon_044_female.png"}
        ]
    },
    
    # フラベベ系統（花の色違い）
    38: {
        "name": "フラベベ",
        "forms": [
            {"name": "フラベベ(赤い花)", "url_suffix": "", "filename": "pokemon_038_red.png"},
            {"name": "フラベベ(黄色い花)", "url_suffix": "y", "filename": "pokemon_038_yellow.png"},
            {"name": "フラベベ(オレンジの花)", "url_suffix": "o", "filename": "pokemon_038_orange.png"},
            {"name": "フラベベ(青い花)", "url_suffix": "b", "filename": "pokemon_038_blue.png"},
            {"name": "フラベベ(白い花)", "url_suffix": "w", "filename": "pokemon_038_white.png"}
        ]
    },
    
    39: {
        "name": "フラエッテ",
        "forms": [
            {"name": "フラエッテ(赤い花)", "url_suffix": "", "filename": "pokemon_039_red.png"},
            {"name": "フラエッテ(黄色い花)", "url_suffix": "y", "filename": "pokemon_039_yellow.png"},
            {"name": "フラエッテ(オレンジの花)", "url_suffix": "o", "filename": "pokemon_039_orange.png"},
            {"name": "フラエッテ(青い花)", "url_suffix": "b", "filename": "pokemon_039_blue.png"},
            {"name": "フラエッテ(白い花)", "url_suffix": "w", "filename": "pokemon_039_white.png"},
            {"name": "フラエッテ(永遠の花)", "url_suffix": "e", "filename": "pokemon_039_eternal.png"}
        ]
    },
    
    40: {
        "name": "フラージェス",
        "forms": [
            {"name": "フラージェス(赤い花)", "url_suffix": "", "filename": "pokemon_040_red.png"},
            {"name": "フラージェス(黄色い花)", "url_suffix": "y", "filename": "pokemon_040_yellow.png"},
            {"name": "フラージェス(オレンジの花)", "url_suffix": "o", "filename": "pokemon_040_orange.png"},
            {"name": "フラージェス(青い花)", "url_suffix": "b", "filename": "pokemon_040_blue.png"},
            {"name": "フラージェス(白い花)", "url_suffix": "w", "filename": "pokemon_040_white.png"}
        ]
    },
    
    # ビビヨン（模様違い） - 数字ベースのURL構造
    17: {
        "name": "ビビヨン",
        "forms": [
            {"name": "ビビヨン(花園の模様)", "url_suffix": "", "filename": "pokemon_017_meadow.png"},
            {"name": "ビビヨン(雪国の模様)", "url_suffix": "_1", "filename": "pokemon_017_icy.png"},
            {"name": "ビビヨン(極地の模様)", "url_suffix": "_2", "filename": "pokemon_017_polar.png"},
            {"name": "ビビヨン(ツンドラの模様)", "url_suffix": "_3", "filename": "pokemon_017_tundra.png"},
            {"name": "ビビヨン(大陸の模様)", "url_suffix": "_4", "filename": "pokemon_017_continental.png"},
            {"name": "ビビヨン(庭園の模様)", "url_suffix": "_5", "filename": "pokemon_017_garden.png"},
            {"name": "ビビヨン(雅な模様)", "url_suffix": "_6", "filename": "pokemon_017_elegant.png"},
            {"name": "ビビヨン(現代の模様)", "url_suffix": "_7", "filename": "pokemon_017_modern.png"},
            {"name": "ビビヨン(海洋の模様)", "url_suffix": "_8", "filename": "pokemon_017_marine.png"},
            {"name": "ビビヨン(群島の模様)", "url_suffix": "_9", "filename": "pokemon_017_archipelago.png"},
            {"name": "ビビヨン(高原の模様)", "url_suffix": "_10", "filename": "pokemon_017_high_plains.png"},
            {"name": "ビビヨン(砂塵の模様)", "url_suffix": "_11", "filename": "pokemon_017_sandstorm.png"},
            {"name": "ビビヨン(大河の模様)", "url_suffix": "_12", "filename": "pokemon_017_river.png"},
            {"name": "ビビヨン(モンスーンの模様)", "url_suffix": "_13", "filename": "pokemon_017_monsoon.png"},
            {"name": "ビビヨン(サバンナの模様)", "url_suffix": "_14", "filename": "pokemon_017_savanna.png"},
            {"name": "ビビヨン(太陽の模様)", "url_suffix": "_15", "filename": "pokemon_017_sun.png"},
            {"name": "ビビヨン(オーシャンの模様)", "url_suffix": "_16", "filename": "pokemon_017_ocean.png"},
            {"name": "ビビヨン(ジャングルの模様)", "url_suffix": "_17", "filename": "pokemon_017_jungle.png"}
        ]
    },
    
    # トリミアン（カット違い） - 数字ベースのURL構造
    158: {
        "name": "トリミアン",
        "forms": [
            {"name": "トリミアン(やせいのすがた)", "url_suffix": "", "filename": "pokemon_158_natural.png"},
            {"name": "トリミアン(ハートカット)", "url_suffix": "_1", "filename": "pokemon_158_heart.png"},
            {"name": "トリミアン(スターカット)", "url_suffix": "_2", "filename": "pokemon_158_star.png"},
            {"name": "トリミアン(ダイヤカット)", "url_suffix": "_3", "filename": "pokemon_158_diamond.png"},
            {"name": "トリミアン(レディカット)", "url_suffix": "_4", "filename": "pokemon_158_debutante.png"},
            {"name": "トリミアン(マダムカット)", "url_suffix": "_5", "filename": "pokemon_158_matron.png"},
            {"name": "トリミアン(ジェントルカット)", "url_suffix": "_6", "filename": "pokemon_158_dandy.png"},
            {"name": "トリミアン(クイーンカット)", "url_suffix": "_7", "filename": "pokemon_158_la_reine.png"},
            {"name": "トリミアン(カブキカット)", "url_suffix": "_8", "filename": "pokemon_158_pharaoh.png"}
        ]
    },
    
    # バケッチャ・パンプジン（サイズ違い）
    204: {
        "name": "バケッチャ",
        "forms": [
            {"name": "バケッチャ(小さいサイズ)", "url_suffix": "s", "filename": "pokemon_204_small.png"},
            {"name": "バケッチャ(普通のサイズ)", "url_suffix": "", "filename": "pokemon_204_average.png"},
            {"name": "バケッチャ(大きいサイズ)", "url_suffix": "l", "filename": "pokemon_204_large.png"},
            {"name": "バケッチャ(特大サイズ)", "url_suffix": "k", "filename": "pokemon_204_super.png"}
        ]
    },
    
    205: {
        "name": "パンプジン",
        "forms": [
            {"name": "パンプジン(小さいサイズ)", "url_suffix": "s", "filename": "pokemon_205_small.png"},
            {"name": "パンプジン(普通のサイズ)", "url_suffix": "", "filename": "pokemon_205_average.png"},
            {"name": "パンプジン(大きいサイズ)", "url_suffix": "l", "filename": "pokemon_205_large.png"},
            {"name": "パンプジン(特大サイズ)", "url_suffix": "k", "filename": "pokemon_205_super.png"}
        ]
    },
    
    # ギルガルド（フォルム違い）
    73: {
        "name": "ギルガルド",
        "forms": [
            {"name": "ギルガルド(シールドフォルム)", "url_suffix": "", "filename": "pokemon_073_shield.png"},
            {"name": "ギルガルド(ブレードフォルム)", "url_suffix": "b", "filename": "pokemon_073_blade.png"}
        ]
    },
    
    # ジガルデ（フォルム違い）
    230: {
        "name": "ジガルデ",
        "forms": [
            {"name": "ジガルデ(10%フォルム)", "url_suffix": "t", "filename": "pokemon_230_10.png"},
            {"name": "ジガルデ(50%フォルム)", "url_suffix": "", "filename": "pokemon_230_50.png"},
            {"name": "ジガルデ(パーフェクトフォルム)", "url_suffix": "c", "filename": "pokemon_230_perfect.png"}
        ]
    },
    
    # ヤドン・ヤドラン・ヤドキング（ガラルの姿）
    137: {
        "name": "ヤドン",
        "forms": [
            {"name": "ヤドン", "url_suffix": "", "filename": "pokemon_137_normal.png"},
            {"name": "ヤドン(ガラル)", "url_suffix": "g", "filename": "pokemon_137_galar.png"}
        ]
    },
    
    138: {
        "name": "ヤドラン",
        "forms": [
            {"name": "ヤドラン", "url_suffix": "", "filename": "pokemon_138_normal.png"},
            {"name": "ヤドラン(ガラル)", "url_suffix": "g", "filename": "pokemon_138_galar.png"}
        ]
    },
    
    139: {
        "name": "ヤドキング",
        "forms": [
            {"name": "ヤドキング", "url_suffix": "", "filename": "pokemon_139_normal.png"},
            {"name": "ヤドキング(ガラル)", "url_suffix": "g", "filename": "pokemon_139_galar.png"}
        ]
    },
    
    # ライチュウ（アローラの姿）
    54: {
        "name": "ライチュウ",
        "forms": [
            {"name": "ライチュウ", "url_suffix": "", "filename": "pokemon_054_normal.png"},
            {"name": "ライチュウ(アローラ)", "url_suffix": "a", "filename": "pokemon_054_alola.png"}
        ]
    },
    
    # マッギョ（ガラルの姿）
    157: {
        "name": "マッギョ",
        "forms": [
            {"name": "マッギョ", "url_suffix": "", "filename": "pokemon_157_normal.png"},
            {"name": "マッギョ(ガラル)", "url_suffix": "g", "filename": "pokemon_157_galar.png"}
        ]
    },
    
    # ヌメイル・ヌメルゴン（ヒスイの姿）
    166: {
        "name": "ヌメイル",
        "forms": [
            {"name": "ヌメイル", "url_suffix": "", "filename": "pokemon_166_normal.png"},
            {"name": "ヌメイル(ヒスイ)", "url_suffix": "h", "filename": "pokemon_166_hisui.png"}
        ]
    },
    
    167: {
        "name": "ヌメルゴン",
        "forms": [
            {"name": "ヌメルゴン", "url_suffix": "", "filename": "pokemon_167_normal.png"},
            {"name": "ヌメルゴン(ヒスイ)", "url_suffix": "h", "filename": "pokemon_167_hisui.png"}
        ]
    },
    
    # クレベース（ヒスイの姿）
    175: {
        "name": "クレベース",
        "forms": [
            {"name": "クレベース", "url_suffix": "", "filename": "pokemon_175_normal.png"},
            {"name": "クレベース(ヒスイ)", "url_suffix": "h", "filename": "pokemon_175_hisui.png"}
        ]
    }
}

class PokemonImageDownloader:
    def __init__(self, output_dir="pokemon_images"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.base_url = "https://img.yakkun.com/poke/icon32/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def get_national_number_from_za_number(self, za_number):
        """ZA図鑑番号から全国図鑑番号を取得する簡易マッピング"""
        # 一部のポケモンの実際の全国図鑑番号
        mapping = {
            1: 152,    # チコリータ
            2: 153,    # ベイリーフ
            3: 154,    # メガニウム
            17: 666,   # ビビヨン
            38: 669,   # フラベベ
            39: 670,   # フラエッテ
            40: 671,   # フラージェス
            44: 678,   # ニャオニクス
            54: 26,    # ライチュウ
            73: 681,   # ギルガルド
            137: 79,   # ヤドン
            138: 80,   # ヤドラン
            139: 199,  # ヤドキング
            157: 618,  # マッギョ
            158: 676,  # トリミアン
            166: 705,  # ヌメイル
            167: 706,  # ヌメルゴン
            175: 713,  # クレベース
            204: 710,  # バケッチャ
            205: 711,  # パンプジン
            230: 718,  # ジガルデ
        }
        return mapping.get(za_number, za_number)
    
    def download_image(self, url, filename):
        """画像をダウンロードする"""
        try:
            print(f"📸 ダウンロード中: {filename}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            file_path = self.output_dir / filename
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ 成功: {filename}")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ エラー: {filename} - {e}")
            return False
    
    def download_pokemon_forms(self, za_number):
        """指定されたポケモンの全姿違いをダウンロード"""
        if za_number not in POKEMON_FORMS_DATA:
            print(f"⚠️  No.{za_number} の姿違いデータが見つかりません")
            return False
        
        pokemon_data = POKEMON_FORMS_DATA[za_number]
        national_number = self.get_national_number_from_za_number(za_number)
        
        print(f"\n🎀 {pokemon_data['name']} の姿違いをダウンロード開始! (No.{za_number})")
        
        success_count = 0
        total_count = len(pokemon_data['forms'])
        
        for form_data in pokemon_data['forms']:
            # yakkun.comの画像URL構築
            if form_data['url_suffix']:
                image_url = f"{self.base_url}n{national_number}{form_data['url_suffix']}.gif"
            else:
                image_url = f"{self.base_url}n{national_number}.gif"
            
            # ダウンロード実行
            if self.download_image(image_url, form_data['filename']):
                success_count += 1
            
            # サーバーに優しく
            time.sleep(1)
        
        print(f"📊 {pokemon_data['name']}: {success_count}/{total_count} 個の画像をダウンロード完了!")
        return success_count == total_count
    
    def download_all_forms(self):
        """全ての姿違いポケモンをダウンロード"""
        print("🌟 ポケモン姿違い画像の一括ダウンロードを開始します!")
        print(f"💾 保存先: {self.output_dir.absolute()}")
        
        total_pokemon = len(POKEMON_FORMS_DATA)
        success_pokemon = 0
        
        for za_number in sorted(POKEMON_FORMS_DATA.keys()):
            if self.download_pokemon_forms(za_number):
                success_pokemon += 1
            time.sleep(2)  # ポケモン間の待機時間
        
        print(f"\n🎉 ダウンロード完了!")
        print(f"📈 成功: {success_pokemon}/{total_pokemon} 種類のポケモン")
        
        # レポート生成
        self.generate_report()
    
    def generate_report(self):
        """ダウンロードレポートを生成"""
        report = {
            "download_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_pokemon": len(POKEMON_FORMS_DATA),
            "pokemon_forms": {}
        }
        
        for za_number, pokemon_data in POKEMON_FORMS_DATA.items():
            downloaded_forms = []
            for form_data in pokemon_data['forms']:
                file_path = self.output_dir / form_data['filename']
                if file_path.exists():
                    downloaded_forms.append({
                        "name": form_data['name'],
                        "filename": form_data['filename'],
                        "file_size": file_path.stat().st_size
                    })
            
            report["pokemon_forms"][za_number] = {
                "name": pokemon_data['name'],
                "total_forms": len(pokemon_data['forms']),
                "downloaded_forms": len(downloaded_forms),
                "forms": downloaded_forms
            }
        
        # JSONレポート保存
        report_path = self.output_dir / "download_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"📄 レポートを保存しました: {report_path}")

def main():
    print("🎀✨ ポケモンZA 姿違い画像ダウンローダー ✨🎀")
    print("=" * 50)
    
    downloader = PokemonImageDownloader()
    
    while True:
        print("\n📋 メニュー:")
        print("1. 全ての姿違いポケモンをダウンロード")
        print("2. 特定のポケモンをダウンロード")
        print("3. 利用可能な姿違いポケモン一覧を表示")
        print("4. 終了")
        
        choice = input("\n選択してください (1-4): ").strip()
        
        if choice == "1":
            downloader.download_all_forms()
            
        elif choice == "2":
            print("\n📝 利用可能なポケモン:")
            for za_num, data in sorted(POKEMON_FORMS_DATA.items()):
                print(f"  No.{za_num:03d}: {data['name']} ({len(data['forms'])}種類)")
            
            try:
                za_number = int(input("\nZA図鑑番号を入力してください: "))
                downloader.download_pokemon_forms(za_number)
            except ValueError:
                print("❌ 無効な番号です")
                
        elif choice == "3":
            print("\n🎨 姿違いポケモン一覧:")
            for za_num, data in sorted(POKEMON_FORMS_DATA.items()):
                print(f"\nNo.{za_num:03d}: {data['name']}")
                for form in data['forms']:
                    print(f"  └ {form['name']}")
                    
        elif choice == "4":
            print("👋 ダウンローダーを終了します。お疲れ様でした!")
            break
            
        else:
            print("❌ 無効な選択です")

if __name__ == "__main__":
    main()