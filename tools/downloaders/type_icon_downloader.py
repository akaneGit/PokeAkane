"""
タイプアイコン画像ダウンロードツール 💎
ポケモンの18タイプのアイコン画像を収集
"""

import requests
import os
from urllib.parse import urlparse

class TypeIconDownloader:
    def __init__(self):
        self.type_icons = {
            # ポケモン公式風のタイプアイコンURL（例）
            "ノーマル": "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/normal.png",
            "ほのお": "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/fire.png", 
            "みず": "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/water.png",
            "でんき": "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/electric.png",
            "くさ": "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/grass.png",
            "こおり": "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/ice.png",
            "かくとう": "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/fighting.png",
            "どく": "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/poison.png",
            "じめん": "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/ground.png",
            "ひこう": "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/flying.png",
            "エスパー": "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/psychic.png",
            "むし": "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/bug.png",
            "いわ": "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/rock.png",
            "ゴースト": "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/ghost.png",
            "ドラゴン": "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/dragon.png",
            "あく": "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/dark.png",
            "はがね": "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/steel.png",
            "フェアリー": "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/fairy.png"
        }
        
        self.output_dir = "type_images"

    def download_type_icon(self, type_name, url):
        """単一タイプアイコンのダウンロード"""
        try:
            print(f"🔄 {type_name}タイプアイコンダウンロード中...")
            
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                filename = f"{type_name}.png"
                filepath = os.path.join(self.output_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                print(f"✅ {type_name}タイプ保存完了: {filepath}")
                return True
            else:
                print(f"❌ {type_name}タイプ取得失敗: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ {type_name}タイプエラー: {str(e)}")
            return False

    def download_all_icons(self):
        """全タイプアイコンのダウンロード"""
        print("🚀 タイプアイコン一括ダウンロード開始！")
        
        # ディレクトリ作成
        os.makedirs(self.output_dir, exist_ok=True)
        
        success_count = 0
        total_count = len(self.type_icons)
        
        for type_name, url in self.type_icons.items():
            if self.download_type_icon(type_name, url):
                success_count += 1
        
        print(f"🎉 タイプアイコンダウンロード完了！ {success_count}/{total_count}")

    def create_backup_icons(self):
        """URLが使えない場合のバックアップ用簡易アイコン作成"""
        print("🔧 バックアップ用シンプルアイコン作成中...")
        
        from PIL import Image, ImageDraw, ImageFont
        
        # タイプ別カラー
        type_colors = {
            "ノーマル": "#A8A878", "ほのお": "#F08030", "みず": "#6890F0",
            "でんき": "#F8D030", "くさ": "#78C850", "こおり": "#98D8D8",
            "かくとう": "#C03028", "どく": "#A040A0", "じめん": "#E0C068",
            "ひこう": "#A890F0", "エスパー": "#F85888", "むし": "#A8B820",
            "いわ": "#B8A038", "ゴースト": "#705898", "ドラゴン": "#7038F8",
            "あく": "#705848", "はがね": "#B8B8D0", "フェアリー": "#EE99AC"
        }
        
        for type_name, color in type_colors.items():
            try:
                # 64x64のシンプルなアイコン作成
                img = Image.new('RGB', (64, 64), color)
                draw = ImageDraw.Draw(img)
                
                # テキスト描画（簡易）
                draw.text((10, 20), type_name[:2], fill='white')
                
                filepath = os.path.join(self.output_dir, f"{type_name}_backup.png")
                img.save(filepath)
                print(f"✅ {type_name}バックアップアイコン作成: {filepath}")
                
            except Exception as e:
                print(f"❌ {type_name}バックアップ作成失敗: {e}")

def main():
    print("💎 タイプアイコンダウンロードツール起動！")
    
    downloader = TypeIconDownloader()
    
    # メインダウンロード実行
    downloader.download_all_icons()
    
    # バックアップアイコンも作成（optional）
    try:
        downloader.create_backup_icons()
    except:
        print("⚠️ バックアップアイコン作成はスキップ（PILライブラリが必要）")
    
    print("✨ タイプアイコン準備完了！")

if __name__ == "__main__":
    main()