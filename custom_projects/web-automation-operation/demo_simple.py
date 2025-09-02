#!/usr/bin/env python3
# 簡化的 Chrome 啟動演示

import subprocess
import time
import os

def launch_chrome_simple(url="https://mail.google.com/mail/u/0/#inbox"):
    """
    簡化版本的 Chrome 啟動功能
    """
    print(f"🚀 正在啟動 Chrome 瀏覽器並導航到: {url}")
    
    # 嘗試啟動 Chrome
    chrome_command = [
        "chrome.exe",
        "--new-window",
        "--start-maximized", 
        url
    ]
    
    try:
        process = subprocess.Popen(chrome_command)
        print(f"✅ Chrome 已啟動，程序 PID: {process.pid}")
        time.sleep(3)
        return True
        
    except FileNotFoundError:
        # 嘗試常見的 Chrome 路徑
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
        
        for chrome_path in chrome_paths:
            if os.path.exists(chrome_path):
                print(f"🔍 在 {chrome_path} 找到 Chrome")
                chrome_command[0] = chrome_path
                try:
                    process = subprocess.Popen(chrome_command)
                    print(f"✅ Chrome 已啟動，程序 PID: {process.pid}")
                    time.sleep(3)
                    return True
                except Exception as e:
                    print(f"❌ 使用路徑 {chrome_path} 啟動失敗: {e}")
                    continue
        
        # 最後嘗試使用 start 命令
        try:
            start_command = f'start chrome "{url}"'
            os.system(start_command)
            print("✅ 使用 Windows start 命令啟動 Chrome")
            time.sleep(3)
            return True
        except Exception as e:
            print(f"❌ 所有啟動方法都失敗: {e}")
            return False

if __name__ == "__main__":
    print("=== 簡化 Chrome 啟動演示 ===")
    print("此演示將啟動 Chrome 瀏覽器並開啟 Gmail")
    print("-" * 50)
    
    success = launch_chrome_simple()
    
    if success:
        print("\n✅ Chrome 瀏覽器啟動成功！")
        print("💡 Chrome 應該已經開啟並顯示 Gmail 收件箱")
        print("📝 這是不使用 UFO2 AI 功能的基本版本")
    else:
        print("\n❌ Chrome 瀏覽器啟動失敗")
        print("請確認：")
        print("1. Chrome 瀏覽器已正確安裝")
        print("2. 沒有防火牆阻擋")
        print("3. 系統權限充足")
