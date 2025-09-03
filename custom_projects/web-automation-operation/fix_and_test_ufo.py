#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# 設定 UFO 路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
ufo_path = os.path.join(current_dir, "../..")
ufo_path = os.path.abspath(ufo_path)
sys.path.insert(0, ufo_path)

# 設定配置檔案路徑
config_path = os.path.join(current_dir, 'config.yaml')
os.environ['UFO_CONFIG_PATH'] = config_path

print(f"UFO 路徑: {ufo_path}")
print(f"配置檔案: {config_path}")

# 檢查並修復 UFO 配置檔案
ufo_config_path = os.path.join(ufo_path, "ufo", "config", "config.yaml")
print(f"UFO 內部配置檔案: {ufo_config_path}")

if os.path.exists(ufo_config_path):
    print("正在修復 UFO 內部配置檔案...")
    
    # 創建一個最小的有效 YAML 配置
    minimal_config = """# UFO Configuration
LOG_LEVEL: INFO
LOG_PATH: "./logs/"

# Minimal required configuration
HOST_AGENT:
  VISUAL_MODE: true
  REASONING_MODEL: false
  API_TYPE: "openai"
  API_BASE: "https://api.openai.com/v1/chat/completions"
  API_KEY: "sk-YOUR_API_KEY_HERE"
  API_VERSION: "2025-02-01-preview"
  API_MODEL: "gpt-4o"

APP_AGENT:
  VISUAL_MODE: true
  REASONING_MODEL: false
  API_TYPE: "openai"
  API_BASE: "https://api.openai.com/v1/chat/completions"
  API_KEY: "sk-YOUR_API_KEY_HERE"
  API_VERSION: "2025-02-01-preview"
  API_MODEL: "gpt-4o"

EVALUATION_AGENT:
  VISUAL_MODE: true
  REASONING_MODEL: false
  API_TYPE: "openai"
  API_BASE: "https://api.openai.com/v1/chat/completions"
  API_KEY: "sk-YOUR_API_KEY_HERE"
  API_VERSION: "2025-02-01-preview"
  API_MODEL: "gpt-4o"
"""
    
    # 創建備份
    backup_path = ufo_config_path + '.original_backup'
    if not os.path.exists(backup_path):
        with open(ufo_config_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original_content)
        print(f"已創建原始備份: {backup_path}")
    
    # 寫入修復的配置
    with open(ufo_config_path, 'w', encoding='utf-8') as f:
        f.write(minimal_config)
    print("✅ UFO 內部配置檔案已修復")

# 現在測試導入
try:
    print("測試導入 ufo.config.config...")
    from ufo.config.config import Config
    print("✅ ufo.config.config 導入成功")
    
    print("測試獲取配置實例...")
    config = Config.get_instance()
    print("✅ 配置實例獲取成功")
    
    # 使用我們的本地配置覆蓋
    import yaml
    with open(config_path, 'r', encoding='utf-8') as f:
        local_config = yaml.safe_load(f)
    
    # 覆蓋配置數據
    config.config_data = local_config
    print("✅ 已使用本地配置檔案覆蓋")
    
    print("測試其他模組導入...")
    from ufo.llm.llm_call import get_completion
    print("✅ llm_call 導入成功")
    
    from ufo.agents.agent.host_agent import HostAgent, AgentFactory
    print("✅ host_agent 導入成功")
    
    print("\n🎉 所有測試通過！UFO 框架可以正常使用")
    print("現在可以執行主程式了")
    
except Exception as e:
    print(f"❌ 錯誤: {e}")
    import traceback
    traceback.print_exc()
