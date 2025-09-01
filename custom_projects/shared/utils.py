# ===== UFO 專案共用工具 =====
import sys
import os

def setup_ufo_path(levels_up=2):
    """
    設定 UFO 框架路徑
    
    Args:
        levels_up (int): 向上幾層目錄找到 UFO 根目錄
    
    Returns:
        str: UFO 框架的絕對路徑
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ufo_path = current_dir
    
    for _ in range(levels_up):
        ufo_path = os.path.dirname(ufo_path)
    
    if ufo_path not in sys.path:
        sys.path.append(ufo_path)
    
    return ufo_path

def check_dependencies():
    """
    檢查必要的依賴套件
    
    Returns:
        dict: 依賴套件的可用性狀態
    """
    dependencies = {}
    
    try:
        import pyautogui
        dependencies['pyautogui'] = True
    except ImportError:
        dependencies['pyautogui'] = False
    
    try:
        import pyperclip
        dependencies['pyperclip'] = True
    except ImportError:
        dependencies['pyperclip'] = False
    
    try:
        from ufo.automator.ui_control.inspector import ControlInspectorFacade
        dependencies['ufo'] = True
    except ImportError:
        dependencies['ufo'] = False
    
    return dependencies

def print_system_info():
    """列印系統和環境資訊"""
    import platform
    
    print("=== 系統環境資訊 ===")
    print(f"作業系統: {platform.system()} {platform.release()}")
    print(f"Python 版本: {platform.python_version()}")
    print(f"架構: {platform.architecture()[0]}")
    
    dependencies = check_dependencies()
    print("\n=== 依賴套件狀態 ===")
    for package, available in dependencies.items():
        status = "✅ 已安裝" if available else "❌ 未安裝"
        print(f"{package}: {status}")
    
    print("-" * 40)

class UIAutomationHelper:
    """UI 自動化輔助工具類"""
    
    @staticmethod
    def safe_input_text(content, use_clipboard=True):
        """
        安全的文字輸入方法
        
        Args:
            content (str): 要輸入的文字
            use_clipboard (bool): 是否優先使用剪貼簿
        """
        try:
            if use_clipboard:
                import pyperclip
                pyperclip.copy(content)
                import pyautogui
                pyautogui.hotkey("ctrl", "v")
            else:
                import pyautogui
                pyautogui.write(content, interval=0.1)
        except ImportError:
            print("警告：缺少必要的套件，請安裝 pyautogui 和 pyperclip")
            raise
    
    @staticmethod
    def wait_and_retry(func, max_retries=3, delay=1):
        """
        帶重試機制的函數執行
        
        Args:
            func: 要執行的函數
            max_retries (int): 最大重試次數
            delay (float): 重試間隔（秒）
        """
        import time
        
        for attempt in range(max_retries):
            try:
                return func()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                print(f"嘗試 {attempt + 1} 失敗，{delay} 秒後重試...")
                time.sleep(delay)
