# ===== 模組導入區 =====
import sys
import os

# 添加 UFO 框架路徑到 Python 路徑
UFO_PATH = os.path.join(os.path.dirname(__file__), "../..")
sys.path.append(UFO_PATH)

# 設定配置檔案路徑環境變數（避免警告）
os.environ.setdefault('UFO_CONFIG_PATH', os.path.join(os.path.dirname(__file__), 'config.yaml'))

# 導入 UFO 框架模組
from ufo.automator.ui_control.inspector import ControlInspectorFacade  # UFO框架的UI檢查器，用於檢測和操作桌面視窗
import time  # 時間模組，用於添加延遲確保GUI操作穩定
import pyautogui  # Python GUI自動化庫，模擬鍵盤滑鼠操作

# 嘗試導入剪貼簿庫，用於解決中文輸入問題
try:
    import pyperclip  # 剪貼簿操作庫，用於處理中文字符輸入
    HAS_PYPERCLIP = True
except ImportError:
    HAS_PYPERCLIP = False
    print("警告：未安裝 pyperclip，中文輸入可能有問題。請執行 'pip install pyperclip' 安裝。")

# ===== 記事本自動化代理類別 =====
class NotepadGUIAgent:
    def __init__(self):
        """初始化記事本 GUI 代理"""
        # 建立UFO框架的UI檢查器實例，用於檢測桌面視窗
        self.inspector = ControlInspectorFacade()
        # 儲存記事本視窗物件的變數，初始為None
        self.notepad_window = None

    def open_notepad(self):
        """步驟1：打開記事本"""
        # ===== 啟動記事本應用程式 =====
        # 通過系統命令啟動 Notepad（Windows 環境）
        os.startfile("notepad.exe")  # 使用Windows內建指令啟動記事本
        time.sleep(3)  # 等待3秒讓記事本完全載入
        
        # ===== 尋找記事本視窗 =====
        # 獲取所有桌面視窗的清單
        desktop_windows = self.inspector.get_desktop_windows()
        
        # 遍歷所有視窗，尋找記事本視窗
        for window in desktop_windows:
            try:
                # 獲取視窗標題文字
                window_text = window.window_text()
                # 檢查是否包含記事本相關的關鍵字（支援中英文）
                if "記事本" in window_text or "Notepad" in window_text or "無標題" in window_text:
                    self.notepad_window = window  # 儲存找到的記事本視窗
                    print(f"記事本已成功打開: {window_text}")
                    return  # 找到後立即返回
            except:
                # 如果某個視窗無法讀取標題，繼續檢查下一個
                continue
        
        # ===== 錯誤處理 =====
        # 如果沒有找到記事本視窗，拋出異常
        if not self.notepad_window:
            raise Exception("記事本窗口未找到，啟動失敗")

    def input_text(self, content):
        """步驟2：在記事本中輸入文本"""
        # ===== 檢查前置條件 =====
        # 確保記事本視窗已經找到並存在
        if not self.notepad_window:
            raise Exception("記事本窗口未找到")
        
        # ===== 激活記事本視窗 =====
        # 將焦點設定到記事本視窗，確保後續輸入會進入記事本
        self.notepad_window.set_focus()
        time.sleep(1)  # 等待視窗激活完成
        
        # ===== 輸入文字 =====
        # 根據是否有 pyperclip 庫選擇不同的輸入方式
        if HAS_PYPERCLIP:
            # 方法1: 使用剪貼簿方式輸入中文文本，避免編碼問題
            pyperclip.copy(content)  # 將文本複製到剪貼簿
            time.sleep(0.5)  # 等待剪貼簿操作完成
            pyautogui.hotkey("ctrl", "v")  # 使用 Ctrl+V 粘貼文本（支援中文）
        else:
            # 方法2: 備用方案 - 逐字符輸入（可能對中文支援有限）
            try:
                # 嘗試設定 pyautogui 的輸入法
                pyautogui.write(content, interval=0.1)  # 增加間隔時間
            except:
                # 如果直接輸入失敗，嘗試使用虛擬鍵盤
                for char in content:
                    pyautogui.press(char) if char.isascii() else pyautogui.write(char)
                    time.sleep(0.1)
                    
        print(f"已輸入文本：{content}")  # 確認輸入完成

    def save_file(self, save_path):
        """步驟3：按指定路徑保存文件"""
        # ===== 檢查前置條件 =====
        # 確保記事本視窗已經找到並存在
        if not self.notepad_window:
            raise Exception("記事本窗口未找到")
        
        # ===== 觸發保存對話框 =====
        # 模擬按下 Ctrl+S 觸發保存對話框
        pyautogui.hotkey("ctrl", "s")  # 組合鍵：Ctrl + S
        time.sleep(2)  # 等待保存對話框完全顯示
        
        # ===== 輸入檔案路徑 =====
        # 在保存對話框中輸入指定的檔案路徑
        pyautogui.write(save_path, interval=0.05)  # 逐字輸入路徑
        time.sleep(1)  # 等待輸入完成
        
        # ===== 確認保存 =====
        # 按下 Enter 確認保存操作
        pyautogui.press("enter")
        time.sleep(1)  # 等待保存操作完成
        
        # ===== 處理檔案覆蓋確認 =====
        # 如果檔案已存在，可能會出現覆蓋確認對話框
        try:
            pyautogui.press("enter")  # 如果有確認弹窗就按確認
        except:
            pass  # 如果沒有弹窗就忽略
            
        print(f"文件已保存至：{save_path}")  # 確認保存完成

    def close_notepad(self):
        """步驟4：關閉記事本"""
        # ===== 檢查前置條件 =====
        # 確保記事本視窗已經找到並存在
        if not self.notepad_window:
            raise Exception("記事本窗口未找到")
        
        # ===== 激活並關閉視窗 =====
        # 激活窗口後，模擬 Alt+F4 關閉
        self.notepad_window.set_focus()  # 確保記事本視窗在前景
        time.sleep(0.5)  # 等待視窗激活
        pyautogui.hotkey("alt", "f4")  # 組合鍵：Alt + F4 (通用關閉視窗快捷鍵)
        print("記事本已關閉")  # 確認關閉完成

# ============================= 主程式執行區 =============================
if __name__ == "__main__":
    print("=== 記事本自動化測試程式 ===")
    print(f"UFO 框架路徑: {os.path.abspath(UFO_PATH)}")
    print(f"pyperclip 支援: {'是' if HAS_PYPERCLIP else '否'}")
    
    # 檢查配置檔案
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    if os.path.exists(config_path):
        print(f"配置檔案: {config_path}")
    else:
        print("注意：未找到配置檔案，使用預設設定")
    
    print("-" * 50)
    
    # ===== 初始化自動化代理 =====
    # 建立記事本 GUI 自動化代理實例
    notepad_agent = NotepadGUIAgent()
    
    try:
        # ===== 執行自動化流程 =====
        # 步驟1: 打開記事本應用程式
        notepad_agent.open_notepad()
        
        # 步驟2: 在記事本中輸入指定的測試文字
        # 注意：此行包含中文字符，需要確保系統支援中文輸入
        # 如果中文無法正確輸出，請安裝 pyperclip: pip install pyperclip
        notepad_agent.input_text("這是 UFO 自動操作 GUI 生成的測試文本！")
        
        # 步驟3: 將文件保存到指定路徑（注意：路徑需要根據實際環境調整）
        save_path = os.path.join(os.path.dirname(__file__), "test_output.txt")
        notepad_agent.save_file(save_path)
        
        # 步驟4: 關閉記事本應用程式
        notepad_agent.close_notepad()
        
        # ===== 成功完成提示 =====
        print("整個 GUI 操作流程執行完成！")
        
    except Exception as e:
        # ===== 錯誤處理 =====
        # 捕獲並顯示任何執行過程中的錯誤
        print(f"操作失敗：{str(e)}")
