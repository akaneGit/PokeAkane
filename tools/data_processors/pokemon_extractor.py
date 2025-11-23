#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ポケモンZA 図鑑画面からポケモン画像を抽出するツール
"""

import cv2
import numpy as np
from PIL import Image, ImageEnhance
import os
from pathlib import Path

class PokemonExtractor:
    def __init__(self, output_dir="extracted_pokemon"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def extract_pokemon_from_pokedex(self, image_path, pokemon_name=None, method="auto"):
        """
        ポケモン図鑑画面からポケモンを抽出
        
        Args:
            image_path: 入力画像のパス
            pokemon_name: 保存時の名前（Noneの場合は自動生成）
            method: 抽出方法 ("auto", "manual", "color_range")
        """
        # 画像読み込み
        image = cv2.imread(str(image_path))
        if image is None:
            print(f"❌ 画像が読み込めません: {image_path}")
            return None
            
        print(f"📸 画像読み込み成功: {image.shape}")
        
        if method == "auto":
            return self._extract_auto(image, pokemon_name, image_path)
        elif method == "manual":
            return self._extract_manual(image, pokemon_name, image_path)
        elif method == "color_range":
            return self._extract_color_range(image, pokemon_name, image_path)
            
    def _extract_auto(self, image, pokemon_name, image_path):
        """自動抽出（複数手法を試行）"""
        print("🤖 自動抽出モードで処理中...")
        
        # 手法1: 色範囲での背景除去
        result1 = self._extract_color_range(image, f"{pokemon_name}_method1" if pokemon_name else "auto_method1", image_path, save=False)
        
        # 手法2: エッジ検出
        result2 = self._extract_edge_detection(image, f"{pokemon_name}_method2" if pokemon_name else "auto_method2", image_path, save=False)
        
        # 手法3: 固定領域抽出
        result3 = self._extract_fixed_region(image, f"{pokemon_name}_method3" if pokemon_name else "auto_method3", image_path, save=False)
        
        # 結果を保存
        results = []
        for i, (result, method_name) in enumerate([(result1, "color_range"), (result2, "edge_detection"), (result3, "fixed_region")]):
            if result is not None:
                filename = f"{pokemon_name}_{method_name}.png" if pokemon_name else f"extracted_{method_name}.png"
                output_path = self.output_dir / filename
                cv2.imwrite(str(output_path), result)
                results.append(output_path)
                print(f"✅ 保存完了: {filename}")
        
        return results
    
    def _extract_color_range(self, image, pokemon_name, image_path, save=True):
        """色範囲指定での背景除去"""
        print("🎨 色範囲指定で背景除去中...")
        
        # BGR色空間をHSVに変換
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # 青い背景の色範囲を定義（HSV）
        # 図鑑の青い背景を除去
        lower_blue1 = np.array([100, 50, 50])   # 薄い青
        upper_blue1 = np.array([130, 255, 255]) # 濃い青
        
        lower_blue2 = np.array([90, 30, 30])    # より広範囲の青
        upper_blue2 = np.array([140, 255, 255])
        
        # マスク作成（背景部分）
        mask_blue1 = cv2.inRange(hsv, lower_blue1, upper_blue1)
        mask_blue2 = cv2.inRange(hsv, lower_blue2, upper_blue2)
        background_mask = cv2.bitwise_or(mask_blue1, mask_blue2)
        
        # モルフォロジー処理でノイズ除去
        kernel = np.ones((3,3), np.uint8)
        background_mask = cv2.morphologyEx(background_mask, cv2.MORPH_CLOSE, kernel)
        background_mask = cv2.morphologyEx(background_mask, cv2.MORPH_OPEN, kernel)
        
        # ポケモン領域のマスク（背景の逆）
        pokemon_mask = cv2.bitwise_not(background_mask)
        
        # 4チャンネル画像作成（BGRA）
        result = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        result[:, :, 3] = pokemon_mask  # アルファチャンネルにマスクを適用
        
        if save and pokemon_name:
            filename = f"{pokemon_name}_color_range.png"
            output_path = self.output_dir / filename
            cv2.imwrite(str(output_path), result)
            print(f"✅ 色範囲抽出完了: {filename}")
            return str(output_path)
            
        return result
    
    def _extract_edge_detection(self, image, pokemon_name, image_path, save=True):
        """エッジ検出による輪郭抽出"""
        print("📐 エッジ検出で輪郭抽出中...")
        
        # グレースケール変換
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # ガウシアンブラーでノイズ除去
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Cannyエッジ検出
        edges = cv2.Canny(blurred, 50, 150)
        
        # 輪郭検出
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # 最大の輪郭を取得（ポケモンと仮定）
            largest_contour = max(contours, key=cv2.contourArea)
            
            # バウンディングボックス取得
            x, y, w, h = cv2.boundingRect(largest_contour)
            
            # ポケモン領域を切り抜き
            pokemon_region = image[y:y+h, x:x+w]
            
            if save and pokemon_name:
                filename = f"{pokemon_name}_edge_detection.png"
                output_path = self.output_dir / filename
                cv2.imwrite(str(output_path), pokemon_region)
                print(f"✅ エッジ検出完了: {filename}")
                return str(output_path)
                
            return pokemon_region
        
        print("⚠️ 輪郭が検出できませんでした")
        return None
    
    def _extract_fixed_region(self, image, pokemon_name, image_path, save=True):
        """固定領域での抽出（図鑑画面用）"""
        print("📏 固定領域で抽出中...")
        
        h, w = image.shape[:2]
        
        # ポケモンZA図鑑画面の推定領域
        # 中央やや右寄り、テキスト領域を避ける
        start_x = int(w * 0.35)  # 左35%から
        end_x = int(w * 0.95)    # 右95%まで
        start_y = int(h * 0.15)  # 上15%から
        end_y = int(h * 0.75)    # 下75%まで
        
        # 領域切り抜き
        pokemon_region = image[start_y:end_y, start_x:end_x]
        
        if save and pokemon_name:
            filename = f"{pokemon_name}_fixed_region.png"
            output_path = self.output_dir / filename
            cv2.imwrite(str(output_path), pokemon_region)
            print(f"✅ 固定領域抽出完了: {filename}")
            return str(output_path)
            
        return pokemon_region
    
    def _extract_manual(self, image, pokemon_name, image_path):
        """手動での座標指定抽出"""
        print("✋ 手動座標指定モード（コンソール入力）")
        
        h, w = image.shape[:2]
        print(f"画像サイズ: {w} x {h}")
        print("抽出したい領域の座標を入力してください:")
        
        try:
            start_x = int(input("開始X座標: "))
            start_y = int(input("開始Y座標: "))
            end_x = int(input("終了X座標: "))
            end_y = int(input("終了Y座標: "))
            
            # 座標範囲チェック
            start_x = max(0, min(start_x, w))
            start_y = max(0, min(start_y, h))
            end_x = max(start_x, min(end_x, w))
            end_y = max(start_y, min(end_y, h))
            
            # 領域切り抜き
            pokemon_region = image[start_y:end_y, start_x:end_x]
            
            if pokemon_name:
                filename = f"{pokemon_name}_manual.png"
                output_path = self.output_dir / filename
                cv2.imwrite(str(output_path), pokemon_region)
                print(f"✅ 手動抽出完了: {filename}")
                return str(output_path)
                
            return pokemon_region
            
        except ValueError:
            print("❌ 無効な座標が入力されました")
            return None

def main():
    print("🎀✨ ポケモンZA 画像抽出ツール ✨🎀")
    print("="*50)
    
    extractor = PokemonExtractor()
    
    # 現在のディレクトリから画像ファイルを検索
    image_extensions = ['.png', '.jpg', '.jpeg', '.bmp']
    current_dir = Path('.')
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(current_dir.glob(f'*{ext}'))
        image_files.extend(current_dir.glob(f'*{ext.upper()}'))
    
    if not image_files:
        print("📁 現在のディレクトリに画像ファイルが見つかりません")
        image_path = input("画像ファイルのパスを入力してください: ")
        if not os.path.exists(image_path):
            print("❌ ファイルが存在しません")
            return
        image_files = [Path(image_path)]
    
    print(f"\n📸 見つかった画像ファイル: {len(image_files)}個")
    for i, img_file in enumerate(image_files):
        print(f"{i+1}. {img_file.name}")
    
    # 抽出方法選択
    print("\n🔧 抽出方法を選択してください:")
    print("1. 自動抽出（全手法を試行）")
    print("2. 色範囲指定")
    print("3. エッジ検出")
    print("4. 固定領域")
    print("5. 手動座標指定")
    
    try:
        method_choice = int(input("選択 (1-5): "))
        methods = ["auto", "color_range", "edge_detection", "fixed_region", "manual"]
        method = methods[method_choice - 1] if 1 <= method_choice <= 5 else "auto"
    except:
        method = "auto"
    
    # 画像ファイル選択
    if len(image_files) == 1:
        selected_file = image_files[0]
    else:
        try:
            file_choice = int(input(f"画像を選択 (1-{len(image_files)}): ")) - 1
            selected_file = image_files[file_choice] if 0 <= file_choice < len(image_files) else image_files[0]
        except:
            selected_file = image_files[0]
    
    print(f"\n🎯 処理開始: {selected_file.name}")
    
    # ポケモン名入力
    pokemon_name = input("ポケモン名を入力（空白で自動生成）: ").strip()
    if not pokemon_name:
        pokemon_name = selected_file.stem
    
    # 抽出実行
    result = extractor.extract_pokemon_from_pokedex(selected_file, pokemon_name, method)
    
    if result:
        if isinstance(result, list):
            print(f"\n🎉 抽出完了! {len(result)}個のファイルを生成しました:")
            for file_path in result:
                print(f"  📁 {file_path}")
        else:
            print(f"\n🎉 抽出完了! ファイル: {result}")
    else:
        print("\n❌ 抽出に失敗しました")

if __name__ == "__main__":
    main()