# 記事本自動化專案

## 📋 描述
使用 UFO 框架實現記事本的自動化操作，包括開啟、輸入文字、保存和關閉功能。

## 🏗️ 專案結構
```
custom_projects/notepad-automation/
├── task1.py              # 主程式
├── requirements.txt      # 專案依賴
├── README.md            # 專案說明
└── test_output.txt      # 輸出檔案（執行後產生）
```

## 🚀 安裝與執行

### 1. 安裝依賴套件
```bash
pip install -r requirements.txt
```

### 2. 執行程式
```bash
cd custom_projects/notepad-automation
python task1.py
```

## ⚙️ 功能特點

### 🔧 核心功能
- ✅ 自動開啟記事本應用程式
- ✅ 智慧視窗偵測（支援中英文版本）
- ✅ 中文文字輸入（支援 pyperclip 剪貼簿方式）
- ✅ 檔案自動保存
- ✅ 應用程式自動關閉

### 🌐 中文支援
- **方法 1**：使用 pyperclip 剪貼簿輸入（推薦）
- **方法 2**：直接鍵盤輸入（備用）
- **方法 3**：逐字符處理（緊急備用）

### 🛡️ 錯誤處理
- 視窗偵測失敗處理
- 中文輸入失敗備用方案
- 檔案覆蓋確認處理

## 📝 注意事項

### 系統需求
- Windows 作業系統
- Python 3.7+
- UFO 框架（相對路徑：`../../`）

### 使用建議
1. 執行前請關閉其他記事本視窗
2. 確保有足夠的磁碟空間保存檔案
3. 建議安裝 pyperclip 以獲得最佳中文支援

### 疑難排解
- **中文無法輸入**：執行 `pip install pyperclip`
- **找不到記事本**：檢查是否有其他記事本視窗開啟
- **保存失敗**：檢查目標路徑權限

## 🔗 相關連結
- [UFO 框架文檔](../../README.md)
- [Python pyautogui 文檔](https://pyautogui.readthedocs.io/)
- [pyperclip 文檔](https://pyperclip.readthedocs.io/)

---
**作者**：UFO GUI 自動化測試  
**更新日期**：2025年8月31日
