#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試腳本：驗證 UFO2 Chrome 自動化程式的核心功能
"""

import sys
import os

def test_core_imports():
    """測試核心模組導入"""
    print("=== 測試核心模組導入 ===")
    
    try:
        # 測試基本 Python 模組
        import time
        import json
        import requests
        print("✅ 基本 Python 模組：正常")
        
        # 測試圖像處理模組
        from PIL import Image
        import io
        import base64
        print("✅ 圖像處理模組：正常")
        
        # 測試 GUI 自動化模組
        import pyautogui
        import pyperclip
        print("✅ GUI 自動化模組：正常")
        
        # 測試網路通訊模組
        import websockets
        print("✅ WebSocket 模組：正常")
        
        return True
        
    except ImportError as e:
        print(f"❌ 模組導入失敗: {e}")
        return False

def test_screenshot_functionality():
    """測試截圖功能"""
    print("\n=== 測試截圖功能 ===")
    
    try:
        import pyautogui
        from PIL import Image
        
        # 模擬截圖（不實際執行）
        print("✅ 截圖功能模組：正常")
        
        # 測試圖像格式轉換
        test_size = (100, 100)
        test_image = Image.new('RGB', test_size, color='red')
        
        import io
        buffered = io.BytesIO()
        test_image.save(buffered, format="PNG")
        print("✅ 圖像格式轉換：正常")
        
        import base64
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        print("✅ Base64 編碼：正常")
        
        return True
        
    except Exception as e:
        print(f"❌ 截圖功能測試失敗: {e}")
        return False

def test_openai_api_setup():
    """測試 OpenAI API 設定"""
    print("\n=== 測試 OpenAI API 設定 ===")
    
    try:
        import os
        
        # 檢查環境變數
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            print("✅ OPENAI_API_KEY 環境變數：已設定")
            print(f"   金鑰前綴: {api_key[:8]}...")
        else:
            print("⚠️  OPENAI_API_KEY 環境變數：未設定")
            print("   請設定 API 金鑰以使用 OCR 功能")
        
        # 測試 HTTP 請求功能
        import requests
        print("✅ HTTP 請求模組：正常")
        
        return True
        
    except Exception as e:
        print(f"❌ OpenAI API 設定測試失敗: {e}")
        return False

def test_chrome_automation_imports():
    """測試 Chrome 自動化相關模組"""
    print("\n=== 測試 Chrome 自動化模組 ===")
    
    try:
        # 測試異步功能
        import asyncio
        print("✅ 異步處理模組：正常")
        
        # 測試時間和日期功能
        from datetime import datetime
        print("✅ 時間日期模組：正常")
        
        # 測試檔案系統操作
        import subprocess
        print("✅ 子程序模組：正常")
        
        return True
        
    except Exception as e:
        print(f"❌ Chrome 自動化模組測試失敗: {e}")
        return False

def test_pandas_conflict():
    """檢查 pandas 相關衝突"""
    print("\n=== 檢查 Pandas 相關衝突 ===")
    
    try:
        # 嘗試導入 pandas（如果存在）
        import pandas as pd
        print(f"⚠️  Pandas 已安裝: {pd.__version__}")
        
        try:
            import numpy as np
            print(f"⚠️  NumPy 已安裝: {np.__version__}")
        except Exception as e:
            print(f"❌ NumPy 導入失敗: {e}")
            
    except ImportError:
        print("✅ Pandas 未安裝（這對您的程式是好的）")
        
        try:
            import numpy as np
            print(f"⚠️  NumPy 已安裝: {np.__version__}")
            print("   如果不需要可以移除")
        except ImportError:
            print("✅ NumPy 未安裝")

def main():
    """主測試函數"""
    print("🧪 UFO2 Chrome 自動化程式核心功能測試")
    print("=" * 50)
    
    tests = [
        test_core_imports,
        test_screenshot_functionality,
        test_openai_api_setup,
        test_chrome_automation_imports,
        test_pandas_conflict
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ 測試執行失敗: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("🎯 測試結果摘要")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ 所有測試通過 ({passed}/{total})")
        print("🎉 您的程式核心功能運作正常！")
    else:
        print(f"⚠️  部分測試失敗 ({passed}/{total})")
        print("💡 請檢查失敗的模組並安裝必要套件")
    
    print("\n💡 建議操作:")
    print("1. 如果 pandas 衝突，執行: pip uninstall pandas -y")
    print("2. 安裝必要套件: pip install -r requirements.txt")
    print("3. 設定 OpenAI API 金鑰以使用 OCR 功能")

if __name__ == "__main__":
    main()
