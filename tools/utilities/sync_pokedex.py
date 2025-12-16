#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
図鑑内容同期ツール
- ある図鑑(ID)の pokemon エントリを別IDへコピーします

使い方:
  python tools/utilities/sync_pokedex.py --from 1 --to 4
"""

import json
from pathlib import Path
import argparse

ROOT = Path(__file__).resolve().parents[2]
STRUCT_DIR = ROOT / 'data' / 'pokedex_structures'

def load_dex(dex_id: int):
    p = STRUCT_DIR / f'{dex_id}.json'
    if not p.exists():
        raise FileNotFoundError(f'{p} が見つかりません')
    return p, json.loads(p.read_text(encoding='utf-8'))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--from', dest='src', type=int, required=True)
    ap.add_argument('--to', dest='dst', type=int, required=True)
    args = ap.parse_args()

    src_path, src = load_dex(args.src)
    dst_path, dst = load_dex(args.dst)

    dst['pokemon'] = src.get('pokemon', {})

    dst_path.write_text(json.dumps(dst, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"図鑑 {args.src} -> {args.dst} の pokemon を同期しました: {dst_path}")

if __name__ == '__main__':
    main()
