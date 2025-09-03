# UFO2 截圖和 OCR 功能設定指南

## 功能介紹

此程式現在使用 **UFO2 框架的 LLM** 進行螢幕截圖和 OCR 辨識功能，可以：

1. 📸 自動截取當前螢幕畫面
2. 💾 將截圖保存到 `logs/screenshots/` 目錄
3. 🔍 使用 **UFO2 的 LLM** 進行智慧型視覺分析和 OCR 文字辨識
4. � 備用方案：如果 UFO2 LLM 不可用，自動切換到 OpenAI API
5. �📄 將 OCR 結果保存為文字檔案

## UFO2 OCR 優勢

### 與傳統 OCR 的差異

- **智慧分析**：不只是文字提取，還能理解 UI 元素和操作建議
- **上下文理解**：專門針對 Gmail 自動化場景進行優化
- **結構化輸出**：提供結構化的分析結果，便於後續處理
- **整合性**：完全整合在 UFO2 框架中，使用統一的配置和成本追蹤

### UFO2 OCR 分析內容

1. **文字內容提取**：所有可見文字
2. **Gmail 專項分析**：郵件主題、寄件者、狀態等
3. **UI 元素識別**：按鈕、連結、輸入框
4. **自動化建議**：可點擊元素和操作狀態

## 必要設定

### 1. UFO2 框架配置

確保您的 `config.yaml` 檔案正確設定了 LLM：

```yaml
# UFO2 LLM 配置
LLM:
  API_TYPE: "openai"  # 或其他支援的 LLM 類型
  API_KEY: "your_api_key_here"
  MODEL: "gpt-4-vision-preview"  # 支援視覺的模型

# 或者使用頂層配置
OPENAI_API_KEY: "your_api_key_here"
API_KEY: "your_api_key_here"
```

### 2. 環境變數設定（備用方案）

如果 UFO2 配置中沒有設定 API 金鑰，程式會使用環境變數：

Windows 命令提示字元：
```cmd
set OPENAI_API_KEY=your_api_key_here
```

PowerShell：
```powershell
$env:OPENAI_API_KEY="your_api_key_here"
```

### 3. 安裝依賴套件

```bash
pip install -r requirements.txt
```

## 使用方式

### 自動執行（推薦）

程式會在郵件選取步驟後自動執行 UFO2 OCR：

1. 截取螢幕畫面
2. 使用 UFO2 LLM 進行智慧分析
3. 如果 UFO2 失敗，自動切換到備用 OpenAI API
4. 保存結果到檔案

### 手動呼叫

```python
# 只截圖不進行 OCR
result = chrome_agent.capture_screenshot_and_ocr(ocr_analysis=False)

# 截圖並進行 UFO2 OCR
result = chrome_agent.capture_screenshot_and_ocr(ocr_analysis=True)

# 指定截圖保存路徑
result = chrome_agent.capture_screenshot_and_ocr(
    save_path="custom_path.png",
    ocr_analysis=True
)
```

## 輸出檔案

### 截圖檔案
- 位置：`logs/screenshots/screenshot_YYYYMMDD_HHMMSS.png`
- 格式：PNG 圖片檔案
- 內容：完整螢幕截圖

### UFO2 OCR 結果檔案
- 位置：`logs/screenshots/screenshot_YYYYMMDD_HHMMSS_ufo2_ocr.txt`
- 格式：UTF-8 文字檔案
- 內容：包含時間戳記、使用方法和完整的 UFO2 分析結果

範例輸出格式：
```
=== UFO2 螢幕截圖 OCR 辨識結果 ===
截圖時間: 2024-12-29 10:30:45
截圖檔案: /path/to/screenshot_20241229_103045.png
OCR 方法: UFO2_LLM
分析成本: $0.0234
------------------------------------------------------------
[UFO2 分析結果]
1. 文字內容提取：
   - Gmail 收件匣標題
   - 郵件主題列表
   ...

2. Gmail 相關內容：
   - 寄件者：xxx@example.com
   - 郵件狀態：已選取 3 封
   ...

3. UI 元素分析：
   - 搜尋框：包含 "多結果子"
   - 選取按鈕：已啟用
   ...

4. 自動化操作建議：
   - 可執行刪除操作
   - 可執行標記操作
   ...
------------------------------------------------------------
```

## 雙重保險機制

### 主要方法：UFO2 LLM
- 使用 UFO2 框架的 `get_completion` 函數
- 與 UFO2 配置完全整合
- 統一的成本追蹤和錯誤處理

### 備用方法：OpenAI API
- 當 UFO2 LLM 不可用時自動啟用
- 直接使用 OpenAI Vision API
- 確保功能的可靠性

## 故障排除

### 常見問題

1. **"UFO2 LLM 調用失敗"**
   - 檢查 UFO2 的 `config.yaml` 設定
   - 確認 LLM 配置正確
   - 系統會自動切換到備用方法

2. **"API 金鑰未設定"**
   - 在 UFO2 配置檔案中設定 API 金鑰
   - 或設定 OPENAI_API_KEY 環境變數

3. **"UFO2 框架初始化失敗"**
   - 檢查 UFO2 框架安裝
   - 確認配置檔案路徑正確

### 除錯資訊

程式會顯示詳細的狀態訊息：
- 🤖 UFO2 LLM 調用狀態
- � 備用方法切換提示
- � 成本追蹤（UFO2 統一計費）
- 📡 網路請求狀態

## 成本估算

### UFO2 LLM 成本
- 由 UFO2 框架統一管理和追蹤
- 在程式摘要中顯示總成本
- 支援多種 LLM 提供商的成本計算

### 備用 API 成本
- GPT-4 Vision：約 $0.01-0.05 美元/次
- 根據圖片複雜度和回應長度而異

## 進階功能

### 自訂分析提示
您可以修改 `_perform_ufo2_ocr` 方法中的提示內容，以：
- 關注特定的 UI 元素
- 調整分析重點
- 客製化輸出格式

### 整合 UFO2 工作流程
UFO2 OCR 結果可以直接用於：
- UFO2 的決策制定
- 自動化操作規劃
- 錯誤檢測和恢復

## 最佳實踐

1. **優先使用 UFO2 配置**：將 API 金鑰設定在 UFO2 配置檔案中
2. **監控成本**：使用 UFO2 的成本追蹤功能
3. **檢查結果**：查看生成的文字檔案確認分析品質
4. **定期更新**：保持 UFO2 框架和相關套件的最新版本
