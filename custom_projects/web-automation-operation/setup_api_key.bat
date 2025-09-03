@echo off
echo =======================================================
echo            設定 OpenAI API 金鑰環境變數
echo =======================================================
echo.
echo 請將您的 OpenAI API 金鑰貼上到下面：
echo (格式應該是 sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx)
echo.
set /p API_KEY="請輸入您的 OpenAI API 金鑰: "

if "%API_KEY%"=="" (
    echo.
    echo ❌ 錯誤：未輸入 API 金鑰
    pause
    exit /b 1
)

if not "%API_KEY:~0,3%"=="sk-" (
    echo.
    echo ❌ 警告：API 金鑰格式可能不正確，應該以 'sk-' 開頭
    echo 繼續設定...
)

echo.
echo 正在設定環境變數 OPENAI_API_KEY...

rem 設定當前會話的環境變數
set OPENAI_API_KEY=%API_KEY%

rem 設定系統環境變數（需要管理員權限）
setx OPENAI_API_KEY "%API_KEY%" >nul 2>&1

if %errorlevel%==0 (
    echo ✅ 環境變數設定成功！
    echo.
    echo 📋 設定資訊：
    echo    變數名稱: OPENAI_API_KEY
    echo    變數值: %API_KEY:~0,7%... (已隱藏完整金鑰)
    echo.
    echo 💡 提示：
    echo    - 當前終端機會話立即生效
    echo    - 新的終端機會話也會自動載入此設定
    echo    - 重新啟動 VS Code 以確保設定生效
) else (
    echo ⚠️  系統環境變數設定失敗（可能需要管理員權限）
    echo 但當前會話的環境變數已設定，您可以繼續使用
)

echo.
echo 🔍 驗證環境變數設定：
echo OPENAI_API_KEY = %OPENAI_API_KEY:~0,7%...

echo.
echo 現在您可以執行 Python 腳本了！
echo 執行命令: python task.py
echo.
pause
