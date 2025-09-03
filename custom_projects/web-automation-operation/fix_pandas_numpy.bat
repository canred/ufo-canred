@echo off
echo ===============================================
echo 修復 Pandas/Numpy 版本相容性問題
echo ===============================================
echo.

echo 步驟 1: 解除安裝可能衝突的套件...
pip uninstall pandas numpy -y

echo.
echo 步驟 2: 清理 pip 快取...
pip cache purge

echo.
echo 步驟 3: 重新安裝相容的版本...
pip install numpy==1.24.4
pip install pandas==2.1.4

echo.
echo 步驟 4: 安裝其他必要套件...
pip install pyautogui>=0.9.54
pip install pyperclip>=1.8.2
pip install pillow>=10.0.0
pip install requests>=2.31.0
pip install opencv-python>=4.8.0
pip install selenium>=4.15.0
pip install websockets>=11.0.3
pip install openai>=1.3.0

echo.
echo 步驟 5: 驗證安裝...
python -c "import numpy; print(f'NumPy version: {numpy.__version__}')"
python -c "import pandas; print(f'Pandas version: {pandas.__version__}')"

echo.
echo ===============================================
echo 修復完成！
echo ===============================================
pause
