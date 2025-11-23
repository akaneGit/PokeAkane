import requests
import json

# PokeAPIから図鑑リストを取得
response = requests.get('https://pokeapi.co/api/v2/pokedex/?limit=33')
data = response.json()

print('📋 PokeAPI 図鑑リスト (33個):\n')
for i, result in enumerate(data['results']):
    print(f'{i+1:2d}. {result["name"]}')

print(f'\n合計: {data["count"]}個の図鑑')