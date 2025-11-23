#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
地域アイコン仮画像生成ツール
PokeAkane用の地域アイコンの仮画像を生成します
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_region_icon(text, filename, size=(48, 48), bg_color=(70, 130, 180), text_color=(255, 255, 255)):
    """
    地域アイコンの仮画像を生成
    
    Args:
        text: アイコンに表示するテキスト
        filename: 保存ファイル名
        size: アイコンサイズ (width, height)
        bg_color: 背景色 (R, G, B)
        text_color: 文字色 (R, G, B)
    """
    # 新しい画像を作成（RGBA形式で透明度対応）
    img = Image.new('RGBA', size, (*bg_color, 255))
    draw = ImageDraw.Draw(img)
    
    # 円形の背景を描画
    margin = 4
    draw.ellipse([margin, margin, size[0]-margin, size[1]-margin], 
                 fill=(*bg_color, 255), outline=(255, 255, 255, 200), width=2)
    
    # テキストを描画
    try:
        # フォントサイズを自動調整
        font_size = min(size) // 4
        font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # テキストの位置を中央に配置
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # テキストに影をつける
    draw.text((x+1, y+1), text, fill=(0, 0, 0, 128), font=font)
    draw.text((x, y), text, fill=(*text_color, 255), font=font)
    
    return img

def generate_all_region_icons():
    """全ての地域アイコンを生成"""
    
    # 出力ディレクトリ
    output_dir = "c:/Users/rarur/OneDrive/ドキュメント/GitHub/PokeAkane/region_icons"
    os.makedirs(output_dir, exist_ok=True)
    
    # 地域アイコン定義（名前, ファイル名, 表示テキスト, 背景色）
    regions = [
        ("全国図鑑", "national.png", "全国", (70, 130, 180)),      # スティールブルー
        ("カントー", "kanto.png", "関東", (255, 69, 0)),           # レッドオレンジ  
        ("ジョウト", "johto.png", "城都", (255, 215, 0)),          # ゴールド
        ("ホウエン", "hoenn.png", "豊縁", (50, 205, 50)),          # ライムグリーン
        ("シンオウ", "sinnoh.png", "神奥", (138, 43, 226)),        # ブルーバイオレット
        ("イッシュ", "unova.png", "合衆", (255, 20, 147)),         # ディープピンク
        ("カロス", "kalos.png", "カロス", (0, 191, 255)),          # ディープスカイブルー
        ("アローラ", "alola.png", "阿羅", (255, 165, 0)),          # オレンジ
        ("ガラル", "galar.png", "ガラル", (128, 0, 128)),          # パープル
        ("ヒスイ", "hisui.png", "翡翠", (34, 139, 34)),            # フォレストグリーン
        ("パルデア", "paldea.png", "パルデ", (220, 20, 60)),       # クリムゾン
        ("ミアレ", "lumiose.png", "ミアレ", (255, 105, 180))       # ホットピンク
    ]
    
    print("🎨 地域アイコン仮画像生成開始...")
    
    for region_name, filename, display_text, bg_color in regions:
        print(f"📍 {region_name} ({filename}) を生成中...")
        
        # アイコン生成
        icon = create_region_icon(display_text, filename, size=(48, 48), bg_color=bg_color)
        
        # 保存
        output_path = os.path.join(output_dir, filename)
        icon.save(output_path, 'PNG')
        print(f"   ✅ 保存完了: {output_path}")
    
    print(f"\n🎉 全{len(regions)}個の地域アイコン生成完了！")
    print(f"📁 出力先: {output_dir}")
    
    # サンプル表示用の大きいバージョンも作成
    print("\n🖼️ サンプル表示用大型アイコンも作成中...")
    sample_dir = os.path.join(output_dir, "samples")
    os.makedirs(sample_dir, exist_ok=True)
    
    for region_name, filename, display_text, bg_color in regions[:3]:  # 最初の3個だけサンプル
        large_icon = create_region_icon(display_text, filename, size=(128, 128), bg_color=bg_color)
        sample_path = os.path.join(sample_dir, f"large_{filename}")
        large_icon.save(sample_path, 'PNG')
    
    print("✨ サンプル大型アイコンも完成〜！")

if __name__ == "__main__":
    generate_all_region_icons()