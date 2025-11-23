# 開発者ドキュメント - PokeAkane

## 🔧 技術アーキテクチャ

### **フロントエンド構成**
```
pokemon_gallery.html          # メインアプリケーション
├─ CSS                        # モダンUI（Grid + Flexbox）
├─ JavaScript                 # バニラJS（ES6+）
└─ 外部ライブラリ               # なし（完全自己完結）
```

### **データ構造**
```
📊 Pokemon Data Structure
{
  "id": 1,
  "name": "フシギダネ",
  "name_en": "Bulbasaur",
  "types": ["grass", "poison"],
  "stats": {
    "hp": 45, "attack": 49, "defense": 49,
    "sp_attack": 65, "sp_defense": 65, "speed": 45
  },
  "evolution": {...},
  "dex_entries": [...],
  "height": 0.7, "weight": 6.9,
  "generation": 1
}
```

### **画像管理システム**
```
🖼️ Image Organization
pokemon_images/
├─ normal/                    # 基本フォルム（1025体）
│  └─ {id:03d}.png           # 例: 001.png, 025.png
├─ forms/                     # 地方フォルム（118画像）
│  └─ {id}_{form_name}.png   # 例: 026_raichu-alola.png
├─ patterns/                  # パターン違い（231画像）
│  └─ {id}_{pattern}.png     # 例: 666_vivillon_elegant.png
├─ shinies/                   # 色違い（1025画像）
│  └─ {id:03d}_shiny.png     # 例: 001_shiny.png
├─ gender_differences/        # 性別差
└─ mega_evolutions/          # メガシンカ
```

## 🛠️ 開発環境構築

### **必須要件**
```bash
# Python 3.8+
python --version

# 推奨：仮想環境
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 依存関係インストール
pip install requests pillow beautifulsoup4
```

### **開発サーバー起動**
```bash
# 簡単起動（推奨）
python tools/server_manager.py start

# 従来方法
python -m http.server 8000

# Windows バッチファイル
server.bat
```

### **ローカル開発URL**
```
メイン図鑑: http://localhost:8000/pokemon_gallery.html
タイプ相性: http://localhost:8000/type_chart.html
性格表:    http://localhost:8000/nature_chart.html
```

## 🧩 コードベース構造

### **主要コンポーネント**

#### **1. フォルム検出システム**
```javascript
// pokemon_gallery.html 内
function detectAvailableForms(pokemonId) {
  const forms = [
    { type: 'normal', path: `pokemon_images/normal/${pokemonId:03d}.png` },
    { type: 'shiny', path: `pokemon_images/shinies/${pokemonId:03d}_shiny.png` },
    // 他フォルム検出ロジック
  ];
  return forms.filter(form => imageExists(form.path));
}
```

#### **2. 検索・フィルターエンジン**
```javascript
function filterPokemon() {
  const searchTerm = searchInput.value.toLowerCase();
  const selectedTypes = getSelectedTypes();
  const evolutionStage = getEvolutionFilter();
  
  return pokemonData.filter(pokemon => {
    return matchesSearch(pokemon, searchTerm) &&
           matchesTypes(pokemon, selectedTypes) &&
           matchesEvolution(pokemon, evolutionStage);
  });
}
```

#### **3. 動的図鑑切り替え**
```javascript
function switchPokedex(dexName) {
  const dexData = pokedexStructure[dexName];
  const filteredPokemon = pokemonData.filter(pokemon => 
    dexData.pokemon_ids.includes(pokemon.id)
  );
  renderPokemonGrid(filteredPokemon);
}
```

### **データ処理フロー**
```
1. JSON読み込み → 2. データ統合 → 3. 検索インデックス構築
     ↓                ↓                ↓
4. UI初期化 → 5. イベントリスナー → 6. リアルタイム更新
```

## 🔄 開発ツール詳細

### **ダウンローダー系（tools/downloaders/）**
```python
# 主要ダウンローダー
pokemon_image_downloader.py      # 基本ポケモン画像
alolan_forms_redownloader.py     # アローラフォルム
galar_forms_redownloader.py      # ガラルフォルム
hisui_forms_redownloader.py      # ヒスイフォルム
missing_forms_downloader.py      # 不足フォルム補完
```

### **データプロセッサー系（tools/data_processors/）**
```python
# 主要プロセッサー
pokeapi_collector.py             # PokeAPIデータ収集
pokemon_data_collector.py        # データ統合処理
evolution_data_fixer.py          # 進化データ修正
za_data_collector.py             # ZAデータ処理
```

### **ユーティリティ系（tools/utilities/）**
```python
# 便利ツール
create_dex_based_html.py         # HTML生成
pokedex_list.py                  # 図鑑一覧作成
region_icon_generator.py         # 地方アイコン生成
check_terapagos_images.py        # 画像チェック
```

## 📊 データ管理

### **JSONファイル構造**
```
data/
├─ gen{N}_pokemon.json          # 世代別データ（9ファイル）
├─ pokedex_structure.json       # 34図鑑構造
├─ pokedex_button_data.json     # UI用図鑑データ
└─ pokedex_hierarchy.json       # 図鑑階層構造
```

### **データ更新フロー**
```bash
# 1. APIデータ取得
python tools/data_processors/pokeapi_collector.py

# 2. データ統合
python tools/data_processors/pokemon_data_collector.py

# 3. 図鑑構造更新
python tools/utilities/create_pokedex_buttons.py

# 4. 不足データ補完
python tools/data_processors/za_data_collector.py
```

## 🧪 テスト・品質管理

### **画像検証**
```python
# 画像存在チェック
python tools/utilities/check_terapagos_images.py

# フォルム画像確認
python tools/downloaders/retrieve_failed_forms.py
```

### **データ検証**
```python
# 図鑑ID確認
python tools/utilities/check_dex_list.py

# 進化データチェック
python tools/data_processors/evolution_data_fixer.py
```

### **パフォーマンス最適化**
- **画像遅延読み込み**: Intersection Observer API使用
- **検索最適化**: デバウンス処理（300ms）
- **メモリ管理**: 大量データのページネーション考慮

## 🚀 デプロイ・配布

### **静的サイト配布**
```bash
# ビルド不要（静的ファイル）
# 必要ファイル：
pokemon_gallery.html
type_chart.html
nature_chart.html
data/
pokemon_images/
type_images/
region_icons/
```

### **GitHub Pages対応**
```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages
on:
  push:
    branches: [ main ]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./
```

## 🐛 トラブルシューティング

### **よくある問題**

#### **画像が表示されない**
```javascript
// 解決方法: パス確認
console.log("画像パス:", imagePath);
console.log("画像存在:", await fetch(imagePath).then(r => r.ok));
```

#### **検索が動作しない**
```javascript
// 解決方法: データ読み込み確認
console.log("ポケモンデータ:", pokemonData.length);
console.log("検索文字列:", searchTerm);
```

#### **フォルム切り替えが効かない**
```javascript
// 解決方法: フォルム検出ログ
console.log("検出フォルム:", detectAvailableForms(pokemonId));
```

### **パフォーマンス問題**
```javascript
// 大量データ対策
const ITEMS_PER_PAGE = 30;
const virtualScrolling = true;
const imageLoadingStrategy = 'lazy';
```

## 🤝 コントリビューションガイド

### **コード規約**
- **JavaScript**: ES6+ 構文使用
- **CSS**: CSS Grid + Flexbox
- **Python**: PEP 8 準拠
- **命名**: camelCase（JS）、snake_case（Python）

### **プルリクエストガイドライン**
1. **機能ブランチ**作成
2. **テスト実行**（画像・データ検証）
3. **ドキュメント更新**
4. **レビュー依頼**

### **イシュー報告**
- **バグ報告**: 環境・再現手順・期待結果
- **機能要望**: ユースケース・実装案
- **パフォーマンス**: 計測データ・改善案

---

## 🎯 今後の開発ロードマップ

### **Phase 1: UI/UX改善**
- [ ] ダークモード対応
- [ ] アニメーション効果追加
- [ ] PWA化

### **Phase 2: 機能拡張**
- [ ] ポケモン比較機能
- [ ] お気に入り機能（localStorage）
- [ ] 統計情報表示

### **Phase 3: データ拡張**
- [ ] 技データ連携
- [ ] 特性詳細情報
- [ ] 生息地情報

---

最終更新: 2025年11月13日  
メンテナー: PokeAkane開発チーム