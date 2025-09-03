# OpenAI API 金鑰設定指南

## 問題描述
當您看到錯誤訊息：
```
❌ UFO2 OCR 辨識失敗: API 金鑰未設定。請在 UFO2 配置檔案中設定或設定 OPENAI_API_KEY 環境變數。
```

這表示程式需要 OpenAI API 金鑰來執行 OCR 功能。

## 解決方案 (任選一種)

### 方案1: 使用環境變數設定 (推薦)

#### 方法A: 使用我們提供的腳本
1. 雙擊執行 `setup_api_key.bat`
2. 按照提示輸入您的 API 金鑰
3. 重新執行 `python task.py`

#### 方法B: 手動設定環境變數
1. 按 `Win + R`，輸入 `cmd` 並按 Enter
2. 執行以下命令（將 YOUR_API_KEY 替換為真實金鑰）：
   ```cmd
   setx OPENAI_API_KEY "sk-YOUR_API_KEY_HERE"
   ```
3. 重新啟動 VS Code
4. 執行 `python task.py`

### 方案2: 使用 .env 檔案
1. 複製 `.env.example` 為 `.env`：
   ```cmd
   copy .env.example .env
   ```
2. 編輯 `.env` 檔案，將 `您的API金鑰` 替換為真實金鑰
3. 執行 `python task.py`

### 方案3: 修改 UFO2 配置檔案
1. 編輯 `config.yaml` 檔案
2. 找到以下行：
   ```yaml
   API_KEY: "sk-YOUR_API_KEY_HERE"
   ```
3. 將 `sk-YOUR_API_KEY_HERE` 替換為您的真實 API 金鑰
4. 在所有三個 Agent 配置中都要修改（HOST_AGENT, APP_AGENT, EVALUATION_AGENT）

## 如何獲取 OpenAI API 金鑰

1. 前往 [OpenAI API Keys 頁面](https://platform.openai.com/api-keys)
2. 登入您的 OpenAI 帳戶
3. 點擊 "Create new secret key"
4. 設定金鑰名稱（可選）
5. 複製生成的 API 金鑰（格式：sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx）

## 注意事項

- ⚠️ **安全性**: API 金鑰具有費用，請勿分享給他人
- ⚠️ **版本控制**: 不要將 API 金鑰提交到 Git
- 💰 **費用**: 使用 GPT-4 Vision API 會產生費用，請注意使用量
- 🔄 **重新啟動**: 設定環境變數後可能需要重新啟動 VS Code

## 驗證設定

執行以下命令驗證 API 金鑰是否正確設定：

```cmd
echo %OPENAI_API_KEY%
```

如果顯示您的 API 金鑰（以 sk- 開頭），則設定成功。

## 故障排除

如果仍然遇到問題，請檢查：

1. API 金鑰格式是否正確（以 sk- 開頭，長度約 51 字符）
2. 是否有充足的 API 餘額
3. 是否重新啟動了 VS Code
4. 網路連接是否正常

## 測試 OCR 功能

設定完成後，執行程式應該會看到類似輸出：
```
🔑 使用 API 金鑰: sk-1234...
📡 發送請求到 UFO2 LLM...
✅ UFO2 OCR 分析完成
💰 UFO2 LLM 成本: $0.0123
```
