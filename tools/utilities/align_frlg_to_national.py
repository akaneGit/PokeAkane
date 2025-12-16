#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FRLG 図鑑(4.json)の図鑑番号を全国図鑑(0.json)の番号に揃えるツール

処理概要:
- data/pokedex_structures/0.json を読み込み、全国図鑑番号 -> pokemon_id の対応表を作る
- data/pokedex_structures/4.json の pokemon を走査し、各 pokemon_id に対応する全国図鑑番号をキーとして再構築
- 全国図鑑に存在しない pokemon_id は末尾に連番で付与（安全策）
- 既存の name/name_en を保持しつつ、必要なら全国側の名前で補完
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STRUCT_DIR = ROOT / 'data' / 'pokedex_structures'

NATIONAL = STRUCT_DIR / '0.json'
FRLG = STRUCT_DIR / '4.json'

def load_json(path: Path):
    if not path.exists():
        raise FileNotFoundError(str(path))
    return json.loads(path.read_text(encoding='utf-8'))

def main():
    nat = load_json(NATIONAL)
    frlg = load_json(FRLG)

    nat_map_pid_to_natnum = {}
    for nat_num_str, entry in nat.get('pokemon', {}).items():
        nat_num = int(nat_num_str)
        pid = int(entry.get('pokemon_id'))
        nat_map_pid_to_natnum[pid] = nat_num

    new_pokemon = {}
    fallback_start = max(nat_map_pid_to_natnum.values()) + 1 if nat_map_pid_to_natnum else 1

    # 既存FRLGの各エントリを全国図鑑番号に再配置
    for _, entry in frlg.get('pokemon', {}).items():
        pid = int(entry.get('pokemon_id'))
        nat_num = nat_map_pid_to_natnum.get(pid)
        if nat_num is None:
            # 全国側にないIDは末尾に追加（念のため）
            while str(fallback_start) in new_pokemon:
                fallback_start += 1
            target_key = str(fallback_start)
            fallback_start += 1
        else:
            target_key = str(nat_num)

        # 名前はFRLG側を優先し、無い場合は全国側で補完
        name = entry.get('name')
        name_en = entry.get('name_en')
        if (not name or not name_en) and nat_num is not None:
            nat_entry = nat['pokemon'].get(str(nat_num), {})
            name = name or nat_entry.get('name')
            name_en = name_en or nat_entry.get('name_en')

        new_pokemon[target_key] = {
            'pokemon_id': pid,
            'name': name,
            'name_en': name_en
        }

    # キーを数値昇順で並べ替え
    ordered = {k: new_pokemon[k] for k in sorted(new_pokemon.keys(), key=lambda s: int(s))}
    frlg['pokemon'] = ordered

    FRLG.write_text(json.dumps(frlg, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"FRLG(4.json) の図鑑番号を全国(0.json)に揃えました: {FRLG}")

if __name__ == '__main__':
    main()
