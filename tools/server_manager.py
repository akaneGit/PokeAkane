#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PokeAkane 簡易サーバー管理ツール
サーバーの起動・停止・状態確認を簡単に行えます
"""

import subprocess
import sys
import time
import signal
import os
import socket
import psutil
from pathlib import Path

class PokeAkaneServer:
    def __init__(self, port=8000):
        self.port = port
        self.project_root = Path(__file__).parent.parent
        self.pid_file = self.project_root / ".server.pid"
        
    def is_port_in_use(self):
        """ポートが使用中かチェック (実接続で確認)"""
        try:
            with socket.create_connection(("127.0.0.1", self.port), timeout=0.3):
                return True
        except OSError:
            return False
    
    def get_server_pid(self):
        """サーバーのPIDを取得"""
        if self.pid_file.exists():
            try:
                with open(self.pid_file, 'r') as f:
                    pid = int(f.read().strip())
                # PIDが実際に存在するかチェック
                if psutil.pid_exists(pid):
                    process = psutil.Process(pid)
                    # python http.serverプロセスかチェック
                    if 'python' in process.name().lower() and str(self.port) in ' '.join(process.cmdline()):
                        return pid
            except:
                pass
        return None
    
    def start_server(self):
        """サーバー起動"""
        print(f"■ PokeAkane サーバー起動中... (ポート:{self.port})")
        
        # 既に起動チェック
        if self.is_port_in_use():
            print(f"??  ポート {self.port} は既に使用中です")
            existing_pid = self.get_server_pid()
            if existing_pid:
                print(f"? PID {existing_pid} でサーバーが動作中です")
                print(f"? http://localhost:{self.port}/pokemon_gallery.html でアクセス可能")
            return False
        
        try:
            # サーバー起動（標準入出力を親コンソールに委譲）
            cmd = [
                sys.executable, '-m', 'http.server', str(self.port),
                '--bind', '127.0.0.1',
                '--directory', str(self.project_root)
            ]

            process = subprocess.Popen(
                cmd,
                cwd=self.project_root,
                stdout=None,
                stderr=None,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
            )

            # 起動確認（最大5秒間ポート疎通を待つ）
            start = time.time()
            while time.time() - start < 5:
                if self.is_port_in_use():
                    # PIDファイル保存（起動確認後に書く）
                    with open(self.pid_file, 'w') as f:
                        f.write(str(process.pid))

                    print(f"■ サーバー起動成功！")
                    print(f"■ PID: {process.pid}")
                    print(f"■ アクセス: http://localhost:{self.port}/pokemon_gallery.html")
                    print(f"■ 停止方法: python tools/server_manager.py stop")
                    return True
                # 途中で異常終了していないか確認
                if process.poll() is not None:
                    break
                time.sleep(0.2)

            print(f"■ サーバー起動失敗（ポートが開きませんでした）")
            # 念のためプロセスが生存していれば終了
            try:
                if process.poll() is None:
                    process.terminate()
            except Exception:
                pass
            return False

        except Exception as e:
            print(f"■ エラー: {e}")
            return False
    
    def stop_server(self):
        """サーバー停止"""
        print(f"? サーバー停止中...")
        
        pid = self.get_server_pid()
        if not pid:
            print("??  実行中のサーバーが見つかりません")
            # PIDファイルがあるが無効なら削除
            if self.pid_file.exists():
                self.pid_file.unlink()
            return False
        
        try:
            process = psutil.Process(pid)
            process.terminate()  # 穏やかに終了
            
            # 終了待機
            try:
                process.wait(timeout=5)
            except psutil.TimeoutExpired:
                process.kill()  # 強制終了
            
            # PIDファイル削除
            if self.pid_file.exists():
                self.pid_file.unlink()
            
            print(f"? サーバー停止完了 (PID: {pid})")
            return True
            
        except Exception as e:
            print(f"? エラー: {e}")
            return False
    
    def status(self):
        """サーバー状態確認"""
        print(f"■ PokeAkane サーバー状態")
        print(f"   ポート: {self.port}")
        
        pid = self.get_server_pid()
        if pid:
            print(f"   状態: ■ 実行中 (PID: {pid})")
            print(f"   URL: http://localhost:{self.port}/pokemon_gallery.html")
        else:
            # PIDがなくてもポートが開いている可能性を表示
            if self.is_port_in_use():
                print(f"   状態: ▲ 稼働中（PID不明・外部起動の可能性）")
                print(f"   URL: http://localhost:{self.port}/pokemon_gallery.html")
            else:
                print(f"   状態: ■ 停止中")
            
        return pid is not None
    
    def restart_server(self):
        """サーバー再起動"""
        print("? サーバー再起動中...")
        self.stop_server()
        time.sleep(1)
        return self.start_server()
    
    def open_browser(self):
        """ブラウザでサイトを開く"""
        if not self.status():
            print("??  サーバーが起動していません。まずサーバーを起動してください。")
            return False
        
        import webbrowser
        url = f"http://localhost:{self.port}/pokemon_gallery.html"
        print(f"? ブラウザでサイトを開いています: {url}")
        webbrowser.open(url)
        return True

def main():
    """メイン実行"""
    server = PokeAkaneServer()
    
    if len(sys.argv) < 2:
        print("? PokeAkane サーバー管理ツール")
        print("\n使用方法:")
        print("  python tools/server_manager.py start   - サーバー起動")
        print("  python tools/server_manager.py stop    - サーバー停止") 
        print("  python tools/server_manager.py status  - 状態確認")
        print("  python tools/server_manager.py restart - 再起動")
        print("  python tools/server_manager.py open    - ブラウザで開く")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'start':
        server.start_server()
    elif command == 'stop':
        server.stop_server()
    elif command == 'status':
        server.status()
    elif command == 'restart':
        server.restart_server()
    elif command == 'open':
        server.open_browser()
    else:
        print(f"? 不明なコマンド: {command}")
        print("利用可能: start, stop, status, restart, open")

if __name__ == "__main__":
    main()