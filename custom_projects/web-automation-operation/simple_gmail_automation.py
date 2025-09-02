#!/usr/bin/env python3
"""
簡化版 Chrome Gmail 自動化 - 專注於搜尋功能
不依賴 UFO2 的 LLM API，純粹使用自動化操作
"""

import os
import sys
import time
import subprocess

# 添加 UFO 路徑（僅用於基本模組）
UFO_PATH = os.path.join(os.path.dirname(__file__), "../..")
sys.path.append(UFO_PATH)

class SimpleGmailAutomation:
    def __init__(self):
        """簡化的 Gmail 自動化初始化"""
        self.session_data = {}
        print("🤖 SimpleGmailAutomation 已初始化")
    
    def launch_chrome_with_gmail(self, url="https://mail.google.com/mail/u/0/#inbox"):
        """啟動 Chrome 並開啟 Gmail"""
        try:
            print(f"🚀 正在啟動 Chrome 並導航到: {url}")
            
            # 記錄啟動資訊
            self.session_data['launch_operation'] = {
                'url': url,
                'timestamp': time.time(),
                'status': 'started'
            }
            
            # 使用 Windows start 命令啟動 Chrome
            start_command = f'start chrome "{url}"'
            result = os.system(start_command)
            
            if result == 0:
                print("✅ Chrome 啟動命令執行成功")
                self.session_data['launch_operation']['status'] = 'success'
                return True
            else:
                print(f"⚠️ Chrome 啟動命令回傳值: {result}")
                self.session_data['launch_operation']['status'] = 'warning'
                return True  # 通常即使有警告也能成功啟動
                
        except Exception as e:
            print(f"❌ Chrome 啟動失敗: {e}")
            self.session_data['launch_operation']['status'] = 'error'
            self.session_data['launch_operation']['error'] = str(e)
            return False
    
    def search_gmail_by_input_click(self, keyword="多結果子"):
        """
        新方法：尋找「搜尋郵件」input，點擊它，輸入關鍵字，按 Enter 搜尋
        """
        try:
            print(f"🔍 使用新方法搜尋包含 '{keyword}' 的 Gmail 信件...")
            
            # 記錄操作資訊
            self.session_data['search_operation'] = {
                'method': 'input_click_and_type',
                'keyword': keyword,
                'timestamp': time.time(),
                'status': 'started'
            }
            
            # 導入 GUI 自動化模組
            try:
                import pyautogui
                import pyperclip
                
                # 設定 pyautogui 安全設定
                pyautogui.FAILSAFE = True
                pyautogui.PAUSE = 0.5
                
                print("✅ GUI 自動化模組已載入")
                
            except ImportError:
                print("❌ 缺少 pyautogui 或 pyperclip，請安裝：pip install pyautogui pyperclip")
                self.session_data['search_operation']['status'] = 'error'
                self.session_data['search_operation']['error'] = 'Missing GUI automation modules'
                return False
            
            # 等待 Gmail 完全載入
            print("⏳ 等待 Gmail 頁面完全載入...")
            time.sleep(5)
            
            # 獲取螢幕尺寸
            screen_width, screen_height = pyautogui.size()
            print(f"📺 螢幕尺寸: {screen_width} x {screen_height}")
            
            # 步驟1: 嘗試多種方法來聚焦搜尋框
            print("🎯 步驟1: 嘗試聚焦到 Gmail 搜尋框...")
            
            # 方法A: 點擊頂部中央的搜尋區域
            search_x = screen_width // 2
            search_y = 120  # Gmail 搜尋框通常在這個高度
            
            print(f"🖱️  方法A: 點擊搜尋區域 ({search_x}, {search_y})")
            pyautogui.click(search_x, search_y)
            time.sleep(1)
            
            # 方法B: 使用 Gmail 搜尋快捷鍵
            print("⌨️  方法B: 使用 Gmail 搜尋快捷鍵 Ctrl+K")
            pyautogui.hotkey('ctrl', 'k')
            time.sleep(1)
            
            # 方法C: 使用 / 鍵啟動搜尋
            print("⌨️  方法C: 使用 / 鍵啟動搜尋")
            pyautogui.press('/')
            time.sleep(1)
            
            # 步驟2: 清空搜尋框並輸入關鍵字
            print(f"📝 步驟2: 輸入搜尋關鍵字 '{keyword}'...")
            
            # 清空搜尋框
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.3)
            
            # 使用剪貼簿輸入關鍵字（更可靠）
            pyperclip.copy(keyword)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.8)
            
            print(f"✅ 已輸入關鍵字: '{keyword}'")
            
            # 步驟3: 按 Enter 執行搜尋
            print("🔎 步驟3: 按 Enter 執行搜尋...")
            pyautogui.press('enter')
            time.sleep(4)  # 等待搜尋結果載入
            
            print("⏳ 等待搜尋結果載入...")
            
            # 步驟4: 選取搜尋結果
            print("📬 步驟4: 選取搜尋到的信件...")
            
            # 全選當前頁面的信件
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(1)
            
            # 如果有更多信件，嘗試選取所有搜尋結果
            try:
                pyautogui.hotkey('ctrl', 'shift', 'a')
                time.sleep(1)
                print("📮 已嘗試選取所有搜尋結果")
            except:
                pass
            
            # 記錄成功
            self.session_data['search_operation']['status'] = 'success'
            
            print(f"✅ 搜尋和選取完成！")
            print(f"💡 應已找到並選取包含 '{keyword}' 的所有信件")
            
            return True
            
        except Exception as e:
            error_msg = f"Gmail 搜尋操作失敗: {str(e)}"
            print(f"❌ {error_msg}")
            self.session_data['search_operation']['status'] = 'error'
            self.session_data['search_operation']['error'] = str(e)
            return False
    
    def print_summary(self):
        """列印操作摘要"""
        print("\n" + "="*50)
        print("📊 Gmail 自動化操作摘要")
        print("="*50)
        
        if 'launch_operation' in self.session_data:
            launch_data = self.session_data['launch_operation']
            print(f"🚀 啟動操作:")
            print(f"   URL: {launch_data.get('url', 'N/A')}")
            print(f"   狀態: {launch_data.get('status', 'N/A')}")
            if 'error' in launch_data:
                print(f"   錯誤: {launch_data['error']}")
        
        if 'search_operation' in self.session_data:
            search_data = self.session_data['search_operation']
            print(f"🔍 搜尋操作:")
            print(f"   方法: {search_data.get('method', 'N/A')}")
            print(f"   關鍵字: {search_data.get('keyword', 'N/A')}")
            print(f"   狀態: {search_data.get('status', 'N/A')}")
            if 'error' in search_data:
                print(f"   錯誤: {search_data['error']}")
        
        print("="*50)

def main():
    """主程式執行"""
    print("🎯 === 簡化版 Chrome Gmail 自動化 ===")
    print("專注於實現：尋找搜尋框 → 點擊 → 輸入關鍵字 → 搜尋 → 選取")
    print("-" * 50)
    
    # 初始化自動化代理
    gmail_agent = SimpleGmailAutomation()
    
    try:
        # 步驟1: 啟動 Chrome 到 Gmail
        print("\n📱 步驟1: 啟動 Chrome 瀏覽器...")
        gmail_url = "https://mail.google.com/mail/u/0/#inbox"
        launch_success = gmail_agent.launch_chrome_with_gmail(gmail_url)
        
        if launch_success:
            print("✅ Chrome 啟動成功")
            
            # 步驟2: 執行搜尋和選取
            print("\n🔍 步驟2: 執行 Gmail 搜尋和信件選取...")
            search_success = gmail_agent.search_gmail_by_input_click("多結果子")
            
            if search_success:
                print("✅ Gmail 搜尋和選取完成")
            else:
                print("❌ Gmail 搜尋和選取失敗")
        else:
            print("❌ Chrome 啟動失敗")
        
        # 顯示操作摘要
        gmail_agent.print_summary()
        
        print("\n🎉 自動化流程執行完成！")
        print("💡 請檢查 Gmail 中的搜尋結果和選取狀態")
        
    except Exception as e:
        print(f"❌ 程式執行失敗: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
    
    print("\n📋 後續檢查項目:")
    print("1. Chrome 是否已開啟 Gmail？")
    print("2. Gmail 搜尋框是否已聚焦並輸入關鍵字？")
    print("3. 搜尋結果是否正確顯示？")
    print("4. 包含 '多結果子' 的信件是否已被選取？")
    
    input("\n按 Enter 鍵結束程式...")
