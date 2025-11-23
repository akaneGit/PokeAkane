@echo off
REM PokeAkane 簡易起動バッチファイル
cd /d %~dp0

echo ? PokeAkane サーバー管理
echo.

:menu
echo 選択してください:
echo [1] サーバー起動
echo [2] サーバー停止  
echo [3] サーバー状態確認
echo [4] サーバー再起動
echo [5] ブラウザで開く
echo [6] 終了
echo.

set /p choice="番号を入力 (1-6): "

if "%choice%"=="1" (
    echo.
    python tools/server_manager.py start
    echo.
    pause
    goto menu
)

if "%choice%"=="2" (
    echo.
    python tools/server_manager.py stop
    echo.
    pause
    goto menu
)

if "%choice%"=="3" (
    echo.
    python tools/server_manager.py status
    echo.
    pause
    goto menu
)

if "%choice%"=="4" (
    echo.
    python tools/server_manager.py restart
    echo.
    pause
    goto menu
)

if "%choice%"=="5" (
    echo.
    python tools/server_manager.py open
    echo.
    pause
    goto menu
)

if "%choice%"=="6" (
    echo ? お疲れ様でした！
    exit /b
)

echo ? 無効な選択です
echo.
goto menu