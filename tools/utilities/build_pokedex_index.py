#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
図鑑インデックス生成ツール
- data/pokedex_structures/*.json を走査して、{id, name, key} の軽量インデックスを生成
- 出力: data/pokedex_index.json

使い方:
  python tools/utilities/build_pokedex_index.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STRUCT_DIR = ROOT / 'data' / 'pokedex_structures'
OUT = ROOT / 'data' / 'pokedex_index.json'

def main():
    if not STRUCT_DIR.exists():
        raise FileNotFoundError(f"図鑑構造フォルダがありません: {STRUCT_DIR}")

    index = {}
    for p in sorted(STRUCT_DIR.glob('*.json')):
        try:
            dex = json.loads(p.read_text(encoding='utf-8'))
            dex_id = int(dex.get('id'))
            index[str(dex_id)] = {
                'id': dex_id,
                'name': dex.get('name'),
                'key': dex.get('key')
            }
        except Exception as e:
            print(f"警告: {p.name} の読み取りに失敗: {e}")

    OUT.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"図鑑インデックスを生成しました: {OUT} ({len(index)}件)")

if __name__ == '__main__':
    main()
