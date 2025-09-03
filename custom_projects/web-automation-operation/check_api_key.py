"""
OpenAI API 金鑰驗證腳本
用於驗證 API 金鑰是否正確設定
"""

import os
import sys

def check_api_key():
    """檢查 OpenAI API 金鑰設定"""
    print("🔍 檢查 OpenAI API 金鑰設定...")
    print("=" * 50)
    
    # 檢查環境變數
    env_key = os.getenv('OPENAI_API_KEY')
    print(f"📍 環境變數 OPENAI_API_KEY: {'✅ 已設定' if env_key else '❌ 未設定'}")
    
    if env_key:
        if env_key.startswith('sk-'):
            print(f"🔑 API 金鑰格式: ✅ 正確 (sk-...)")
            print(f"📏 API 金鑰長度: {len(env_key)} 字符")
            print(f"👀 顯示部分金鑰: {env_key[:7]}...")
        else:
            print(f"❌ API 金鑰格式錯誤: 應以 'sk-' 開頭")
            print(f"👀 目前值: {env_key[:20]}...")
    
    # 檢查 .env 檔案
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    print(f"\n📄 .env 檔案: {'✅ 存在' if os.path.exists(env_file) else '❌ 不存在'}")
    
    if os.path.exists(env_file):
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'OPENAI_API_KEY=' in content:
                    for line in content.split('\n'):
                        if line.strip().startswith('OPENAI_API_KEY='):
                            env_value = line.strip().split('=', 1)[1].strip('"\'')
                            if env_value and env_value != '您的API金鑰':
                                print(f"🔑 .env 中的 API 金鑰: ✅ 已設定")
                                print(f"👀 顯示部分金鑰: {env_value[:7]}...")
                            else:
                                print(f"❌ .env 中的 API 金鑰未正確設定")
                            break
                else:
                    print(f"❌ .env 檔案中沒有 OPENAI_API_KEY 設定")
        except Exception as e:
            print(f"❌ 讀取 .env 檔案失敗: {e}")
    
    # 檢查 UFO2 配置檔案
    config_file = os.path.join(os.path.dirname(__file__), 'config.yaml')
    print(f"\n⚙️  UFO2 配置檔案: {'✅ 存在' if os.path.exists(config_file) else '❌ 不存在'}")
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'sk-YOUR_API_KEY_HERE' in content:
                    print(f"⚠️  UFO2 配置檔案中仍有預設 API 金鑰佔位符")
                else:
                    print(f"✅ UFO2 配置檔案已更新")
        except Exception as e:
            print(f"❌ 讀取 UFO2 配置檔案失敗: {e}")
    
    print("\n" + "=" * 50)
    
    # 總結和建議
    final_key = env_key
    if final_key and final_key.startswith('sk-'):
        print("🎉 API 金鑰設定正確！")
        print("💡 您現在可以執行: python task.py")
        
        # 簡單的 API 連接測試
        try_test = input("\n🧪 是否要測試 API 連接？(y/N): ").strip().lower()
        if try_test in ['y', 'yes']:
            test_api_connection(final_key)
            
    else:
        print("❌ API 金鑰未正確設定！")
        print("\n💡 解決方案:")
        print("1. 執行 setup_api_key.bat 腳本")
        print("2. 或手動執行: setx OPENAI_API_KEY \"您的API金鑰\"")
        print("3. 或編輯 .env 檔案")
        print("4. 然後重新啟動 VS Code")

def test_api_connection(api_key):
    """測試 API 連接"""
    print("\n🧪 測試 OpenAI API 連接...")
    
    try:
        import requests
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # 測試簡單的 API 請求
        response = requests.get(
            "https://api.openai.com/v1/models",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ API 連接成功！")
            models = response.json()
            gpt4_models = [m['id'] for m in models['data'] if 'gpt-4' in m['id']]
            print(f"🤖 可用的 GPT-4 模型: {len(gpt4_models)} 個")
            if gpt4_models:
                print(f"📋 模型範例: {gpt4_models[:3]}")
        elif response.status_code == 401:
            print("❌ API 金鑰無效或已過期")
        elif response.status_code == 429:
            print("⚠️  API 請求過於頻繁，請稍後再試")
        else:
            print(f"❌ API 請求失敗: {response.status_code}")
            
    except ImportError:
        print("⚠️  缺少 requests 模組，跳過 API 測試")
    except Exception as e:
        print(f"❌ API 測試失敗: {e}")

if __name__ == "__main__":
    check_api_key()
    
    print("\n📚 更多幫助請參考: API_KEY_SETUP.md")
    input("\n按 Enter 鍵結束...")
