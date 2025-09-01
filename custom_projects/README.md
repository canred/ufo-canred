# UFO 自定義專案

這個目錄包含基於 UFO 框架開發的自定義自動化專案。

## 📁 專案結構

```
custom_projects/
├── notepad-automation/          # 記事本自動化專案
│   ├── task1.py                # 主程式
│   ├── requirements.txt        # 依賴清單
│   ├── README.md              # 專案文檔
│   └── test_output.txt        # 輸出檔案
├── shared/                     # 共用工具和資源
│   └── utils.py               # 通用工具函數
└── README.md                  # 本檔案
```

## 🚀 快速開始

### 1. 安裝依賴
```bash
cd custom_projects/notepad-automation
pip install -r requirements.txt
```

### 2. 執行測試
```bash
python task1.py
```

## 📋 專案清單

### 🗒️ notepad-automation
- **功能**：記事本自動化操作
- **狀態**：✅ 完成
- **特色**：中文支援、錯誤處理、多種輸入方案

### 🔧 shared
- **功能**：共用工具和函數
- **包含**：路徑設定、依賴檢查、UI輔助工具

## 💡 開發指南

### 新增專案步驟
1. 在 `custom_projects/` 下創建新目錄
2. 複製 `shared/utils.py` 中的輔助函數
3. 建立 `requirements.txt` 列出依賴
4. 撰寫 `README.md` 說明專案
5. 使用相對路徑 `../../` 引用 UFO 框架

### 最佳實踐
- 使用 `shared/utils.py` 中的共用函數
- 保持專案獨立性，避免修改 UFO 核心檔案
- 為每個專案建立獨立的依賴清單
- 提供詳細的文檔和註解

## 🔗 相關資源
- [UFO 框架主目錄](../../)
- [UFO 官方文檔](../../documents/)
- [範例專案](../../dataflow/)

---
**維護者**：UFO 自動化專案組  
**最後更新**：2025年8月31日
