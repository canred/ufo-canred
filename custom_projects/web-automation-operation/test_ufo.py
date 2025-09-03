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

# 測試基本導入
try:
    print("測試導入 ufo 模組...")
    import ufo
    print("✅ ufo 模組導入成功")
    
    print("測試導入 ufo.config.config...")
    from ufo.config.config import Config
    print("✅ ufo.config.config 導入成功")
    
    print("測試獲取配置實例...")
    config = Config.get_instance()
    print("✅ 配置實例獲取成功")
    
    print("測試獲取配置數據...")
    config_data = config.config_data
    print(f"✅ 配置數據獲取成功: {type(config_data)}")
    
    print("測試導入其他模組...")
    from ufo.llm.llm_call import get_completion
    print("✅ llm_call 導入成功")
    
    from ufo.agents.agent.host_agent import HostAgent, AgentFactory
    print("✅ host_agent 導入成功")
    
    print("\n🎉 所有測試通過！UFO 框架可以正常使用")
    
except Exception as e:
    print(f"❌ 錯誤: {e}")
    import traceback
    traceback.print_exc()
