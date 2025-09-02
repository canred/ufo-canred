# ===== 模組導入區 =====
import sys
import os

# 添加 UFO 框架路徑到 Python 路徑
UFO_PATH = os.path.join(os.path.dirname(__file__), "../..")
sys.path.append(UFO_PATH)

# 設定配置檔案路徑環境變數（避免警告）
os.environ.setdefault('UFO_CONFIG_PATH', os.path.join(os.path.dirname(__file__), 'config.yaml'))

# 注意：需要安裝 pyautogui 和 pyperclip 來進行 UI 自動化和剪貼簿操作
# 安裝命令：pip install pyautogui pyperclip

# 導入 UFO2 基本模組
import time
import subprocess
from ufo.module.basic import BaseSession
from ufo.config.config import Config
from ufo.agents.agent.host_agent import HostAgent, AgentFactory
from ufo.agents.agent.app_agent import AppAgent
from ufo.llm.llm_call import get_completion
from ufo.module.sessions.session import SessionFactory
from ufo.module.context import Context, ContextNames
from ufo.automator.ui_control.inspector import ControlInspectorFacade
from ufo import utils

# ===== Chrome 瀏覽器自動化代理類別 =====
class ChromeAutomationAgent:
    def __init__(self):
        """
        初始化 Chrome 自動化代理
        使用 UFO2 架構進行瀏覽器自動化
        """
        self.session_data = {}
        
        # 初始化 UFO2 配置
        try:
            self.config = Config.get_instance().config_data
            print("✅ UFO2 配置已載入")
        except Exception as e:
            print(f"⚠️  UFO2 配置載入失敗，使用預設設定: {e}")
            self.config = {}
            
        # 初始化 Host Agent
        try:
            self.host_agent = AgentFactory.create_agent(
                "host",
                "HostAgent",
                self.config.get("HOST_AGENT", {}).get("VISUAL_MODE", True),
                self.config.get("HOSTAGENT_PROMPT", ""),
                self.config.get("HOSTAGENT_EXAMPLE_PROMPT", ""),
                self.config.get("API_PROMPT", "")
            )
            print("✅ UFO2 Host Agent 已初始化")
        except Exception as e:
            print(f"⚠️  Host Agent 初始化失敗: {e}")
            self.host_agent = None
            
        # 初始化控制檢查器
        self.inspector = ControlInspectorFacade()
        
        # 初始化會話上下文
        self.context = Context()
        self.context.set(ContextNames.LOG_PATH, "./logs/chrome_automation/")
        utils.create_folder("./logs/chrome_automation/")
        
    def launch_chrome_with_gmail(self, url="https://mail.google.com/mail/u/0/#inbox"):
        """
        啟動 Chrome 瀏覽器並開啟指定 URL
        """
        try:
            print(f"🚀 正在啟動 Chrome 瀏覽器並導航到: {url}")
            
            # 記錄啟動資訊
            self.session_data['launch_operation'] = {
                'agent_type': 'HostAgent',
                'automation_type': 'Browser_Launch',
                'target_app': 'Chrome',
                'action': 'launch_with_url',
                'url': url,
                'timestamp': time.time(),
                'status': 'started'
            }
            
            # 方法1: 使用 HostAgent 進行應用程式啟動
            if self.host_agent:
                try:
                    # 構建 LLM 請求來規劃瀏覽器啟動
                    automation_prompt = [
                        {
                            "role": "system", 
                            "content": "You are a UFO2 HostAgent for launching Chrome browser and navigating to websites. Help plan browser automation tasks."
                        },
                        {
                            "role": "user",
                            "content": f"Launch a new Chrome browser window and navigate to {url}. Return the automation plan in text format."
                        }
                    ]
                    
                    # 使用 UFO2 的 LLM API 來規劃瀏覽器啟動
                    response, cost = get_completion(
                        automation_prompt,
                        agent="HOST",  # 使用 HOST Agent
                        use_backup_engine=True
                    )
                    
                    formatted_cost = f"{float(cost):.3f}" if cost is not None else "0.000"
                    print(f"🎯 HostAgent 規劃: {response}")
                    print(f"💰 HostAgent API 成本: ${formatted_cost}")
                    
                    # 記錄 AI 規劃結果
                    self.session_data['launch_operation']['ai_planning'] = response
                    self.session_data['launch_operation']['api_cost'] = float(cost) if cost is not None else 0.0
                    
                except Exception as e:
                    print(f"⚠️  HostAgent 規劃失敗，將使用直接啟動方式: {e}")
            
            # 執行實際的瀏覽器啟動
            print("📋 執行瀏覽器啟動...")
            
            # 方法: 使用系統命令啟動 Chrome 並指定 URL
            chrome_command = [
                "chrome.exe",  # Chrome 執行檔
                "--new-window",  # 開啟新視窗
                "--start-maximized",  # 最大化視窗
                url  # 目標 URL
            ]
            
            # 嘗試啟動 Chrome
            try:
                process = subprocess.Popen(chrome_command)
                print(f"✅ Chrome 已啟動，程序 PID: {process.pid}")
                
                # 等待 Chrome 完全載入
                time.sleep(3)
                
                # 驗證 Chrome 是否成功啟動
                chrome_window = self._find_chrome_window()
                if chrome_window:
                    print(f"✅ Chrome 視窗已找到: {chrome_window.window_text()}")
                    self.session_data['launch_operation']['status'] = 'success'
                    self.session_data['launch_operation']['window_title'] = chrome_window.window_text()
                    return True
                else:
                    print("⚠️  Chrome 視窗未找到，但程序已啟動")
                    self.session_data['launch_operation']['status'] = 'partial_success'
                    return True
                    
            except FileNotFoundError:
                # 如果 chrome.exe 不在 PATH 中，嘗試常見的 安裝路徑
                chrome_paths = [
                    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                    r"C:\Users\{}\AppData\Local\Google\Chrome\Application\chrome.exe".format(os.getenv('USERNAME')),
                ]
                
                for chrome_path in chrome_paths:
                    if os.path.exists(chrome_path):
                        print(f"🔍 在 {chrome_path} 找到 Chrome")
                        chrome_command[0] = chrome_path
                        try:
                            process = subprocess.Popen(chrome_command)
                            print(f"✅ Chrome 已啟動，程序 PID: {process.pid}")
                            time.sleep(3)
                            
                            chrome_window = self._find_chrome_window()
                            if chrome_window:
                                print(f"✅ Chrome 視窗已找到: {chrome_window.window_text()}")
                                self.session_data['launch_operation']['status'] = 'success'
                                self.session_data['launch_operation']['window_title'] = chrome_window.window_text()
                                return True
                            else:
                                self.session_data['launch_operation']['status'] = 'partial_success'
                                return True
                        except Exception as e:
                            print(f"❌ 使用路徑 {chrome_path} 啟動失敗: {e}")
                            continue
                
                # 如果所有路徑都失敗，嘗試使用 Windows start 命令
                print("🔄 嘗試使用 Windows start 命令...")
                try:
                    start_command = f'start chrome "{url}"'
                    os.system(start_command)
                    time.sleep(3)
                    
                    chrome_window = self._find_chrome_window()
                    if chrome_window:
                        print(f"✅ Chrome 視窗已找到: {chrome_window.window_text()}")
                        self.session_data['launch_operation']['status'] = 'success'
                        self.session_data['launch_operation']['window_title'] = chrome_window.window_text()
                        return True
                    else:
                        print("⚠️  Chrome 可能已啟動，但視窗未找到")
                        self.session_data['launch_operation']['status'] = 'unknown'
                        return True
                        
                except Exception as e:
                    print(f"❌ Windows start 命令失敗: {e}")
                    self.session_data['launch_operation']['status'] = 'error'
                    self.session_data['launch_operation']['error'] = str(e)
                    return False
            
        except Exception as e:
            error_msg = f"Chrome 啟動失敗: {str(e)}"
            print(f"❌ {error_msg}")
            self.session_data['launch_operation']['status'] = 'error'
            self.session_data['launch_operation']['error'] = str(e)
            return False
    
    def _find_chrome_window(self):
        """
        尋找 Chrome 瀏覽器視窗
        """
        try:
            desktop_windows = self.inspector.get_desktop_windows()
            
            for window in desktop_windows:
                try:
                    window_text = window.window_text()
                    # 檢查是否為 Chrome 瀏覽器視窗
                    if ("Chrome" in window_text or 
                        "Google Chrome" in window_text or
                        "Gmail" in window_text or
                        "mail.google.com" in window_text):
                        return window
                except:
                    continue
            return None
        except Exception as e:
            print(f"⚠️  尋找 Chrome 視窗時發生錯誤: {e}")
            return None
    
    def create_app_agent_for_chrome(self):
        """
        為 Chrome 瀏覽器建立 AppAgent
        """
        try:
            if not self.host_agent:
                print("❌ Host Agent 未初始化，無法建立 App Agent")
                return None
                
            print("🤖 正在為 Chrome 建立 AppAgent...")
            
            # 尋找 Chrome 視窗
            chrome_window = self._find_chrome_window()
            if not chrome_window:
                print("❌ 未找到 Chrome 視窗，無法建立 AppAgent")
                return None
            
            # 設定 Chrome 視窗為全螢幕模式
            print("🖥️  設定 Chrome 視窗為全螢幕模式...")
            try:
                # 先聚焦到 Chrome 視窗
                chrome_window.set_focus()
                time.sleep(1)
                
                # 使用 F11 鍵進入全螢幕模式
                import pyautogui
                pyautogui.press('f11')
                time.sleep(2)  # 等待全螢幕模式生效
                
                print("✅ Chrome 視窗已設為全螢幕模式")
                
            except Exception as e:
                print(f"⚠️  設定全螢幕模式失敗: {e}")
                # 即使全螢幕設定失敗，仍繼續建立 AppAgent

            # 實際建立 AppAgent
            try:
                print("🔧 建立 Chrome AppAgent...")
                
                # 使用 AgentFactory 建立 AppAgent，提供所有必要參數
                print("111111")
                app_agent = AgentFactory.create_agent(
                    agent_type="app",
                    name="ChromeAppAgent",
                    process_name="chrome.exe",
                    app_root_name="Chrome",
                    is_visual=True,
                    main_prompt="",
                    example_prompt="",
                    api_prompt=""
                )
                print("✅ AppAgent 物件建立成功")
                
                # 檢查 AppAgent 可用的屬性和方法
                print("🔍 檢查 AppAgent 可用的方法...")
                agent_methods = [method for method in dir(app_agent) if not method.startswith('_')]
                window_methods = [method for method in agent_methods if 'window' in method.lower()]
                print(f"📋 視窗相關方法: {window_methods}")
                
                # 嘗試設定應用程式視窗（使用容錯處理）
                try:
                    # 檢查是否有其他設定視窗的方法
                    if hasattr(app_agent, 'application_window'):
                        app_agent.application_window = chrome_window
                        print("✅ 使用 application_window 屬性設定視窗")
                    elif hasattr(app_agent, 'app_window'):
                        app_agent.app_window = chrome_window
                        print("✅ 使用 app_window 屬性設定視窗")
                    else:
                        print("⚠️  AppAgent 沒有視窗設定方法，跳過視窗設定")
                except Exception as e:
                    print(f"⚠️  設定視窗失敗: {e}")
                
                # 獲取應用程式根名稱
                try:
                    app_root_name = chrome_window.window_text()
                    if not app_root_name:
                        app_root_name = "Chrome"
                    
                    # 嘗試設定應用程式根名稱（使用容錯處理）
                    if hasattr(app_agent, 'set_app_root_name'):
                        app_agent.set_app_root_name(app_root_name)
                        print(f"📱 使用 set_app_root_name: {app_root_name}")
                    elif hasattr(app_agent, 'app_root_name'):
                        app_agent.app_root_name = app_root_name
                        print(f"📱 使用 app_root_name 屬性: {app_root_name}")
                    else:
                        print(f"⚠️  無法設定應用程式根名稱，但已記錄: {app_root_name}")
                        
                except Exception as e:
                    print(f"⚠️  設定應用程式根名稱失敗: {e}")
                    # 設定預設值
                    app_root_name = "Chrome"
                
                # 設定上下文
                self.context.set(ContextNames.APPLICATION_WINDOW, chrome_window)
                
                print("✅ Chrome AppAgent 建立成功")
                
                # 記錄 AppAgent 建立資訊
                self.session_data['app_agent_creation'] = {
                    'agent_type': 'AppAgent',
                    'target_app': 'Chrome',
                    'window_title': chrome_window.window_text(),
                    'visual_mode': self.config.get("APP_AGENT", {}).get("VISUAL_MODE", True),
                    'status': 'success',
                    'timestamp': time.time()
                }
                
                return app_agent
                
            except Exception as e:
                error_msg = f"建立 AppAgent 失敗: {e}"
                print(f"❌ {error_msg}")
                self.session_data['app_agent_creation'] = {
                    'agent_type': 'AppAgent',
                    'target_app': 'Chrome',
                    'status': 'error',
                    'error': str(e),
                    'timestamp': time.time()
                }
                return None
            
        except Exception as e:
            error_msg = f"建立 AppAgent 失敗: {e}"
            print(f"❌ {error_msg}")
            self.session_data['app_agent_creation'] = {
                'agent_type': 'AppAgent',
                'target_app': 'Chrome',
                'status': 'error',
                'error': str(e),
                'timestamp': time.time()
            }
            return None
    
    def print_summary(self):
        """
        列印自動化操作摘要
        """
        print("\n" + "="*60)
        print("🎯 Chrome 瀏覽器自動化摘要")
        print("="*60)
        
        if 'launch_operation' in self.session_data:
            launch_data = self.session_data['launch_operation']
            print(f"🚀 啟動操作:")
            print(f"   代理類型: {launch_data.get('agent_type', 'N/A')}")
            print(f"   自動化類型: {launch_data.get('automation_type', 'N/A')}")
            print(f"   目標應用程式: {launch_data.get('target_app', 'N/A')}")
            print(f"   操作方式: {launch_data.get('action', 'N/A')}")
            print(f"   目標 URL: {launch_data.get('url', 'N/A')}")
            print(f"   狀態: {launch_data.get('status', 'N/A')}")
            
            if 'window_title' in launch_data:
                print(f"   視窗標題: {launch_data['window_title']}")
            if 'ai_planning' in launch_data:
                print(f"   AI 規劃: {launch_data['ai_planning']}")
            if 'api_cost' in launch_data:
                print(f"   API 成本: ${launch_data['api_cost']:.3f}")
            if 'error' in launch_data:
                print(f"   錯誤: {launch_data['error']}")
        
        if 'email_selection' in self.session_data:
            email_data = self.session_data['email_selection']
            print(f"\n📧 Gmail 信件選取操作:")
            print(f"   代理類型: {email_data.get('agent_type', 'N/A')}")
            print(f"   自動化類型: {email_data.get('automation_type', 'N/A')}")
            print(f"   目標應用程式: {email_data.get('target_app', 'N/A')}")
            print(f"   操作方式: {email_data.get('action', 'N/A')}")
            print(f"   搜尋關鍵字: {email_data.get('subject_keyword', 'N/A')}")
            print(f"   狀態: {email_data.get('status', 'N/A')}")
            
            if 'selected_count' in email_data:
                print(f"   選取信件數量: {email_data['selected_count']}")
            if 'ai_planning' in email_data:
                print(f"   AI 規劃: {email_data['ai_planning']}")
            if 'api_cost' in email_data:
                print(f"   API 成本: ${email_data['api_cost']:.3f}")
            if 'error' in email_data:
                print(f"   錯誤: {email_data['error']}")
        
        if 'app_agent_search' in self.session_data:
            search_data = self.session_data['app_agent_search']
            print(f"\n🔍 UFO2 AppAgent Gmail 搜尋操作:")
            print(f"   代理類型: {search_data.get('agent_type', 'N/A')}")
            print(f"   自動化類型: {search_data.get('automation_type', 'N/A')}")
            print(f"   目標應用程式: {search_data.get('target_app', 'N/A')}")
            print(f"   操作方式: {search_data.get('action', 'N/A')}")
            print(f"   搜尋關鍵字: {search_data.get('search_keyword', 'N/A')}")
            print(f"   狀態: {search_data.get('status', 'N/A')}")
            
            if 'search_completed' in search_data:
                print(f"   搜尋完成: {search_data['search_completed']}")
            if 'ai_planning' in search_data:
                print(f"   AI 規劃: {search_data['ai_planning']}")
            if 'api_cost' in search_data:
                print(f"   API 成本: ${search_data['api_cost']:.3f}")
            if 'error' in search_data:
                print(f"   錯誤: {search_data['error']}")
        
        print("="*60)
    
    def simulate_mouse_click_at_position(self, x, y, button='left', duration=0.5):
        """
        模擬滑鼠移動到指定位置並點擊
        
        參數:
            x (int): 目標 X 座標
            y (int): 目標 Y 座標  
            button (str): 點擊按鈕類型 - 'left', 'right', 'middle'
            duration (float): 滑鼠移動持續時間（秒）
        """
        try:
            print(f"🖱️  模擬滑鼠移動到位置 ({x}, {y}) 並執行 {button} 點擊...")
            
            # 記錄操作資訊
            self.session_data['mouse_operation'] = {
                'operation_type': 'mouse_click',
                'target_position': (x, y),
                'click_button': button,
                'duration': duration,
                'timestamp': time.time(),
                'status': 'started'
            }
            
            # 導入 GUI 自動化模組
            try:
                import pyautogui
                
                # 設定 pyautogui 安全設定
                pyautogui.FAILSAFE = True
                pyautogui.PAUSE = 0.2
                
                print("✅ GUI 自動化模組已載入")
                
            except ImportError:
                print("❌ 缺少 pyautogui，請安裝：pip install pyautogui")
                self.session_data['mouse_operation']['status'] = 'error'
                self.session_data['mouse_operation']['error'] = 'Missing pyautogui module'
                return False
            
            # 獲取目前滑鼠位置
            current_x, current_y = pyautogui.position()
            print(f"📍 目前滑鼠位置: ({current_x}, {current_y})")
            
            # 獲取螢幕尺寸
            screen_width, screen_height = pyautogui.size()
            print(f"📺 螢幕尺寸: {screen_width} x {screen_height}")
            
            # 驗證座標是否在螢幕範圍內
            if x < 0 or x > screen_width or y < 0 or y > screen_height:
                error_msg = f"目標座標 ({x}, {y}) 超出螢幕範圍 (0, 0) - ({screen_width}, {screen_height})"
                print(f"❌ {error_msg}")
                self.session_data['mouse_operation']['status'] = 'error'
                self.session_data['mouse_operation']['error'] = error_msg
                return False
            
            # 步驟1: 平滑移動滑鼠到目標位置
            print(f"🎯 移動滑鼠到目標位置 ({x}, {y})，持續時間: {duration} 秒...")
            pyautogui.moveTo(x, y, duration=duration)
            time.sleep(0.1)  # 短暫停頓確保位置穩定
            
            # 驗證滑鼠是否到達目標位置
            final_x, final_y = pyautogui.position()
            print(f"📍 滑鼠最終位置: ({final_x}, {final_y})")
            
            # 步驟2: 執行點擊操作
            print(f"🖱️  執行 {button} 點擊...")
            
            if button.lower() == 'left':
                pyautogui.click()
                print("✅ 左鍵點擊完成")
            elif button.lower() == 'right':
                pyautogui.rightClick()
                print("✅ 右鍵點擊完成")
            elif button.lower() == 'middle':
                pyautogui.middleClick()
                print("✅ 中鍵點擊完成")
            else:
                error_msg = f"不支援的點擊按鈕類型: {button}"
                print(f"❌ {error_msg}")
                self.session_data['mouse_operation']['status'] = 'error'
                self.session_data['mouse_operation']['error'] = error_msg
                return False
            
            # 記錄成功
            self.session_data['mouse_operation']['status'] = 'success'
            self.session_data['mouse_operation']['final_position'] = (final_x, final_y)
            
            print(f"✅ 滑鼠操作完成！已在位置 ({final_x}, {final_y}) 執行 {button} 點擊")
            
            return True
        
        except Exception as e:
            error_msg = f"滑鼠操作失敗: {str(e)}"
            print(f"❌ {error_msg}")
            self.session_data['mouse_operation']['status'] = 'error'
            self.session_data['mouse_operation']['error'] = str(e)
            return False

# ============================= 主程式執行區 =============================
if __name__ == "__main__":
    print("=== UFO2 Chrome 瀏覽器自動化程式 ===")
    print(f"UFO 框架路徑: {os.path.abspath(UFO_PATH)}")
    
    # 檢查配置檔案
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    if os.path.exists(config_path):
        print(f"配置檔案: {config_path}")
    else:
        print("注意：未找到配置檔案，使用預設設定")
    
    print("-" * 60)
    
    # ===== 初始化自動化代理 =====
    chrome_agent = ChromeAutomationAgent()
    
    try:
        # ===== 執行 Chrome 自動化流程 =====
        
        # 步驟1: 啟動 Chrome 瀏覽器並開啟 Gmail
        gmail_url = "https://mail.google.com/mail/u/0/#inbox"
        success = chrome_agent.launch_chrome_with_gmail(gmail_url)
        
        if success:
            print(f"✅ Chrome 瀏覽器已成功啟動並導航到 Gmail")
            
            # 步驟2: （可選）建立 AppAgent 用於後續網頁操作
            print("\n🤖 建立 Chrome AppAgent 用於後續網頁操作...")
            app_agent = chrome_agent.create_app_agent_for_chrome()
            if app_agent:
                print("✅ Chrome AppAgent 已建立，可用於後續網頁自動化操作")
            else:
                print("⚠️  Chrome AppAgent 建立失敗，但瀏覽器已成功啟動")
            
            # 步驟3: 等待用戶確認 Gmail 已完全載入
            print("\n⏳ 等待 Gmail 完全載入...")
            time.sleep(5)  # 給 Gmail 更多時間載入
            
            # 步驟4: 使用 UFO2 AppAgent 搜尋 Gmail
            print("\n🔍 步驟4: 使用 UFO2 AppAgent 在 Gmail 中搜尋...")
            
            if app_agent:
                # 使用新建立的 AppAgent 搜尋方法
               
                print("\n🔍 步驟2: 執行 Gmail 搜尋和信件選取...")
                
                # 點擊搜尋框
                print("🎯 點擊 Gmail 搜尋框...")
                chrome_agent.simulate_mouse_click_at_position(280, 20, button='left', duration=0.5)
                time.sleep(1)
                
                # 輸入搜尋關鍵字 多結果子
                print("⌨️  輸入搜尋關鍵字: 多結果子")
                import pyautogui
                import pyperclip
                
                # 使用剪貼簿來輸入中文字，確保字符正確性
                search_keyword = "多結果子"
                pyperclip.copy(search_keyword)  # 複製到剪貼簿
                time.sleep(0.2)  # 等待剪貼簿操作完成
                
                # 使用 Ctrl+V 貼上
                pyautogui.hotkey('ctrl', 'v')
                print(f"✅ 已使用剪貼簿輸入關鍵字: {search_keyword}")
                time.sleep(0.5)
                
                # 按 Enter 執行搜尋
                print("🔍 按 Enter 執行搜尋...")
                pyautogui.press('enter')
                time.sleep(3)  # 等待搜尋結果載入
                
                print("✅ Gmail 搜尋任務完成！已搜尋關鍵字：多結果子")
                
                # 步驟5: 選擇前5筆郵件的checkbox
                print("\n📧 步驟5: 選擇前5筆郵件...")
                
                # 等待搜尋結果完全載入
                print("⏳ 等待搜尋結果完全載入...")
                time.sleep(2)
                
                # Gmail 郵件列表中 checkbox 的大致位置（需要根據實際頁面調整）
                # 假設郵件列表從 Y=150 開始，每筆郵件高度約 40-50 像素
                # checkbox 通常在郵件列表左側，X 座標約在 155 左右
                
                checkbox_x = 258  # checkbox 的 X 座標
                start_y = 150     # 第一筆郵件的 Y 座標
                email_height = 45 # 每筆郵件的高度
                
                selected_count = 0
                max_emails = 5
                
                print(f"🎯 開始選擇前 {max_emails} 筆郵件的 checkbox...")
                
                for i in range(max_emails):
                    # 計算當前郵件 checkbox 的 Y 座標
                    current_y = start_y + (i * email_height)
                    
                    try:
                        print(f"📍 點擊第 {i+1} 筆郵件的 checkbox 位置: ({checkbox_x}, {current_y})")
                        
                        # 點擊 checkbox
                        success = chrome_agent.simulate_mouse_click_at_position(
                            checkbox_x, 
                            current_y, 
                            button='left', 
                            duration=0.3
                        )
                        
                        if success:
                            selected_count += 1
                            print(f"✅ 第 {i+1} 筆郵件已選取")
                            time.sleep(0.5)  # 每次點擊間隔
                        else:
                            print(f"⚠️  第 {i+1} 筆郵件選取失敗")
                            
                    except Exception as e:
                        print(f"❌ 選取第 {i+1} 筆郵件時發生錯誤: {e}")
                        continue
                
                # 記錄選取結果
                chrome_agent.session_data['email_selection'] = {
                    'agent_type': 'MouseAutomation',
                    'automation_type': 'Email_Selection',
                    'target_app': 'Gmail',
                    'action': 'select_checkboxes',
                    'search_keyword': '多結果子',
                    'selected_count': selected_count,
                    'target_count': max_emails,
                    'status': 'completed' if selected_count > 0 else 'failed',
                    'timestamp': time.time()
                }
                
                if selected_count > 0:
                    print(f"🎉 Gmail 郵件選取完成！已成功選取 {selected_count} 筆郵件")
                else:
                    print("❌ 未能選取任何郵件，請檢查頁面佈局或座標設定")
                
                #search_success = chrome_agent.search_gmail_by_input_click("多結果子")
                # if search_success:
                #     print("✅ Gmail 搜尋和選取完成")
                # else:
                #     print("❌ Gmail 搜尋和選取失敗")
                    
                # if search_success:
                #     print("✅ UFO2 AppAgent Gmail 搜尋完成")
                #     print("📧 已在 Gmail 中搜尋關鍵字：多結果子")
                    
                #     # 額外等待時間讓搜尋結果完全載入
                #     print("⏳ 等待搜尋結果完全載入...")
                #     time.sleep(3)
                    
                # else:
                #     print("❌ UFO2 AppAgent Gmail 搜尋失敗")
                #     print("🔄 嘗試使用備用搜尋方法...")
                    
                #     # 備用方法：使用原有的搜尋功能
                #     backup_success = chrome_agent.select_gmail_emails_by_subject("多結果子")
                #     if backup_success:
                #         print("✅ 備用搜尋方法成功")
                #     else:
                #         print("❌ 備用搜尋方法也失敗")
            
                
            # 等待一段時間讓用戶觀察結果
            time.sleep(2)
            
        else:
            print("❌ Chrome 瀏覽器啟動失敗")
        
        # ===== 顯示操作摘要 =====
        #chrome_agent.print_summary()
        
        # ===== 成功完成提示 =====
        # print("\n✅ UFO2 Chrome 自動化流程執行完成！")
        # print("💡 Chrome 瀏覽器現在應該已經開啟並顯示 Gmail 收件箱")
        
    except Exception as e:
        # ===== 錯誤處理 =====
        print(f"❌ 操作失敗：{str(e)}")
        import traceback
        traceback.print_exc()
