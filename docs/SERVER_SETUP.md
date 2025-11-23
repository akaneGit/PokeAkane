# PokeAkane 簡易起動用README

## 🚀 簡単な起動方法

### 1. バッチファイルで起動（Windows）
```
server.bat
```
メニュー形式で起動・停止・状態確認ができます

### 2. コマンドラインで起動
```bash
# サーバー起動
python tools/server_manager.py start

# サーバー停止  
python tools/server_manager.py stop

# 状態確認
python tools/server_manager.py status

# 再起動
python tools/server_manager.py restart

# ブラウザで開く
python tools/server_manager.py open
```

### 3. 従来の方法
```bash
python -m http.server 8000
```

## 📍 アクセス
サーバー起動後、以下のURLでアクセス:
```
http://localhost:8000/pokemon_gallery.html
```

## 💡 便利な機能
- PIDファイルによる適切なサーバー管理
- ポート使用状況の自動チェック
- ブラウザ自動起動
- 穏やかな終了（Ctrl+Cより安全）