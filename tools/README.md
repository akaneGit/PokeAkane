# PokeAkane Tools Directory

このディレクトリには、PokeAkaneプロジェクトで使用される各種ツールスクリプトが含まれています。

## 📁 ディレクトリ構成

### 🔄 server_manager.py
- **機能**: PokeAkaneのHTTPサーバー管理
- **使用方法**: `python server_manager.py [start|stop|restart|status]`
- **説明**: ローカルサーバーの起動・停止・再起動・状態確認を行います

### 📥 downloaders/
画像やデータのダウンロードを行うスクリプト群

#### 地方別フォーム画像ダウンローダー
- `alolan_forms_redownloader.py` - アローラフォーム画像の一括再取得
- `galar_forms_redownloader.py` - ガラルフォーム画像の一括再取得  
- `hisui_forms_redownloader.py` - ヒスイフォーム画像の一括再取得

#### 特殊ポケモン対応ダウンローダー
- `darmanitan_complete_downloader.py` - ヒヒダルマ全フォーム対応
- `darmanitan_galar_correct_downloader.py` - ガラルヒヒダルマ正規URL対応
- `darmanitan_galar_redownloader.py` - ガラルヒヒダルマ再取得
- `darmanitan_zen_redownloader.py` - ヒヒダルマダルマモード取得
- `tauros_combat_downloader.py` - パルデアタウロス コンバット種取得
- `terapagos_stellar_downloader.py` - テラパゴス ステラフォーム取得

#### 汎用画像ダウンローダー
- `pokemon_image_downloader.py` - 基本ポケモン画像ダウンローダー
- `missing_forms_downloader.py` - 不足フォーム画像の一括取得
- `download_form_shinies.py` - フォーム色違い画像取得
- `type_icon_downloader.py` - タイプアイコンダウンローダー (v1)
- `type_icon_downloader_v2.py` - タイプアイコンダウンローダー (v2)

#### 探索・検証ツール
- `pokemondb_explorer.py` - PokemonDB探索ツール
- `retrieve_failed_forms.py` - 失敗したフォーム画像の再取得

### 🔄 data_processors/
データの処理・変換・更新を行うスクリプト群

#### データ収集・処理
- `pokemon_data_collector.py` - ポケモンデータ収集
- `pokemon_extractor.py` - ポケモンデータ抽出
- `data_splitter.py` - データ分割処理
- `evolution_data_fixer.py` - 進化データ修正

#### 図鑑番号・世代管理
- `game_dex_number_updater.py` - ゲーム内図鑑番号更新
- `generation_dex_updater.py` - 世代別図鑑更新
- `manual_dex_updater.py` - 手動図鑑更新
- `za_dex_updater.py` - ZA図鑑更新
- `accurate_za_updater.py` - 精密ZA更新

#### API・外部データ連携
- `pokeapi_collector.py` - PokeAPI データ収集
- `pokeapi_data_updater.py` - PokeAPI データ更新
- `za_data_collector.py` - ZAデータ収集

#### 地域特化処理
- `lumiose_dex_implementer.py` - ルミオース図鑑実装
- `correct_lumiose_implementer.py` - ルミオース図鑑修正実装
- `kitakami_blueberry_processor.py` - キタカミ・ブルーベリー処理
- `blueberry_pokemon_complete.py` - ブルーベリーポケモン完成処理

### 🛠️ utilities/
ユーティリティ・修正・生成ツール群

#### HTML・UI生成
- `create_dex_based_html.py` - 図鑑ベースHTML生成
- `create_pokedex_buttons.py` - 図鑑ボタン生成
- `region_icon_generator.py` - 地域アイコン生成

#### データ修正・検証
- `fix_nakanuchan_shiny.py` - ナカヌチャン色違い修正
- `fix_pokedex_ids.py` - 図鑑ID修正
- `check_dex_list.py` - 図鑑リスト確認
- `check_terapagos_images.py` - テラパゴス画像確認

#### 構造・管理
- `add_national_dex.py` - 全国図鑑追加
- `pokedex_list.py` - 図鑑リスト生成
- `restructure_to_dex_based.py` - 図鑑ベース構造変換

### 📦 archived/
使用されなくなった古いスクリプト（将来的な参考用）

### 🧪 temp_test/
テスト・実験用スクリプト（開発中・検証中のコード）

## 🚀 使用方法

### サーバー管理
```bash
# サーバー起動
python server_manager.py start

# サーバー停止  
python server_manager.py stop

# サーバー再起動
python server_manager.py restart

# サーバー状態確認
python server_manager.py status
```

### 画像ダウンロード
```bash
# 地方別フォーム画像を一括更新
python downloaders/alolan_forms_redownloader.py
python downloaders/galar_forms_redownloader.py
python downloaders/hisui_forms_redownloader.py

# 特定ポケモンの画像取得
python downloaders/tauros_combat_downloader.py
python downloaders/terapagos_stellar_downloader.py
```

### データ処理
```bash
# ポケモンデータの収集・更新
python data_processors/pokemon_data_collector.py
python data_processors/pokeapi_data_updater.py

# 図鑑番号の更新
python data_processors/game_dex_number_updater.py
```

### ユーティリティ
```bash
# データ検証
python utilities/check_dex_list.py
python utilities/check_terapagos_images.py

# HTML生成
python utilities/create_dex_based_html.py
```

## ⚠️ 注意事項

1. **依存関係**: 各スクリプトはrequests、PIL等の外部ライブラリを使用している場合があります
2. **実行順序**: データ処理系スクリプトは適切な順序で実行してください
3. **API制限**: PokemonDBやPokeAPI使用時はレート制限にご注意ください
4. **バックアップ**: 重要なデータ操作前は必ずバックアップを取ってください

## 📝 更新履歴

- 2025/11/13: ディレクトリ構造整理、機能別分類実施
- 2025/11/13: 地方別フォーム対応スクリプト群完成
- 2025/11/06-12: 各種データ処理・画像取得スクリプト開発
- 2025/10/27-31: 基本的な画像・データ収集ツール開発

---
*Last updated: 2025/11/13*