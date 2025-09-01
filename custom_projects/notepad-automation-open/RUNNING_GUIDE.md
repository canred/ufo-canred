# 運行指導

## 🚨 解決 "Config file not found" 警告

### 問題說明
執行時出現警告：
```
Warning: Config file not found at ufo/config/. Using only environment variables.
```

這個警告不會影響程式執行，但為了完全解決，有以下幾種方法：

### 🔧 解決方案

#### 方案 1：使用項目配置檔案（推薦）
專案已包含 `config.yaml` 檔案，程式會自動使用。

#### 方案 2：創建全域配置檔案
```bash
# 複製模板檔案
copy "..\..\ufo\config\config.yaml.template" "..\..\ufo\config\config.yaml"
```

#### 方案 3：設定環境變數
```bash
set UFO_CONFIG_PATH=%cd%\config.yaml
python task1.py
```

## 📋 完整運行步驟

### 1. 安裝依賴
```bash
cd custom_projects\notepad-automation
pip install -r requirements.txt
```

### 2. 運行程式
```bash
python task1.py
```

### 3. 預期輸出
```
=== 記事本自動化測試程式 ===
UFO 框架路徑: C:\Users\canred\Downloads\UFO
pyperclip 支援: 是
配置檔案: C:\Users\canred\Downloads\UFO\custom_projects\notepad-automation\config.yaml
--------------------------------------------------
記事本已成功打開: 無標題 - 記事本
已輸入文本：這是 UFO 自動操作 GUI 生成的測試文本！
文件已保存至：C:\Users\canred\Downloads\UFO\custom_projects\notepad-automation\test_output.txt
記事本已關閉
整個 GUI 操作流程執行完成！
```

## 🔍 疑難排解

### 問題：模組導入錯誤
**解決**：安裝缺少的套件
```bash
pip install pyautogui pyperclip pillow
```

### 問題：找不到記事本視窗
**解決**：
1. 確保沒有其他記事本視窗開啟
2. 增加等待時間
3. 檢查系統語言設定

### 問題：中文輸入異常
**解決**：
1. 確保安裝了 pyperclip：`pip install pyperclip`
2. 檢查系統剪貼簿權限
3. 嘗試切換輸入法為英文

## 📝 注意事項

1. **系統需求**：Windows 作業系統
2. **權限**：確保有檔案寫入權限
3. **安全**：程式會控制滑鼠和鍵盤，請在安全環境下測試
4. **備份**：如果目標路徑已有檔案，會被覆蓋

---
**更新時間**：2025年9月1日
