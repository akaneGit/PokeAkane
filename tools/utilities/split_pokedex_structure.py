#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PokeAkane 図鑑構造分割ツール
- data/pokedex_structure.json を図鑑ごとに分割して data/pokedex_structures/ に書き出します
- 出力ファイル名: {id}.json （内容はその図鑑オブジェクト1つのみ）

使い方:
  python tools/utilities/split_pokedex_structure.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'data' / 'pokedex_structure.json'
OUT_DIR = ROOT / 'data' / 'pokedex_structures'

def main():
    if not SRC.exists():
        raise FileNotFoundError(f"構造ファイルが見つかりません: {SRC}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    data = json.loads(SRC.read_text(encoding='utf-8'))

    count = 0
    for key, dex in data.items():
        try:
            dex_id = int(dex.get('id', key))
        except Exception:
            # キーが数値文字列である前提
            dex_id = int(key)

        # 単一図鑑オブジェクトとして保存
        out_path = OUT_DIR / f"{dex_id}.json"
        out_path.write_text(json.dumps(dex, ensure_ascii=False, indent=2), encoding='utf-8')
        count += 1

    print(f"{count} 個の図鑑を {OUT_DIR} に書き出しました")

if __name__ == '__main__':
    main()
