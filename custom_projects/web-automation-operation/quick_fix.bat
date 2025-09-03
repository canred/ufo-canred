@echo off
title 修復 Pandas/Numpy 衝突問題

echo ===============================================
echo 🔧 快速修復 Pandas/Numpy 衝突問題
echo ===============================================
echo.

echo 📋 當前目錄: %CD%
echo.

echo 🗑️  步驟 1: 移除可能衝突的 pandas...
pip uninstall pandas -y
echo.

echo 🧹 步驟 2: 清理 pip 快取...
pip cache purge
echo.

echo 📦 步驟 3: 安裝必要套件...
pip install -r requirements.txt
echo.

echo 🧪 步驟 4: 測試核心功能...
python -c "print('Testing core imports...'); import pyautogui, requests, pillow; print('✅ Core modules work')"
echo.

echo ✅ 修復完成！現在可以執行您的程式了：
echo python task.py
echo.

pause
