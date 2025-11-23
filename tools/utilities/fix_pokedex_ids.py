import json

# 現在のpokedex_hierarchy.jsonからIDマッピングを取得
with open('data/pokedex_hierarchy.json', 'r', encoding='utf-8') as f:
    hierarchy = json.load(f)

# pokedex_structure.jsonを読み込み
with open('data/pokedex_structure.json', 'r', encoding='utf-8') as f:
    structure = json.load(f)

# 新しいIDマッピングを作成
new_structure = {}

# hierarchy.jsonからIDマッピングを取得
id_mapping = {}
for category in hierarchy['categories']:
    for sub in category['subcategories']:
        pokedex_id = sub['pokedex_id']
        name = sub['name']
        id_mapping[pokedex_id] = name

for special in hierarchy['special_categories']:
    for sub in special['subcategories']:
        pokedex_id = sub['pokedex_id']
        name = sub['name']
        id_mapping[pokedex_id] = name

print("新しいIDマッピング:")
for pid, name in sorted(id_mapping.items()):
    print(f"ID {pid}: {name}")

# 既存のstructure.jsonから対応するデータを見つけて新しいIDに配置
old_to_new_mapping = {
    # 現在のstructure.jsonのID : 新しいID
    0: 0,   # 全国図鑑（全ポケモン）
    1: 1,   # カントー図鑑（赤緑青ピカ）
    2: 2,   # ジョウト図鑑（金銀クリスタル）
    3: 3,   # ホウエン図鑑（RSE）
    4: 4,   # カントー図鑑（FRLG）
    5: 5,   # シンオウ図鑑（DPPt）
    6: 6,   # ジョウト図鑑（HGSS）
    7: 7,   # イッシュ図鑑（BW）
    8: 8,   # イッシュ図鑑（BW2）
    9: 9,   # セントラルカロス図鑑（XY）
    10: 12,  # ホウエン図鑑（ORAS） -> 新ID 12
    11: 13,  # アローラ図鑑（SM） -> 新ID 13
    12: 14,  # アローラ図鑑（USUM） -> 新ID 14
    13: 15,  # カントー図鑑（Let's Go!） -> 新ID 15
    14: 16,  # ガラル図鑑（SwSh） -> 新ID 16
    15: 17,  # シンオウ図鑑（BDSP） -> 新ID 17
    16: 18,  # ヒスイ図鑑（PLA） -> 新ID 18
    17: 19,  # パルデア図鑑（SV） -> 新ID 19
    20: 20,  # キタカミ図鑑
    21: 21,  # ブルーベリー図鑑
    34: 22,  # ミアレシティ図鑑（Z-A） -> 新ID 22
}

# 新しいstructureを構築
for old_id, new_id in old_to_new_mapping.items():
    old_id_str = str(old_id)
    new_id_str = str(new_id)
    
    if old_id_str in structure:
        new_structure[new_id_str] = structure[old_id_str].copy()
        new_structure[new_id_str]['id'] = new_id
        print(f"移動: {old_id} -> {new_id}")

# 新しいカロス図鑑（ID 10, 11）を追加
new_structure['10'] = {
    "id": 10,
    "name": "コーストカロス図鑑（X・Y）",
    "key": "xy_coastal",
    "pokemon": {
        "1": {"pokemon_id": 425, "name": "ドリフロン", "name_en": "drifloon"},
        "2": {"pokemon_id": 426, "name": "ドリフゴン", "name_en": "drifblim"},
        "3": {"pokemon_id": 619, "name": "ココロモリ", "name_en": "mienfoo"},
        "4": {"pokemon_id": 620, "name": "コジョンド", "name_en": "mienshao"},
        "5": {"pokemon_id": 335, "name": "ザングース", "name_en": "zangoose"},
        "153": {"pokemon_id": 146, "name": "ファイヤー", "name_en": "moltres"}
    }
}

new_structure['11'] = {
    "id": 11,
    "name": "マウンテンカロス図鑑（X・Y）",
    "key": "xy_mountain",
    "pokemon": {
        "1": {"pokemon_id": 50, "name": "ディグダ", "name_en": "diglett"},
        "2": {"pokemon_id": 51, "name": "ダグトリオ", "name_en": "dugtrio"},
        "3": {"pokemon_id": 328, "name": "ナックラー", "name_en": "trapinch"},
        "4": {"pokemon_id": 329, "name": "ビブラーバ", "name_en": "vibrava"},
        "5": {"pokemon_id": 330, "name": "フライゴン", "name_en": "flygon"},
        "151": {"pokemon_id": 150, "name": "ミュウツー", "name_en": "mewtwo"}
    }
}

# 新しいstructure.jsonを保存
with open('data/pokedex_structure_new.json', 'w', encoding='utf-8') as f:
    json.dump(new_structure, f, ensure_ascii=False, indent=2)

print("新しいpokedex_structure_new.jsonを作成しました")
print(f"図鑑数: {len(new_structure)}")