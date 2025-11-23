#!/usr/bin/env python3
import json

# 図鑑一覧を表示
with open('pokedex_structure.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("📖 現在の図鑑一覧:")
for k, v in data.items():
    print(f"ID {k}: {v['name']}")

print(f"\n総図鑑数: {len(data)}個")