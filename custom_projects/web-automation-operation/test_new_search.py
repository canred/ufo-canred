#!/usr/bin/env python3
"""
Gmail 搜尋輸入框測試 - 專門測試新的搜尋方法
"""
import time
import subprocess
import os

def test_gmail_search_input():
    """測試 Gmail 搜尋輸入框的新方法"""
    print("🔍 === Gmail 搜尋輸入框測試 ===")
    
    try:
        # 1. 啟動 Chrome 到 Gmail
        print("🚀 步驟 1: 啟動 Chrome 到 Gmail...")
        gmail_url = "https://mail.google.com/mail/u/0/#inbox"
        
        start_command = f'start chrome "{gmail_url}"'
        os.system(start_command)
        
        print("✅ Chrome 已啟動")
        
        # 2. 等待 Gmail 載入
        print("⏳ 步驟 2: 等待 Gmail 載入...")
        for i in range(8, 0, -1):
            print(f"   倒數 {i} 秒...")
            time.sleep(1)
        
        # 3. 測試新的搜尋方法
        print("🔍 步驟 3: 測試尋找「搜尋郵件」輸入框...")
        
        try:
            import pyautogui
            import pyperclip
            
            # 獲取螢幕尺寸
            screen_width, screen_height = pyautogui.size()
            print(f"📺 螢幕尺寸: {screen_width} x {screen_height}")
            
            # 方法1: 點擊頂部中央的搜尋區域
            search_x = screen_width // 2
            search_y = 100
            
            print(f"🖱️  方法1: 點擊搜尋區域 ({search_x}, {search_y})")
            pyautogui.click(search_x, search_y)
            time.sleep(1)
            
            # 方法2: 使用 Gmail 搜尋快捷鍵
            print("⌨️  方法2: 使用 Gmail 搜尋快捷鍵 Ctrl+K")
            pyautogui.hotkey('ctrl', 'k')
            time.sleep(1)
            
            # 方法3: 使用 / 鍵
            print("⌨️  方法3: 使用 / 鍵啟動搜尋")
            pyautogui.press('/')
            time.sleep(1)
            
            # 清空並輸入搜尋關鍵字
            print("📝 清空搜尋框並輸入關鍵字...")
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.3)
            
            # 輸入搜尋關鍵字
            search_keyword = "多結果子"
            print(f"⌨️  輸入關鍵字: '{search_keyword}'")
            pyperclip.copy(search_keyword)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.5)
            
            # 按 Enter 執行搜尋
            print("🔎 按 Enter 執行搜尋...")
            pyautogui.press('enter')
            time.sleep(4)
            
            # 選取搜尋結果
            print("✅ 選取搜尋結果...")
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(1)
            
            # 嘗試全選
            try:
                pyautogui.hotkey('ctrl', 'shift', 'a')
                print("📬 已嘗試全選所有搜尋結果")
            except:
                pass
            
            print("🎉 搜尋和選取流程完成！")
            print("💡 請檢查 Gmail 中是否已正確搜尋並選取包含 '多結果子' 的信件")
            
        except ImportError:
            print("⚠️ pyautogui 或 pyperclip 未安裝")
            print("💡 請手動在 Gmail 搜尋框中輸入 '多結果子' 並選取結果")
        
        return True
        
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        return False

if __name__ == "__main__":
    success = test_gmail_search_input()
    
    if success:
        print("\n✅ Gmail 搜尋輸入框測試完成！")
    else:
        print("\n❌ 測試過程遇到問題")
    
    print("\n📋 操作結果檢查:")
    print("1. Chrome 是否已開啟 Gmail？")
    print("2. Gmail 搜尋框是否已聚焦？")
    print("3. 是否已輸入 '多結果子' 關鍵字？")
    print("4. 搜尋結果是否正確顯示？")
    print("5. 相關信件是否已被選取？")
    
    input("\n按 Enter 鍵結束測試...")
