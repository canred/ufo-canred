import time
from enum import Enum

class AutomationMethod(Enum):
    SELENIUM = "selenium"
    PLAYWRIGHT = "playwright"
    CDP = "cdp"
    PYAUTOGUI = "pyautogui"

class SmartChromeAutomation:
    def __init__(self, preferred_method=AutomationMethod.SELENIUM):
        """智能 Chrome 自動化 - 支援多種方法"""
        self.method = preferred_method
        self.automation_instance = None
        
    def setup(self):
        """自動設定最佳的自動化方法"""
        methods_to_try = [
            (AutomationMethod.SELENIUM, self._setup_selenium),
            (AutomationMethod.PLAYWRIGHT, self._setup_playwright),
            (AutomationMethod.CDP, self._setup_cdp),
            (AutomationMethod.PYAUTOGUI, self._setup_pyautogui)
        ]
        
        # 優先嘗試用戶指定的方法
        for method, setup_func in methods_to_try:
            if method == self.method:
                if setup_func():
                    print(f"✅ 使用 {method.value} 方法初始化成功")
                    return True
        
        # 如果指定方法失敗，嘗試其他方法
        for method, setup_func in methods_to_try:
            if method != self.method:
                if setup_func():
                    print(f"✅ 回退到 {method.value} 方法")
                    self.method = method
                    return True
        
        print("❌ 所有自動化方法都失敗")
        return False
    
    def _setup_selenium(self):
        """設定 Selenium"""
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--start-maximized")
            
            self.automation_instance = webdriver.Chrome(options=chrome_options)
            return True
        except:
            return False
    
    def _setup_playwright(self):
        """設定 Playwright"""
        try:
            from playwright.sync_api import sync_playwright
            
            playwright = sync_playwright().start()
            browser = playwright.chromium.launch(headless=False)
            self.automation_instance = browser.new_page()
            return True
        except:
            return False
    
    def _setup_cdp(self):
        """設定 CDP"""
        try:
            # CDP 設定邏輯
            return False  # 簡化示例
        except:
            return False
    
    def _setup_pyautogui(self):
        """設定 PyAutoGUI"""
        try:
            import pyautogui
            self.automation_instance = pyautogui
            return True
        except:
            return False
    
    def gmail_automation(self):
        """統一的 Gmail 自動化接口"""
        if self.method == AutomationMethod.SELENIUM:
            return self._selenium_gmail_automation()
        elif self.method == AutomationMethod.PLAYWRIGHT:
            return self._playwright_gmail_automation()
        elif self.method == AutomationMethod.PYAUTOGUI:
            return self._pyautogui_gmail_automation()
        else:
            return False
    
    def _selenium_gmail_automation(self):
        """Selenium Gmail 自動化"""
        try:
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.keys import Keys
            
            driver = self.automation_instance
            driver.get("https://mail.google.com/mail/u/0/#inbox")
            
            # 等待並操作搜尋框
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label*='搜尋']"))
            )
            search_box.send_keys("多結果子")
            search_box.send_keys(Keys.ENTER)
            
            time.sleep(3)
            
            # 選取 checkboxes
            checkboxes = driver.find_elements(By.CSS_SELECTOR, "div[role='checkbox']")
            for i, checkbox in enumerate(checkboxes[:5]):
                checkbox.click()
                time.sleep(0.5)
            
            print("✅ Selenium Gmail 自動化完成")
            return True
            
        except Exception as e:
            print(f"❌ Selenium Gmail 自動化失敗: {e}")
            return False
    
    def _pyautogui_gmail_automation(self):
        """PyAutoGUI Gmail 自動化"""
        try:
            import pyautogui
            import subprocess
            
            # 啟動 Chrome
            subprocess.Popen(["chrome.exe", "https://mail.google.com/mail/u/0/#inbox"])
            time.sleep(5)
            
            # 點擊搜尋框並輸入
            pyautogui.click(400, 100)  # 搜尋框座標
            pyautogui.typewrite("多結果子")
            pyautogui.press('enter')
            
            time.sleep(3)
            
            # 點擊 checkboxes
            for i in range(5):
                y_pos = 200 + (i * 50)
                pyautogui.click(155, y_pos)
                time.sleep(0.5)
            
            print("✅ PyAutoGUI Gmail 自動化完成")
            return True
            
        except Exception as e:
            print(f"❌ PyAutoGUI Gmail 自動化失敗: {e}")
            return False

# 使用範例
if __name__ == "__main__":
    # 建立智能自動化實例
    automation = SmartChromeAutomation(AutomationMethod.SELENIUM)
    
    if automation.setup():
        automation.gmail_automation()
        input("按 Enter 鍵繼續...")