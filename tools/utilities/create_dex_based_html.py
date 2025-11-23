#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
図鑑ベース構造用のHTMLギャラリー更新ツール
"""

import json

def create_updated_html():
    """新しい図鑑ベース構造に対応したHTMLを生成"""
    
    html_content = '''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ポケモンギャラリー - 図鑑ベース</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        
        .controls {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            border: 2px solid #e9ecef;
        }
        
        .dex-button {
            padding: 10px 15px;
            border: none;
            border-radius: 8px;
            background: linear-gradient(145deg, #6c5ce7, #a29bfe);
            color: white;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s ease;
            font-size: 12px;
            min-width: 120px;
            text-align: center;
        }
        
        .dex-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(108, 92, 231, 0.4);
            background: linear-gradient(145deg, #5f4bd1, #9187fc);
        }
        
        .dex-button.active {
            background: linear-gradient(145deg, #fd79a8, #fdcb6e);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(253, 121, 168, 0.4);
        }
        
        .info-panel {
            background: #e8f4fd;
            border: 2px solid #74b9ff;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .pokemon-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .pokemon-card {
            background: white;
            border-radius: 15px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            border: 2px solid #e9ecef;
        }
        
        .pokemon-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            border-color: #74b9ff;
        }
        
        .pokemon-image {
            width: 120px;
            height: 120px;
            object-fit: contain;
            margin-bottom: 10px;
            background: radial-gradient(circle, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 10px;
            padding: 10px;
        }
        
        .pokemon-name {
            font-weight: bold;
            color: #2d3436;
            margin-bottom: 5px;
            font-size: 16px;
        }
        
        .pokemon-number {
            color: #636e72;
            font-size: 14px;
            margin-bottom: 10px;
        }
        
        .pokemon-types {
            display: flex;
            justify-content: center;
            gap: 5px;
            flex-wrap: wrap;
        }
        
        .type-badge {
            padding: 4px 8px;
            border-radius: 15px;
            font-size: 12px;
            font-weight: bold;
            color: white;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }
        
        /* タイプ別の色 */
        .type-ノーマル { background: #A8A878; }
        .type-ほのお { background: #F08030; }
        .type-みず { background: #6890F0; }
        .type-でんき { background: #F8D030; }
        .type-くさ { background: #78C850; }
        .type-こおり { background: #98D8D8; }
        .type-かくとう { background: #C03028; }
        .type-どく { background: #A040A0; }
        .type-じめん { background: #E0C068; }
        .type-ひこう { background: #A890F0; }
        .type-エスパー { background: #F85888; }
        .type-むし { background: #A8B820; }
        .type-いわ { background: #B8A038; }
        .type-ゴースト { background: #705898; }
        .type-ドラゴン { background: #7038F8; }
        .type-あく { background: #705848; }
        .type-はがね { background: #B8B8D0; }
        .type-フェアリー { background: #EE99AC; }
        
        .loading {
            text-align: center;
            color: #666;
            font-style: italic;
            padding: 40px;
        }
        
        .error {
            background: #ffe0e0;
            border: 2px solid #ff6b6b;
            color: #d63031;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌟 ポケモンギャラリー - 図鑑ベース 🌟</h1>
        
        <div class="controls" id="dexButtons">
            <div class="loading">図鑑一覧を読み込み中...</div>
        </div>
        
        <div class="info-panel" id="infoPanel" style="display: none;">
            <strong id="selectedDexName">図鑑を選択してください</strong>
            <div id="pokemonCount"></div>
        </div>
        
        <div class="pokemon-grid" id="pokemonGrid">
            <div class="loading">図鑑を選択してポケモンを表示</div>
        </div>
    </div>

    <script>
        // グローバル変数
        let pokedexData = {};
        let pokemonData = {};
        let currentDex = null;
        
        // 初期化
        async function init() {
            try {
                await loadPokedexStructure();
                await loadPokemonData();
                createDexButtons();
            } catch (error) {
                console.error('初期化エラー:', error);
                showError('データの読み込みに失敗しました。');
            }
        }
        
        // 図鑑構造データを読み込み
        async function loadPokedexStructure() {
            try {
                const response = await fetch('pokedex_structure.json');
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                pokedexData = await response.json();
                console.log('図鑑構造データを読み込みました:', Object.keys(pokedexData).length, '個の図鑑');
            } catch (error) {
                console.error('図鑑構造データ読み込みエラー:', error);
                throw error;
            }
        }
        
        // ポケモンデータを読み込み
        async function loadPokemonData() {
            const generations = [1, 2, 3, 4, 5, 6, 7, 8, 9];
            
            for (const gen of generations) {
                try {
                    const response = await fetch(`gen${gen}_pokemon.json`);
                    if (response.ok) {
                        const genData = await response.json();
                        Object.assign(pokemonData, genData);
                        console.log(`第${gen}世代のデータを読み込みました:`, Object.keys(genData).length, '匹');
                    }
                } catch (error) {
                    console.warn(`第${gen}世代のデータ読み込みに失敗:`, error);
                }
            }
            
            console.log('総ポケモンデータ:', Object.keys(pokemonData).length, '匹');
        }
        
        // 図鑑ボタンを作成
        function createDexButtons() {
            const container = document.getElementById('dexButtons');
            container.innerHTML = '';
            
            // 図鑑IDでソート
            const sortedDexes = Object.values(pokedexData).sort((a, b) => a.id - b.id);
            
            sortedDexes.forEach(dex => {
                const button = document.createElement('button');
                button.className = 'dex-button';
                button.textContent = dex.name;
                button.onclick = () => selectDex(dex.id);
                button.dataset.dexId = dex.id;
                container.appendChild(button);
            });
        }
        
        // 図鑑を選択
        function selectDex(dexId) {
            currentDex = dexId;
            
            // ボタンの状態を更新
            document.querySelectorAll('.dex-button').forEach(btn => {
                btn.classList.remove('active');
            });
            document.querySelector(`[data-dex-id="${dexId}"]`).classList.add('active');
            
            // 図鑑情報を表示
            const dex = pokedexData[dexId];
            document.getElementById('selectedDexName').textContent = dex.name;
            document.getElementById('pokemonCount').textContent = `登録ポケモン数: ${Object.keys(dex.pokemon).length}匹`;
            document.getElementById('infoPanel').style.display = 'block';
            
            // ポケモンを表示
            displayPokemon(dex);
        }
        
        // ポケモンを表示
        function displayPokemon(dex) {
            const container = document.getElementById('pokemonGrid');
            container.innerHTML = '';
            
            // 図鑑番号順にソート
            const sortedPokemon = Object.entries(dex.pokemon).sort((a, b) => parseInt(a[0]) - parseInt(b[0]));
            
            sortedPokemon.forEach(([dexNumber, pokemonInfo]) => {
                const pokemon = pokemonData[pokemonInfo.pokemon_id];
                if (!pokemon) {
                    console.warn(`ポケモンデータが見つかりません: ID ${pokemonInfo.pokemon_id}`);
                    return;
                }
                
                const card = createPokemonCard(pokemon, dexNumber);
                container.appendChild(card);
            });
        }
        
        // ポケモンカードを作成
        function createPokemonCard(pokemon, dexNumber) {
            const card = document.createElement('div');
            card.className = 'pokemon-card';
            
            const imageUrl = `pokemon_images/normal/${pokemon.id}.png`;
            
            card.innerHTML = `
                <img src="${imageUrl}" alt="${pokemon.name}" class="pokemon-image" 
                     onerror="this.src='pokemon_images/normal/0.png'">
                <div class="pokemon-name">${pokemon.name}</div>
                <div class="pokemon-number">図鑑No. ${dexNumber} (全国No. ${pokemon.id})</div>
                <div class="pokemon-types">
                    ${pokemon.types.map(type => `<span class="type-badge type-${type}">${type}</span>`).join('')}
                </div>
            `;
            
            return card;
        }
        
        // エラー表示
        function showError(message) {
            const container = document.getElementById('pokemonGrid');
            container.innerHTML = `<div class="error">${message}</div>`;
        }
        
        // ページ読み込み時に初期化
        window.addEventListener('load', init);
    </script>
</body>
</html>'''

    with open("pokemon_gallery_dex_based.html", 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("図鑑ベース対応のHTMLファイルを作成しました: pokemon_gallery_dex_based.html")

if __name__ == "__main__":
    create_updated_html()