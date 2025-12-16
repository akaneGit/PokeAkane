#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FRLG 図鑑の全国図鑑追加分を反映するツール
- 参照: https://way78.com/gba/2004/pokemon2/poke07.html の一覧
- data/pokedex_structures/4.json に、既存151種の後へ追記します
- タグや版別情報は付与しません（名称は既存世代JSONから取得）
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STRUCT = ROOT / 'data' / 'pokedex_structures' / '4.json'
GEN_DIR = ROOT / 'data'

# 追加対象の全国図鑑ID一覧（重複は自動スキップ）
EXTRA_IDS = [
    161,162,165,166,167,168,169,172,173,174,175,176,177,178,182,
    183,184,186,187,188,189,193,194,195,198,199,200,201,202,206,
    208,211,212,214,215,218,219,220,221,223,224,225,226,227,230,
    231,232,233,236,237,238,239,240,242,243,244,245,246,247,248,
    249,250,386,
    298,360
]

def load_all_pokemon():
    """gen1-9 の JSON から {id: {name, name_en}} を作る"""
    data = {}
    for gen in range(1, 10):
        p = GEN_DIR / f'gen{gen}_pokemon.json'
        if not p.exists():
            continue
        doc = json.loads(p.read_text(encoding='utf-8'))
        for pid_str, info in doc.items():
            pid = int(pid_str)
            data[pid] = {
                'name': info.get('name'),
                'name_en': info.get('name_en')
            }
    return data

def main():
    if not STRUCT.exists():
        raise FileNotFoundError(f'FRLG 図鑑が見つかりません: {STRUCT}')
    dex = json.loads(STRUCT.read_text(encoding='utf-8'))

    all_poke = load_all_pokemon()
    pokemon = dex.get('pokemon', {})

    # 既存の図鑑番号の最大値を把握し、続き番号で追記
    existing_numbers = [int(k) for k in pokemon.keys()] if pokemon else []
    next_number = (max(existing_numbers) + 1) if existing_numbers else 1

    # 既に含まれている全国IDを集合で把握
    existing_ids = {int(v.get('pokemon_id')) for v in pokemon.values()} if pokemon else set()

    added = 0
    for pid in EXTRA_IDS:
        if pid in existing_ids:
            continue
        meta = all_poke.get(pid)
        if not meta:
            # 名前が取得できない場合でも最低限の構造で追加
            meta = {'name': f'ID{pid}', 'name_en': None}
        pokemon[str(next_number)] = {
            'pokemon_id': pid,
            'name': meta['name'],
            'name_en': meta['name_en']
        }
        next_number += 1
        added += 1

    dex['pokemon'] = pokemon
    STRUCT.write_text(json.dumps(dex, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'FRLG 図鑑に {added} 件を追記しました: {STRUCT}')

if __name__ == '__main__':
    main()
