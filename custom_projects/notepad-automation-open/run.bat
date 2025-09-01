@echo off
echo ===============================================
echo       UFO 記事本自動化測試程式
echo ===============================================
echo.

:: 檢查是否在正確的目錄
if not exist "task1.py" (
    echo ❌ 錯誤：請在 notepad-automation 目錄下執行此腳本
    echo 正確路徑：custom_projects\notepad-automation\
    pause
    exit /b 1
)

:: 檢查 Python 是否安裝
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ 錯誤：未找到 Python，請先安裝 Python
    pause
    exit /b 1
)

echo ✅ Python 已安裝
echo.

:: 檢查必要套件
echo 🔍 檢查依賴套件...
python -c "import pyautogui; print('✅ pyautogui 已安裝')" 2>nul || (
    echo ❌ pyautogui 未安裝，正在安裝...
    pip install pyautogui
)

python -c "import pyperclip; print('✅ pyperclip 已安裝')" 2>nul || (
    echo ❌ pyperclip 未安裝，正在安裝...
    pip install pyperclip
)

echo.
echo 🚀 啟動記事本自動化程式...
echo.
echo 注意：程式將自動控制滑鼠和鍵盤
echo      請確保記事本沒有其他重要文件開啟
echo.
pause

:: 執行主程式
python task1.py

echo.
echo ===============================================
echo 程式執行完成，按任意鍵關閉視窗...
pause
