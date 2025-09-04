# ===== 模組導入區 =====
import sys
import os
import time
import subprocess
import json
import asyncio
import autoit

# ===== 環境變數和路徑設定區 =====
def setup_environment():
    """設定環境變數和 Python 路徑"""
    print("🔧 設定執行環境...")
    
    # 1. 設定 UFO 框架路徑
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ufo_path = os.path.join(current_dir, "../..")
    ufo_path = os.path.abspath(ufo_path)
    
    print(f"📂 當前目錄: {current_dir}")
    print(f"📂 UFO 框架路徑: {ufo_path}")
    
    # 檢查 UFO 路徑是否存在
    if not os.path.exists(ufo_path):
        print(f"❌ UFO 框架路徑不存在: {ufo_path}")
        return False
    
    # 檢查關鍵 UFO 模組是否存在
    ufo_module_path = os.path.join(ufo_path, "ufo")
    if not os.path.exists(ufo_module_path):
        print(f"❌ UFO 模組目錄不存在: {ufo_module_path}")
        return False
    
    # 添加 UFO 路徑到 Python 路徑（如果還沒有的話）
    if ufo_path not in sys.path:
        sys.path.insert(0, ufo_path)
        print(f"✅ 已添加 UFO 路徑到 Python PATH: {ufo_path}")
    else:
        print(f"✅ UFO 路徑已在 Python PATH 中")
    
    # 2. 設定配置檔案路徑
    config_path = os.path.join(current_dir, 'config.yaml')
    config_path = os.path.abspath(config_path)
    
    print(f"📄 配置檔案路徑: {config_path}")
    
    # 檢查配置檔案是否存在
    if not os.path.exists(config_path):
        print(f"❌ 配置檔案不存在: {config_path}")
        return False
    
    # 設定 UFO 配置檔案環境變數
    os.environ['UFO_CONFIG_PATH'] = config_path
    print(f"✅ 已設定 UFO_CONFIG_PATH: {config_path}")
    
    # 3. 設定 PYTHONPATH 環境變數（確保子程序也能找到模組）
    pythonpath = os.environ.get('PYTHONPATH', '')
    paths_to_add = [ufo_path, current_dir]
    
    for path in paths_to_add:
        if path not in pythonpath:
            if pythonpath:
                pythonpath = f"{path};{pythonpath}"
            else:
                pythonpath = path
    
    os.environ['PYTHONPATH'] = pythonpath
    print(f"✅ 已設定 PYTHONPATH: {pythonpath}")
    
    # 4. 顯示 Python 路徑資訊
    print("📋 Python sys.path 前5項:")
    for i, path in enumerate(sys.path[:5]):
        print(f"   {i+1}. {path}")
    
    # 5. 驗證 UFO 模組是否可以導入
    try:
        # 先測試基本導入
        import ufo
        print("✅ UFO 模組導入成功")
        
        # 測試關鍵子模組
        from ufo.config.config import Config
        print("✅ UFO Config 模組導入成功")
        
        return True
        
    except ImportError as e:
        print(f"❌ UFO 模組導入失敗: {e}")
        print("💡 可能的解決方案:")
        print("   1. 檢查 UFO 框架是否正確安裝")
        print("   2. 檢查路徑設定是否正確")
        print("   3. 確認當前目錄結構是否正確")
        return False

# 執行環境設定
if not setup_environment():
    print("❌ 環境設定失敗，程式無法繼續執行")
    sys.exit(1)

# 注意：需要安裝 pyautogui 和 pyperclip 來進行 UI 自動化和剪貼簿操作
# 安裝命令：pip install pyautogui pyperclip

# 導入基本模組
import websockets
import requests
import base64
from datetime import datetime
from PIL import Image
import io

print("✅ 基本模組導入完成，開始導入 UFO2 模組...")

# 修復 UFO 框架配置檔案問題
def fix_ufo_config():
    """修復 UFO 框架內部的配置檔案 YAML 語法問題"""
    try:
        ufo_config_path = os.path.join(os.path.dirname(__file__), "../..", "ufo", "config", "config.yaml")
        ufo_config_path = os.path.abspath(ufo_config_path)
        
        if os.path.exists(ufo_config_path):
            print(f"🔧 檢查 UFO 框架配置檔案: {ufo_config_path}")
            
            # 讀取並檢查配置檔案
            with open(ufo_config_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 檢查是否包含語法錯誤的模式
            if '{' in content and '}' in content and ',' in content:
                print("⚠️  發現 UFO 配置檔案使用了錯誤的 YAML 語法，正在修復...")
                
                # 創建備份
                backup_path = ufo_config_path + '.backup'
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"📄 已建立備份檔案: {backup_path}")
                
                # 修復 YAML 語法（簡單的修復模式）
                fixed_content = content
                
                # 將 {key: value, key2: value2} 格式轉換為標準 YAML
                import re
                
                # 尋找並替換問題模式
                patterns = [
                    (r'(\w+):\s*{([^}]+)}', lambda m: fix_yaml_block(m.group(1), m.group(2))),
                ]
                
                for pattern, replacement in patterns:
                    fixed_content = re.sub(pattern, replacement, fixed_content, flags=re.MULTILINE | re.DOTALL)
                
                # 寫回修復後的內容
                with open(ufo_config_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                print("✅ UFO 配置檔案已修復")
                return True
            else:
                print("✅ UFO 配置檔案格式正常")
                return True
        else:
            print(f"⚠️  UFO 配置檔案不存在: {ufo_config_path}")
            return True  # 如果檔案不存在，繼續執行
            
    except Exception as e:
        print(f"⚠️  修復 UFO 配置檔案時發生錯誤: {e}")
        print("💡 將使用本地配置檔案繼續執行")
        return True  # 即使修復失敗，也繼續執行

def fix_yaml_block(key, content):
    """將 {key: value, key2: value2} 格式轉換為標準 YAML"""
    lines = [f"{key}:"]
    
    # 分割鍵值對
    pairs = content.split(',')
    for pair in pairs:
        pair = pair.strip()
        if ':' in pair:
            k, v = pair.split(':', 1)
            k = k.strip()
            v = v.strip()
            lines.append(f"  {k}: {v}")
    
    return '\n'.join(lines)

# 執行 UFO 配置修復
fix_ufo_config()

# 導入 UFO2 基本模組（在環境設定後）
try:
    from ufo.module.basic import BaseSession
    from ufo.config.config import Config
    from ufo.agents.agent.host_agent import HostAgent, AgentFactory
    from ufo.agents.agent.app_agent import AppAgent
    from ufo.llm.llm_call import get_completion
    from ufo.module.sessions.session import SessionFactory
    from ufo.module.context import Context, ContextNames
    from ufo.automator.ui_control.inspector import ControlInspectorFacade
    from ufo import utils
    print("✅ UFO2 模組導入成功")
except ImportError as e:
    print(f"❌ UFO2 模組導入失敗: {e}")
    print("💡 請確認環境設定是否正確")
    sys.exit(1)
except Exception as e:
    print(f"❌ UFO2 模組載入時發生錯誤: {e}")
    print("💡 這可能是配置檔案問題，嘗試使用替代方案...")
    
    # 如果還是有問題，嘗試直接設定配置
    try:
        print("🔄 嘗試直接設定 UFO 配置...")
        
        # 先導入基本的配置模組
        import yaml
        
        # 直接使用我們的配置檔案
        local_config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
        with open(local_config_path, 'r', encoding='utf-8') as f:
            local_config = yaml.safe_load(f)
        
        # 創建最小必要的導入
        from ufo.config.config import Config
        
        # 手動設定配置
        config_instance = Config.get_instance()
        config_instance.config_data = local_config
        
        print("✅ 使用本地配置檔案成功設定 UFO")
        
        # 現在導入其他模組
        from ufo.agents.agent.host_agent import HostAgent, AgentFactory
        from ufo.llm.llm_call import get_completion
        from ufo import utils
        
        print("✅ UFO2 核心模組導入成功（使用本地配置）")
        
    except Exception as e2:
        print(f"❌ 替代方案也失敗: {e2}")
        print("💡 請檢查 UFO 框架安裝是否完整")
        sys.exit(1)


def find_text_input_box(target_window_title, input_box_class="編輯"):
    """
    打开目标窗口并定位文字输入框
    :param target_window_title: 目标窗口标题（如“无标题 - 记事本”）
    :param input_box_class: 文字输入框的控件类名（默认“Edit”，多数输入框通用）
    :return: 输入框信息字典（坐标、尺寸、状态）或错误信息
    """
    try:
        # 1. 打开目标窗口（以记事本为例，其他窗口替换为对应启动命令）
        print(f"正在打开目标窗口：{target_window_title}")
        autoit.run("notepad.exe")  # 启动记事本，其他程序替换为路径（如"E:\App\XXX.exe"）
        time.sleep(2)  # 等待窗口完全打开（根据程序启动速度调整时间）
            # 2. 检查窗口是否成功打开并激活
        if not autoit.win_exists(target_window_title):
            return {"status": "fail", "msg": f"窗口「{target_window_title}」未找到，请检查窗口标题或启动命令"}
        autoit.win_activate(target_window_title)  # 激活窗口（确保控件可识别）
        time.sleep(1)

        # 3. 定位文字输入框（通过“窗口标题+控件类名”精准匹配，INSTANCE=1表示第一个匹配的控件）
        #input_box_identifier = f"CLASS:{input_box_class};INSTANCE:1"
        input_box_identifier = f"[CLASS:Microsoft.UI.Content.DesktopChildSiteBridge; INSTANCE:4]"
        input_box_identifier = f"[CLASS:RichEditD2DPT; INSTANCE:1]"
        # 检查输入框是否存在 - 使用 control_get_handle 来检查控件是否存在
        try:
            print(f"🔍 正在獲取視窗句柄...")
            window_handle = autoit.win_get_handle(target_window_title)
            print(f"📋 視窗句柄獲取成功: {window_handle}")
            
            if not window_handle or window_handle == 0:
                return {"status": "fail", "msg": f"無法獲取視窗句柄: {target_window_title}"}
            
            print(f"🔍 正在獲取控件句柄: {input_box_identifier}")
            control_handle = autoit.control_get_handle(window_handle, input_box_identifier)
            print(f"📋 控件句柄獲取結果: {control_handle}")
            
            if not control_handle or control_handle == 0:
                # 嘗試列出視窗中的所有控件以幫助調試
                try:
                    print("🔍 嘗試列出視窗中的控件...")
                    class_list = autoit.win_get_class_list(window_handle)
                    print(f"📋 視窗控件類別列表: {class_list}")
                except Exception as list_error:
                    print(f"⚠️  無法列出控件: {list_error}")
                
                return {"status": "fail", "msg": f"在窗口「{target_window_title}」中未找到控件「{input_box_identifier}」"}
                
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            print(f"❌ 獲取句柄時發生異常:")
            print(f"   異常類型: {type(e).__name__}")
            print(f"   異常訊息: {str(e)}")
            print(f"   詳細追蹤: {error_detail}")
            return {"status": "fail", "msg": f"在窗口「{target_window_title}」中未找到「{input_box_class}」类的文字输入框: {str(e)}", "traceback": error_detail}

        # 4. 获取输入框的关键信息（坐标、尺寸、当前文本）
        # 添加詳細的驗證和錯誤處理
        print(f"📋 視窗句柄: {window_handle}")
        print(f"📋 控件識別符: {input_box_identifier}")
        
        # 驗證視窗句柄是否有效
        if not window_handle or window_handle == 0:
            return {"status": "fail", "msg": f"無效的視窗句柄: {window_handle}"}
        
        # 驗證控件句柄是否有效
        if not control_handle or control_handle == 0:
            return {"status": "fail", "msg": f"無效的控件句柄: {control_handle}"}
        
        print(f"📋 控件句柄: {control_handle}")
        
        # 嘗試點擊控件（使用控件句柄而不是識別符）
        try:
            print("🖱️  嘗試點擊控件...")
            # 使用 control_click_by_handle 替代 control_click
            autoit.control_click_by_handle(window_handle, control_handle)
            print("✅ 控件點擊成功")
        except Exception as click_error:
            print(f"⚠️  控件點擊失敗: {click_error}")
            # 如果點擊失敗，嘗試其他方法設置焦點
            try:
                print("🔄 嘗試使用 control_focus...")
                autoit.control_focus_by_handle(window_handle, control_handle)
                print("✅ 控件焦點設置成功")
            except Exception as focus_error:
                print(f"⚠️  設置焦點也失敗: {focus_error}")
                # 繼續執行，但記錄警告
        
        time.sleep(0.5)  # 等待控件響應
        
        # input_box_x, input_box_y, input_box_width, input_box_height = autoit.control_get_pos(
        #     window_handle,
        #     input_box_identifier
        # )
        # # 获取输入框当前文本（可选）
        # input_box_current_text = autoit.control_get_text(
        #     window_handle,
        #     input_box_identifier
        # )

        # 5. （可选）操作输入框：清空原有文本并输入新内容
        try:
            print("⌨️  嘗試設置控件文本...")
            # 使用 control_set_text_by_handle 替代 control_set_text
            autoit.control_set_text_by_handle(
                window_handle,
                control_handle,
                "这是通过Python+autoit输入的文本"
            )
            print("✅ 文本設置成功")
        except Exception as set_text_error:
            print(f"⚠️  設置文本失敗: {set_text_error}")
            # 嘗試使用 send 命令作為備用方案
            try:
                print("🔄 嘗試使用 send 命令...")
                # 先確保控件有焦點，然後發送文本
                autoit.control_focus_by_handle(window_handle, control_handle)
                time.sleep(0.2)
                autoit.send("^a")  # Ctrl+A 全選
                time.sleep(0.1)
                autoit.send("这是通过Python+autoit输入的文本")
                print("✅ 使用 send 命令設置文本成功")
            except Exception as send_error:
                print(f"⚠️  send 命令也失敗: {send_error}")
                # 記錄錯誤但繼續執行

        # 6. 返回成功结果
        return {
            "status": "success",
            "window_title": target_window_title,
            # "input_box_info": {
            #     "class": input_box_class,
            #     "position": (input_box_x, input_box_y),  # 输入框左上角坐标
            #     "size": (input_box_width, input_box_height),  # 输入框宽高
            #     "current_text": input_box_current_text  # 操作前的文本（若需保留可注释set_text）
            # }
        }

    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"❌ find_text_input_box 執行異常:")
        print(f"   異常類型: {type(e).__name__}")
        print(f"   異常訊息: {str(e)}")
        print(f"   詳細追蹤:")
        print(error_traceback)
        return {
            "status": "fail", 
            "msg": f"执行出错：{str(e)}",
            "error_type": type(e).__name__,
            "traceback": error_traceback
        }

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
                "--remote-debugging-port=9222",  # 啟用調試端口
                # "--user-data-dir=C:\\ChromeDebugProfile",  # 指定用戶數據目錄
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
    
    def ensure_chrome_window_active(self):
        """
        確保 Chrome 視窗處於活動狀態
        """
        try:
            chrome_window = self._find_chrome_window()
            if chrome_window:
                # 檢查視窗是否已經是活動視窗
                try:
                    # 使用 set_focus 方法激活視窗
                    chrome_window.set_focus()
                    time.sleep(0.2)  # 短暫等待確保視窗獲得焦點
                    print(f"✅ Chrome 視窗已激活: {chrome_window.window_text()}")
                    return True
                except Exception as e:
                    print(f"⚠️  使用 set_focus 激活失敗，嘗試其他方法: {e}")
                    
                    # 備用方法：如果視窗有 activate 方法
                    try:
                        if hasattr(chrome_window, 'activate'):
                            chrome_window.activate()
                            time.sleep(0.2)
                            print("✅ 使用 activate 方法成功激活 Chrome 視窗")
                            return True
                    except Exception as e2:
                        print(f"⚠️  activate 方法也失敗: {e2}")
                    
                    # 最後備用方法：使用 pyautogui 點擊視窗
                    try:
                        import pyautogui
                        # 獲取視窗矩形區域
                        rect = chrome_window.rectangle()
                        center_x = (rect.left + rect.right) // 2
                        center_y = (rect.top + rect.bottom) // 2
                        
                        # 點擊視窗中心來激活
                        pyautogui.click(center_x, center_y)
                        time.sleep(0.2)
                        print("✅ 使用滑鼠點擊成功激活 Chrome 視窗")
                        return True
                    except Exception as e3:
                        print(f"⚠️  滑鼠點擊激活也失敗: {e3}")
                        return False
            else:
                print("❌ 未找到 Chrome 視窗")
                return False
        except Exception as e:
            print(f"❌ 確保 Chrome 視窗活動時發生錯誤: {e}")
            return False
    
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
        
        if 'screenshot_operation' in self.session_data:
            screenshot_data = self.session_data['screenshot_operation']
            print(f"\n📸 螢幕截圖和 UFO2 OCR 操作:")
            print(f"   操作類型: {screenshot_data.get('operation_type', 'N/A')}")
            print(f"   狀態: {screenshot_data.get('status', 'N/A')}")
            
            if 'screenshot_path' in screenshot_data:
                print(f"   截圖檔案: {screenshot_data['screenshot_path']}")
            if 'screenshot_saved' in screenshot_data:
                print(f"   截圖已保存: {screenshot_data['screenshot_saved']}")
            if 'ocr_completed' in screenshot_data:
                print(f"   UFO2 OCR 已完成: {screenshot_data['ocr_completed']}")
            if 'ocr_method' in screenshot_data:
                print(f"   OCR 方法: {screenshot_data['ocr_method']}")
            if 'ocr_cost' in screenshot_data:
                print(f"   UFO2 OCR 成本: ${screenshot_data['ocr_cost']:.4f}")
            if 'error' in screenshot_data:
                print(f"   錯誤: {screenshot_data['error']}")
            if 'ocr_error' in screenshot_data:
                print(f"   UFO2 OCR 錯誤: {screenshot_data['ocr_error']}")
        
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

    async def check_navigation(self):
        """
        檢查頁面導航狀態
        使用 Chrome DevTools Protocol 驗證頁面載入和 URL 跳轉
        """
        try:
            print("🔍 檢查頁面導航狀態...")
            
            # 1. 获取目标标签页的调试链接
            try:
                response = requests.get("http://localhost:9222/json", timeout=5)
                tabs = response.json()
            except requests.RequestException as e:
                print(f"❌ 無法連接到 Chrome 調試端口: {e}")
                return False
            
            # 尋找包含 Gmail 關鍵字的標籤頁
            target_tab = None
            for tab in tabs:
                url = tab.get("url", "")
                if any(keyword in url.lower() for keyword in ["mail.google.com", "gmail"]):
                    target_tab = tab
                    break
            
            if not target_tab:
                print("❌ 未找到 Gmail 標籤頁")
                return False
                
            print(f"✅ 找到目標標籤頁: {target_tab['url']}")
            ws_url = target_tab["webSocketDebuggerUrl"]

            # 2. 连接调试接口，验证跳转
            async with websockets.connect(ws_url) as ws:
                # 启用页面事件
                await ws.send(json.dumps({"id": 1, "method": "Page.enable"}))
                response = await ws.recv()
                print(f"📄 Page.enable 響應: {json.loads(response).get('result', 'OK')}")
                
                # 启用运行时
                await ws.send(json.dumps({"id": 2, "method": "Runtime.enable"}))
                await ws.recv()
                
                # 設置超時機制，避免無限等待
                timeout_seconds = 10
                start_time = time.time()
                page_loaded = False
                
                print("⏳ 等待頁面載入完成事件...")
                
                # 等待页面加载完成事件
                while time.time() - start_time < timeout_seconds:
                    try:
                        # 設置較短的超時，避免阻塞
                        message = await asyncio.wait_for(ws.recv(), timeout=1.0)
                        message_data = json.loads(message)
                        
                        # 檢查是否為頁面載入完成事件
                        method = message_data.get("method", "")
                        if method in ["Page.domContentEventFired", "Page.loadEventFired"]:
                            print(f"✅ 頁面載入事件已觸發: {method}")
                            page_loaded = True
                            break
                            
                    except asyncio.TimeoutError:
                        # 沒有收到事件，繼續等待
                        continue
                    except json.JSONDecodeError:
                        # 忽略無效的 JSON 訊息
                        continue
                
                # 如果沒有等到載入事件，也繼續檢查 URL
                if not page_loaded:
                    print("⚠️  未收到頁面載入事件，但繼續檢查 URL")
                
                # 3. 获取当前URL并验证
                await ws.send(json.dumps({
                    "id": 3, "method": "Runtime.evaluate",
                    "params": {"expression": "window.location.href"}
                }))
                result = await ws.recv()
                result_data = json.loads(result)
                
                if "result" in result_data and "result" in result_data["result"]:
                    current_url = result_data["result"]["result"]["value"]
                    print(f"🌐 當前 URL: {current_url}")
                    
                    # 檢查是否為預期的 Gmail 相關 URL
                    expected_keywords = ["mail.google.com", "gmail"]
                    if any(keyword in current_url.lower() for keyword in expected_keywords):
                        print("✅ 頁面導航成功 - URL 驗證通過")
                        return True
                    else:
                        print(f"❌ 頁面導航失敗 - 當前URL不符合預期: {current_url}")
                        return False
                else:
                    print("❌ 無法獲取當前 URL")
                    print(f"調試資訊: {result_data}")
                    return False
                    
        except websockets.exceptions.ConnectionClosed as e:
            print(f"❌ WebSocket 連接已關閉: {e}")
            return False
        except websockets.exceptions.WebSocketException as e:
            print(f"❌ WebSocket 連接錯誤: {e}")
            return False
        except Exception as e:
            print(f"❌ 檢查導航時發生錯誤: {e}")
            import traceback
            traceback.print_exc()
            return False

    
    def _perform_ufo2_ocr(self, image):
        """
        使用 UFO2 框架的 LLM 進行 OCR 辨識
        
        參數:
            image (PIL.Image): 要進行 OCR 的圖片
            
        返回:
            dict: OCR 結果
        """
        try:
            print("🤖 正在使用 UFO2 LLM 進行 OCR 辨識...")
            
            # 將圖片轉換為 base64 格式
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
            # 構建 UFO2 LLM 請求，使用視覺分析提示
            ocr_prompt = [
                {
                    "role": "system", 
                    "content": """您是一個專業的螢幕截圖分析助手，專門協助分析 Gmail 自動化操作的螢幕截圖。
                    請詳細分析提供的螢幕截圖並提取所有可見的文字內容和 UI 元素資訊。"""
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """請仔細分析這張螢幕截圖並提供以下資訊：

1. **文字內容提取**：
   - 提取所有可見的文字內容
   - 包括按鈕文字、連結文字、標題等

2. **Gmail 相關內容**（如果適用）：
   - 郵件主題和內容
   - 寄件者資訊
   - 收件匣狀態
   - 郵件數量
   - 選取狀態

3. **UI 元素分析**：
   - 按鈕位置和文字
   - 輸入框內容
   - 選單項目
   - 導航元素

4. **自動化操作建議**：
   - 可點擊的元素
   - 表單填寫狀態
   - 操作完成狀態

請以結構化的方式提供分析結果。"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{img_base64}",
                                "detail": "high"
                            }
                        }
                    ]
                }
            ]
            
            # 使用 UFO2 的 get_completion 函數進行 LLM 調用
            print("📡 發送請求到 UFO2 LLM...")
            try:
                response, cost = get_completion(
                    ocr_prompt,
                    agent="APP",  # 使用 APP Agent 進行視覺分析
                    use_backup_engine=True
                )
                
                formatted_cost = f"{float(cost):.4f}" if cost is not None else "0.0000"
                print(f"✅ UFO2 OCR 分析完成")
                print(f"💰 UFO2 LLM 成本: ${formatted_cost}")
                
                return {
                    'success': True,
                    'text': response,
                    'cost': float(cost) if cost is not None else 0.0,
                    'method': 'UFO2_LLM'
                }
                
            except Exception as e:
                print(f"⚠️  UFO2 LLM 調用失敗，嘗試使用備用方法: {e}")
                
                # 備用方法：直接使用 OpenAI API（如果 UFO2 LLM 失敗）
                return self._perform_backup_ocr(image)
                
        except Exception as e:
            error_msg = f"UFO2 OCR 處理失敗: {str(e)}"
            print(f"❌ {error_msg}")
            return {'success': False, 'error': error_msg}
    
    def _perform_backup_ocr(self, image):
        """
        備用 OCR 方法：直接使用 OpenAI API
        當 UFO2 LLM 不可用時使用
        
        參數:
            image (PIL.Image): 要進行 OCR 的圖片
            
        返回:
            dict: OCR 結果
        """
        try:
            print("🔄 使用備用 OpenAI API 進行 OCR...")
            
            # 將圖片轉換為 base64 格式
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
            # 嘗試從多個來源獲取 API 金鑰
            api_key = None
            
            # 方法1: 檢查環境變數（優先）
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key and api_key.startswith('sk-'):
                print("✅ 從環境變數 OPENAI_API_KEY 獲取到 API 金鑰")
            else:
                print("🔍 環境變數中未找到有效的 OPENAI_API_KEY")
                
            # 方法2: 檢查 UFO2 配置檔案
            if not api_key or api_key == "sk-YOUR_API_KEY_HERE":
                try:
                    if self.config:
                        # 檢查各個 Agent 的配置
                        for agent_name in ['HOST_AGENT', 'APP_AGENT', 'EVALUATION_AGENT']:
                            agent_config = self.config.get(agent_name, {})
                            config_key = agent_config.get('API_KEY')
                            if config_key and config_key != "sk-YOUR_API_KEY_HERE" and config_key.startswith('sk-'):
                                api_key = config_key
                                print(f"✅ 從 UFO2 配置 {agent_name} 獲取到 API 金鑰")
                                break
                        
                        # 如果還沒找到，檢查頂層配置
                        if not api_key or api_key == "sk-YOUR_API_KEY_HERE":
                            config_keys = ['OPENAI_API_KEY', 'API_KEY']
                            for key in config_keys:
                                config_value = self.config.get(key)
                                if config_value and config_value != "sk-YOUR_API_KEY_HERE" and config_value.startswith('sk-'):
                                    api_key = config_value
                                    print(f"✅ 從 UFO2 配置 {key} 獲取到 API 金鑰")
                                    break
                except Exception as e:
                    print(f"⚠️  讀取 UFO2 配置失敗: {e}")
            
            # 方法3: 檢查是否有 .env 檔案
            if not api_key or api_key == "sk-YOUR_API_KEY_HERE":
                env_file = os.path.join(os.path.dirname(__file__), '.env')
                if os.path.exists(env_file):
                    try:
                        with open(env_file, 'r', encoding='utf-8') as f:
                            for line in f:
                                if line.strip().startswith('OPENAI_API_KEY='):
                                    env_key = line.strip().split('=', 1)[1].strip('"\'')
                                    if env_key.startswith('sk-'):
                                        api_key = env_key
                                        print("✅ 從 .env 檔案獲取到 API 金鑰")
                                        break
                    except Exception as e:
                        print(f"⚠️  讀取 .env 檔案失敗: {e}")
                    
            # 最終檢查
            if not api_key or api_key == "sk-YOUR_API_KEY_HERE":
                error_msg = """❌ API 金鑰未設定或無效！

請使用以下任一方法設定您的 OpenAI API 金鑰：

方法1 (推薦): 設定環境變數
   在 Windows 中執行：
   setx OPENAI_API_KEY "您的_API_金鑰"
   
   或執行我們提供的腳本：
   setup_api_key.bat

方法2: 在 UFO2 配置檔案中設定
   編輯 config.yaml 檔案，將以下行：
   API_KEY: "sk-YOUR_API_KEY_HERE"
   替換為：
   API_KEY: "您的真實API金鑰"

方法3: 創建 .env 檔案
   在專案目錄建立 .env 檔案，內容：
   OPENAI_API_KEY=您的API金鑰

💡 API 金鑰格式：sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
💡 獲取 API 金鑰：https://platform.openai.com/api-keys"""
                
                print(error_msg)
                return {
                    'success': False,
                    'error': 'API 金鑰未設定。請參考上述說明設定 API 金鑰。'
                }
            
            print(f"🔑 使用 API 金鑰: {api_key[:7]}...")  # 只顯示前7個字符用於驗證
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            payload = {
                "model": "gpt-4o",  # 使用最新的 GPT-4 Vision 模型
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "請分析這張螢幕截圖並提取所有可見的文字內容。請詳細描述你看到的內容，包括任何按鈕、連結、輸入框和其他 UI 元素。特別關注 Gmail 相關的內容，如郵件主題、寄件者、收件匣狀態等。"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{img_base64}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 1000
            }
            
            # 發送請求到 OpenAI
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                response_data = response.json()
                ocr_text = response_data['choices'][0]['message']['content']
                
                # 計算成本（估算）
                usage = response_data.get('usage', {})
                prompt_tokens = usage.get('prompt_tokens', 0)
                completion_tokens = usage.get('completion_tokens', 0)
                cost = (prompt_tokens * 0.01 + completion_tokens * 0.03) / 1000
                
                print(f"✅ 備用 OCR 完成，使用 tokens: {prompt_tokens + completion_tokens}")
                print(f"💰 估算成本: ${cost:.4f}")
                
                return {
                    'success': True,
                    'text': ocr_text,
                    'cost': cost,
                    'tokens_used': prompt_tokens + completion_tokens,
                    'method': 'Backup_OpenAI_API'
                }
            else:
                error_msg = f"OpenAI API 請求失敗: {response.status_code} - {response.text}"
                print(f"❌ {error_msg}")
                return {'success': False, 'error': error_msg}
                
        except Exception as e:
            error_msg = f"備用 OCR 處理失敗: {str(e)}"
            print(f"❌ {error_msg}")
            return {'success': False, 'error': error_msg}
                
# ============================= 主程式執行區 =============================
"""
AutoIt 協同範例：
1. 直接呼叫 .au3 腳本（需安裝 AutoIt 並設置 au3 腳本關聯）
2. 使用 pyautoit 套件直接操作 AutoIt（需 pip install pyautoit）
"""

def run_autoit_au3():
    """
    執行 AutoIt .au3 腳本（需已安裝 AutoIt 並設置 au3 腳本關聯）
    """
    au3_path = os.path.join(os.path.dirname(__file__), "autoit_demo.au3")
    if not os.path.exists(au3_path):
        print(f"❌ 找不到 AutoIt 腳本: {au3_path}")
        return False
    print(f"🚀 執行 AutoIt au3 腳本: {au3_path}")
    # Windows 下可直接用 start 命令呼叫
    os.system(f'start "" "{au3_path}"')
    return True

def autoit_py_demo():
    """
    使用 autoit 控制視窗（原本需要 pyautoit，現在使用 autoit）
    """
    try:
        # 不需要額外導入，autoit 已經在頂部導入
        pass
    except ImportError:
        print("❌ autoit 模組未找到")
        return False
    # 範例：啟動記事本並輸入文字
    autoit.run("notepad.exe")
    autoit.win_wait_active("無標題 - 記事本", 5)
    autoit.send("這是 UFO2 + AutoIt 範例!{ENTER}")
    print("✅ autoit 操作完成")
    return True
if __name__ == "__main__":
    print("=== UFO2 Chrome 瀏覽器自動化程式 ===")
    
    # 顯示路徑資訊
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ufo_path = os.path.join(current_dir, "../..")
    ufo_path = os.path.abspath(ufo_path)
    print(f"UFO 框架路徑: {ufo_path}")    
    
    # 檢查配置檔案
    config_path = os.path.join(current_dir, 'config.yaml')
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
            time.sleep(2)  # 給 Gmail 更多時間載入
            
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
                
                # 使用 autoit portable 執行 mouse 移動到 (600,600)
                import subprocess
                autoit_exe = os.path.join(os.path.dirname(__file__), 'autoit', 'AutoIt3.exe')
                au3_script = os.path.join(os.path.dirname(__file__), 'autoit', 'move_mouse_600_600.au3')
                
                if not os.path.exists(autoit_exe):
                    print(f"❌ 找不到 AutoIt3.exe: {autoit_exe}")
                elif not os.path.exists(au3_script):
                    # 自動產生一個簡單的 au3 腳本
                    with open(au3_script, 'w', encoding='utf-8') as f:
                        f.write("MouseMove(600, 600, 0)\n")
                    print(f"✅ 已自動產生 {au3_script}")
                # 執行 au3 腳本
                print(f"🚀 執行 AutoIt 移動滑鼠腳本: {au3_script}")
                subprocess.Popen([autoit_exe, au3_script])
                
                # # 配置目标窗口参数（需根据你的实际需求修改！）
                TARGET_WINDOW = "无标题 - Notepad"  # 目标窗口标题（用AutoIT Window Info工具查看）
                INPUT_BOX_CLASS = "Edit"  # 文字输入框类名（默认“Edit”，多数程序通用，特殊情况需修改）
                # 执行定位逻辑
                result = find_text_input_box(TARGET_WINDOW, INPUT_BOX_CLASS)
            
        else:
            print("❌ Chrome 瀏覽器啟動失敗")
        
    except Exception as e:
        # ===== 錯誤處理 =====
        print(f"❌ 操作失敗：{str(e)}")
        import traceback
        traceback.print_exc()
