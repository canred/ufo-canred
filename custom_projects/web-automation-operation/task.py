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
from ufo.module.basic import BaseSession
from ufo.config.config import Config
from ufo.agents.agent.host_agent import HostAgent, AgentFactory
from ufo.agents.agent.app_agent import AppAgent
from ufo.llm.llm_call import get_completion

# ===== UFO2 文件操作代理類別 =====
class UFO2FileAgent:
    def __init__(self):
        """
        初始化 UFO2 文件操作代理
        使用 UFO2 架構的基礎組件
        """
        self.file_content = None
        self.first_line = None
        self.session_data = {}
        
        # 初始化 UFO2 配置
        try:
            self.config = Config.get_instance().config_data
            print("✅ UFO2 配置已載入")
        except Exception as e:
            print(f"⚠️  UFO2 配置載入失敗，使用預設設定: {e}")
            self.config = {}
            
        # 初始化 Host Agent 用於專題報告生成
        try:
            self.host_agent = AgentFactory.create_agent(
                "host",
                "HostAgent",
                True,  # is_visual
                "",    # main_prompt
                "",    # example_prompt
                ""     # api_prompt
            )
            print("✅ UFO2 Host Agent 已初始化")
        except Exception as e:
            print(f"⚠️  Host Agent 初始化失敗: {e}")
            self.host_agent = None
            
        # 初始化 App Agent 用於 UI 自動化
        try:
            self.app_agent = AgentFactory.create_agent(
                "app",
                "AppAgent",
                True,  # is_visual
                "",    # main_prompt
                "",    # example_prompt
                ""     # api_prompt
            )
            print("✅ UFO2 App Agent 已初始化")
        except Exception as e:
            print(f"⚠️  App Agent 初始化失敗: {e}")
            self.app_agent = None

    def open_and_read_file(self, file_path):
        """
        開啟檔案並讀取第一行內容
        使用 UFO2 架構的檔案操作方式
        """
        try:
            # 檢查檔案是否存在
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"檔案 {file_path} 不存在")
            
            # 使用 UFO2 架構的檔案操作方式
            print(f"🔄 正在使用 UFO2 架構開啟檔案: {file_path}")
            
            # 記錄操作到 session 中（UFO2 風格）
            self.session_data['file_operation'] = {
                'action': 'open_file',
                'file_path': file_path,
                'timestamp': time.time()
            }
            
            # 讀取檔案內容
            with open(file_path, 'r', encoding='utf-8') as file:
                self.file_content = file.read()
                lines = self.file_content.splitlines()
                
                if lines:
                    self.first_line = lines[0]
                    print(f"✅ 成功讀取檔案第一行: {self.first_line}")
                    
                    # 更新 session 資料
                    self.session_data['file_operation']['result'] = 'success'
                    self.session_data['file_operation']['first_line'] = self.first_line
                    self.session_data['file_operation']['total_lines'] = len(lines)
                else:
                    self.first_line = ""
                    print("⚠️  檔案為空")
                    self.session_data['file_operation']['result'] = 'empty_file'
                    
            return self.first_line
            
        except Exception as e:
            error_msg = f"讀取檔案時發生錯誤: {str(e)}"
            print(f"❌ {error_msg}")
            
            # 記錄錯誤到 session
            self.session_data['file_operation']['result'] = 'error'
            self.session_data['file_operation']['error'] = str(e)
            
            raise

    def translate_with_host_agent(self, text):
        """
        使用 UFO2 Host Agent 進行中文專題報告生成
        """
        try:
            print(f"🤖 正在使用 UFO2 Host Agent 生成專題報告: {text}")
            
            # 構建專題報告生成請求的訊息（包含 'json' 關鍵字以符合 UFO2 要求）
            translation_prompt = [
                {
                    "role": "system",
                    "content": "您是一位專業的中文寫作專家。請根據提供的內容撰寫一篇結構完整的中文專題報告。報告格式要求：1)標題 2)前言/背景 3)主要內容分析 4)結論與建議。文字要流暢、邏輯清晰，適合作為專題報告使用，字數嚴格控制在200字以內。請以JSON格式回應，使用'article'作為key。"
                },
                {
                    "role": "user", 
                    "content": f"請根據以下內容撰寫一篇中文專題報告，包含完整結構，字數500字以內，以JSON格式返回：'{text}'"
                }
            ]
            
            # 使用 UFO2 的 LLM API 進行翻譯
            response, cost = get_completion(
                translation_prompt, 
                agent="HOST", 
                use_backup_engine=True
            )
            
            # 解析 JSON 回應並提取翻譯結果
            try:
                import json
                # 嘗試解析 JSON 回應
                if response.startswith('{') and response.endswith('}'):
                    response_json = json.loads(response)
                    translated_text = response_json.get('article', response_json.get('translation', response))
                else:
                    # 如果回應不是 JSON 格式，直接使用內容
                    translated_text = response
            except json.JSONDecodeError:
                # JSON 解析失敗時，直接使用回應內容
                translated_text = response
            except Exception:
                # 其他錯誤時，使用回應內容
                translated_text = response
            
            # 清理翻譯結果
            translated_text = str(translated_text).strip().strip('"').strip("'")
            
            # 格式化成本為小數3位
            formatted_cost = f"{float(cost):.3f}" if cost is not None else "0.000"
            
            print(f"✅ 專題報告生成完成: {translated_text}")
            print(f"💰 API 成本: ${formatted_cost}")
            
            # 記錄報告生成操作
            self.session_data['translation'] = {
                'original_text': text,
                'translated_text': translated_text,
                'timestamp': time.time(),
                'cost': float(cost) if cost is not None else 0.0
            }
            
            return translated_text
            
        except Exception as e:
            error_msg = f"專題報告生成失敗: {str(e)}"
            print(f"❌ {error_msg}")
            
            # 記錄報告生成錯誤
            self.session_data['translation'] = {
                'original_text': text,
                'result': 'error',
                'error': str(e),
                'timestamp': time.time(),
                'cost': 0.0
            }
            
            raise

    def write_to_file(self, file_path, content, append_mode=True):
        """
        使用 UFO2 AppAgent 控制 Notepad 創建新檔案並將內容寫入
        通過 UI 自動化的方式開啟空白 Notepad，輸入內容後保存為指定檔案
        """
        try:
            print(f"🤖 正在使用 UFO2 AppAgent 控制 Notepad 寫入檔案...")
            
            # 構建 AppAgent 的 UI 自動化請求
            automation_prompt = [
                {
                    "role": "system",
                    "content": "You are a UI automation assistant. Help control Windows applications like Notepad through keyboard and mouse actions. Respond in JSON format with 'actions' and 'status' as keys."
                },
                {
                    "role": "user",
                    "content": f"Open Notepad (blank), type the following content character by character: '{content}', then save the file as '{file_path}'. Return the automation steps in JSON format."
                }
            ]
            
            # 使用 UFO2 的 LLM API 來規劃 UI 自動化步驟
            response, cost = get_completion(
                automation_prompt,
                agent="APP",  # 使用 APP Agent
                use_backup_engine=True
            )
            
            print(f"🎯 AppAgent 規劃的自動化步驟: {response}")
            
            # 執行實際的 UI 自動化操作
            import subprocess
            import pyautogui
            import pyperclip  # 用於剪貼簿操作
            import time as sleep_time
            
            # 步驟1: 啟動 Notepad（不直接開啟檔案）
            print("📋 步驟1: 啟動 Notepad")
            subprocess.Popen(['notepad.exe'])  # 啟動空白的 Notepad
            sleep_time.sleep(1)  # 等待 Notepad 啟動（增加等待時間）
            
            # # 步驟1.5: 最大化 Notepad 視窗
            # print("🔍 步驟1.5: 最大化 Notepad 服務視窗")
            # # 使用 Alt+Tab 確保 Notepad 在前景
            # pyautogui.hotkey('alt', 'tab')
            # sleep_time.sleep(0.5)
            
            # # 使用 Windows 鍵 + 上箭頭最大化視窗
            # pyautogui.hotkey('win', 'up')
            # sleep_time.sleep(1)
            
            # # 或者使用 Alt+Space 然後 x 來最大化
            # pyautogui.hotkey('alt', 'space')
            # sleep_time.sleep(0.3)
            # pyautogui.press('x')  # x 代表最大化
            # sleep_time.sleep(1)

            print("✅ Notepad 視窗已最大化")
            
            # 步驟2: 確保 Notepad 視窗在前景並點擊文本編輯區域
            print("🔍 步驟2: 確保 Notepad 視窗在前景並點擊文本編輯區域")
            
            # 點擊 Notepad 的文本編輯區域以確保游標在正確位置
            # print("👆 點擊文本編輯區域以定位游標")
            # # 由於視窗已最大化，可以更精確地定位文本區域
            # screen_width, screen_height = pyautogui.size()
            # # 點擊螢幕中央偏上的位置（文本編輯區域）
            # click_x = screen_width // 2
            # click_y = screen_height // 3  # 偏上一些，避免點到狀態欄
            # pyautogui.click(click_x, click_y)
            # sleep_time.sleep(0.5)
            
            # print(f"🖱️  已點擊座標 ({click_x}, {click_y}) 以定位游標")
            
            # 步驟3: 確保文本編輯區域有焦點並準備輸入
            # print("⌨️ 步驟3: 確保文本編輯區域有焦點並準備輸入")
            
            # 使用 Tab 鍵確保焦點在文本編輯區域（如果焦點在菜單欄）
            # pyautogui.press('tab')
            # sleep_time.sleep(0.2)
            
            # 按 Ctrl+Home 確保游標在文件開頭
            pyautogui.hotkey('ctrl', 'home')
            sleep_time.sleep(0.2)
            
            # 測試輸入一個空格然後刪除，確認輸入功能正常
            print("🧪 測試輸入功能...")
            pyautogui.press('space')
            sleep_time.sleep(0.1)
            pyautogui.press('backspace')
            sleep_time.sleep(0.2)
            
            print("✅ 文本編輯區域已準備就緒")  
            
            # 使用剪貼簿方式逐字輸入中文內容（解決中文輸入問題）
            print("📋 使用剪貼簿方式逐字輸入中文內容...")
            
            # 設定輸入速度（可調整）- 批次處理提升速度
            chunk_size = 8  # 每次貼入的字符數量（5-10個字符）
            chunk_delay = 0.01  # 每批次間的延遲（秒）
            clipboard_delay = 0.005  # 剪貼簿更新延遲（秒）
            
            # 分批處理內容
            total_chars = len(content)
            for i in range(0, total_chars, chunk_size):
                # 取得當前批次的字符
                chunk = content[i:i + chunk_size]
                
                # 將批次字符複製到剪貼簿
                pyperclip.copy(chunk)
                sleep_time.sleep(clipboard_delay)  # 等待剪貼簿更新
                
                # 使用 Ctrl+V 貼上批次字符
                pyautogui.hotkey('ctrl', 'v')
                sleep_time.sleep(chunk_delay)  # 每個批次間的延遲
                
                # 每3個批次顯示進度（約24個字符）
                current_pos = min(i + chunk_size, total_chars)
                if (i // chunk_size + 1) % 3 == 0 or current_pos == total_chars:
                    print(f"📝 已輸入 {current_pos}/{total_chars} 個字符... (批次大小: {len(chunk)})")
            
            print(f"✅ 中文內容已通過剪貼簿逐字成功輸入 (共 {len(content)} 個字符)")
            
            # 步驟4: 保存檔案到指定路徑
            print("💾 步驟4: 保存檔案到指定路徑")
            pyautogui.hotkey('ctrl', 's')  # Ctrl+S 開啟保存對話框
            sleep_time.sleep(1)
            
            # 輸入檔案路徑和名稱
            print(f"📁 輸入檔案路徑: {file_path}")
            pyperclip.copy(file_path)  # 將檔案路徑複製到剪貼簿
            sleep_time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'v')  # 貼上檔案路徑
            sleep_time.sleep(0.5)
            
            # 按下 Enter 確認保存
            pyautogui.press('enter')
            sleep_time.sleep(1)
            
            # 格式化成本為小數3位
            formatted_cost = f"{float(cost):.3f}" if cost is not None else "0.000"
            
            print(f"✅ AppAgent 成功使用 Notepad 創建新檔案並寫入內容: {content}")
            print(f"💰 AppAgent API 成本: ${formatted_cost}")
            print(f"🎮 UI 自動化完成：已在新檔案中通過剪貼簿逐字輸入中文到 Notepad")
            
            # 記錄寫入操作（UFO2 AppAgent UI 自動化風格）
            self.session_data['write_operation'] = {
                'agent_type': 'AppAgent',
                'automation_type': 'UI_Automation',
                'target_app': 'Notepad',
                'action': 'create_new_file_via_clipboard',
                'file_path': file_path,
                'content': content,
                'append_mode': append_mode,
                'automation_steps': [
                    'Launch Notepad (blank)',
                    'Maximize Notepad window',
                    'Focus on text editing area',
                    'Click text area and position cursor',
                    'Test input functionality',
                    'Copy each character to clipboard',
                    'Paste character by character',
                    'Save file to specified path'
                ],
                'ai_response': response,
                'api_cost': float(cost) if cost is not None else 0.0,
                'timestamp': time.time(),
                'result': 'success'
            }
            
        except Exception as e:
            error_msg = f"AppAgent UI 自動化失敗: {str(e)}"
            print(f"❌ {error_msg}")
            
            # 記錄自動化錯誤
            self.session_data['write_operation'] = {
                'agent_type': 'AppAgent',
                'automation_type': 'UI_Automation',
                'target_app': 'Notepad',
                'action': 'create_new_file_via_clipboard',
                'result': 'error',
                'error': str(e),
                'api_cost': 0.0,
                'timestamp': time.time()
            }
            
            # 如果 UI 自動化失敗，回退到傳統檔案寫入
            print("🔄 回退到傳統檔案寫入方式...")
            try:
                mode = 'a' if append_mode else 'w'
                with open(file_path, mode, encoding='utf-8') as file:
                    if append_mode:
                        file.write('\n' + content)
                    else:
                        file.write(content)
                print(f"✅ 回退成功：已寫入檔案 {content}")
                self.session_data['write_operation']['fallback'] = 'traditional_file_write'
                self.session_data['write_operation']['result'] = 'success_with_fallback'
            except Exception as fallback_error:
                print(f"❌ 回退也失敗: {fallback_error}")
                raise

    def assign_to_variable(self, variable_name="assigned_variable"):
        """
        將第一行內容指派到指定變數
        UFO2 風格的變數管理
        """
        if self.first_line is not None:
            # 在 session 中記錄變數指派
            self.session_data['variable_assignment'] = {
                'variable_name': variable_name,
                'value': self.first_line,
                'type': type(self.first_line).__name__,
                'length': len(self.first_line) if self.first_line else 0,
                'timestamp': time.time()
            }
            
            print(f"📝 變數 '{variable_name}' 已成功指派: '{self.first_line}'")
            return self.first_line
        else:
            print("❌ 無法指派變數：尚未讀取檔案或檔案為空")
            return None

    def get_session_summary(self):
        """
        取得 UFO2 風格的 session 摘要
        """
        return {
            'session_type': 'UFO2_File_Operation_with_Article_Generation',
            'operations_performed': list(self.session_data.keys()),
            'session_data': self.session_data,
            'total_operations': len(self.session_data)
        }

    def display_file_info(self, file_path):
        """顯示檔案資訊（UFO2 風格的詳細報告）"""
        print("\n📊 === UFO2 檔案資訊報告 ===")
        
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"📁 檔案路徑: {file_path}")
            print(f"📏 檔案大小: {file_size} bytes")
            print(f"📄 第一行內容: {self.first_line}")
            
            # 顯示 session 統計
            if 'file_operation' in self.session_data:
                op_data = self.session_data['file_operation']
                print(f"🕐 操作時間: {time.ctime(op_data['timestamp'])}")
                print(f"✅ 操作結果: {op_data['result']}")
                if 'total_lines' in op_data:
                    print(f"📝 總行數: {op_data['total_lines']}")
        else:
            print(f"❌ 檔案 {file_path} 不存在")

# ============================= 主程式執行區 =============================
if __name__ == "__main__":
    print("🛸 === UFO2 檔案操作測試程式 ===")
    print(f"🗂️  UFO 框架路徑: {os.path.abspath(UFO_PATH)}")
    
    # 檢查配置檔案
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    if os.path.exists(config_path):
        print(f"⚙️  配置檔案: {config_path}")
    else:
        print("⚠️  注意：未找到配置檔案，使用預設設定")
    
    print("-" * 60)
    
    # ===== 初始化 UFO2 檔案操作代理 =====
    print("🚀 初始化 UFO2 檔案操作代理...")
    file_agent = UFO2FileAgent()
    
    try:
        # ===== 設定要開啟的檔案路徑 =====
        doc_file_path = os.path.join(os.path.dirname(__file__), "doc.txt")
        
        # ===== 執行 UFO2 檔案操作流程 =====
        print("\n🔄 開始執行 UFO2 檔案操作流程...")
        
        # 步驟1: 開啟 doc.txt 檔案並讀取第一行
        print("\n📖 步驟1: 讀取檔案第一行")
        first_line_content = file_agent.open_and_read_file(doc_file_path)
        
        # 步驟2: 將第一行內容指派到變數
        print("\n📝 步驟2: 指派變數")
        assigned_variable = file_agent.assign_to_variable("assigned_variable")
        
        # 步驟3: 使用 Host Agent 進行中文專題報告生成
        print("\n🌐 步驟3: 使用 UFO2 Host Agent 生成專題報告")
        if assigned_variable:
            translated_text = file_agent.translate_with_host_agent(assigned_variable)
        else:
            translated_text = ""
            print("⚠️  無法生成報告：變數為空")
        
        # 步驟4: 將專題報告寫入檔案的下一行
        print("\n💾 步驟4: 將專題報告寫入檔案")
        if translated_text:
            file_agent.write_to_file(doc_file_path, translated_text, append_mode=True)
            print(f"✅ 專題報告已寫入檔案: {translated_text}")
        else:
            print("⚠️  無法寫入：專題報告為空")
        
        # 步驟5: 顯示結果
        print("\n🎯 === UFO2 操作結果 ===")
        print(f"✅ 原始內容: '{assigned_variable}'")
        print(f"✅ 專題報告: '{translated_text}'")
        print(f"✅ 專題報告已追加到檔案中")
        
        # 步驟6: 顯示檔案資訊
        file_agent.display_file_info(doc_file_path)
        
        # ===== UFO2 風格的變數驗證 =====
        print(f"\n🔍 === UFO2 變數驗證 ===")
        session_summary = file_agent.get_session_summary()
        
        if 'variable_assignment' in session_summary['session_data']:
            var_data = session_summary['session_data']['variable_assignment']
            print(f"📊 變數名稱: {var_data['variable_name']}")
            print(f"💾 變數值: '{var_data['value']}'")
            print(f"🏷️  變數類型: {var_data['type']}")
            print(f"📏 變數長度: {var_data['length']}")
        
        # ===== UFO2 專題報告生成統計 =====
        if 'translation' in session_summary['session_data']:
            trans_data = session_summary['session_data']['translation']
            print(f"\n📝 === UFO2 專題報告生成統計 ===")
            print(f"📖 原始內容: {trans_data['original_text']}")
            print(f"📋 專題報告: {trans_data['translated_text']}")
            print(f"💰 成本: ${trans_data['cost']:.3f}")
            print(f"🕐 生成時間: {time.ctime(trans_data['timestamp'])}")
        
        # ===== UFO2 Session 摘要 =====
        print(f"\n📋 === UFO2 Session 摘要 ===")
        print(f"🔧 Session 類型: {session_summary['session_type']}")
        print(f"⚡ 執行的操作: {', '.join(session_summary['operations_performed'])}")
        print(f"📈 總操作數: {session_summary['total_operations']}")
        
        # ===== UFO2 AppAgent UI 自動化統計 =====
        if 'write_operation' in session_summary['session_data']:
            write_data = session_summary['session_data']['write_operation']
            print(f"\n💾 === UFO2 AppAgent UI 自動化統計 ===")
            print(f"🤖 代理類型: {write_data.get('agent_type', 'Unknown')}")
            print(f"🎮 自動化類型: {write_data.get('automation_type', 'N/A')}")
            print(f"�️  目標應用程式: {write_data.get('target_app', 'N/A')}")
            print(f"⌨️ 操作方式: {write_data.get('action', 'N/A')}")
            print(f"�📝 輸入內容: {write_data.get('content', 'N/A')}")
            print(f"📁 檔案路徑: {write_data.get('file_path', 'N/A')}")
            if 'automation_steps' in write_data:
                print(f"� 自動化步驟: {' → '.join(write_data['automation_steps'])}")
            print(f"💰 API 成本: ${write_data.get('api_cost', 0.0):.3f}")
            print(f"✅ 操作結果: {write_data.get('result', 'N/A')}")
            if 'fallback' in write_data:
                print(f"🔄 回退方式: {write_data['fallback']}")
            print(f"🕐 操作時間: {time.ctime(write_data['timestamp'])}")
        
        # ===== 檢查最終檔案內容 =====
        print(f"\n📄 === 最終檔案內容 ===")
        try:
            with open(doc_file_path, 'r', encoding='utf-8') as file:
                final_content = file.read()
                lines = final_content.splitlines()
                for i, line in enumerate(lines, 1):
                    print(f"第{i}行: {line}")
        except Exception as e:
            print(f"❌ 讀取最終檔案內容失敗: {e}")
        
        # ===== 成功完成提示 =====
        print("\n🎉 整個 UFO2 檔案操作流程執行完成！")
        print("✅ 檔案已成功開啟，第一行內容已指派到變數中")
        print("✅ 中文專題報告已成功生成")
        print("✅ 專題報告已寫入檔案下一行")
        print("🛸 UFO2 架構操作完成！")
        
    except Exception as e:
        # ===== 錯誤處理 =====
        print(f"\n❌ UFO2 操作失敗：{str(e)}")
        print("🔧 請檢查檔案路徑和權限設定")
        print("🔧 請確認 LLM 配置正確")
