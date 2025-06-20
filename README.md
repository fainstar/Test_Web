# 線上測驗系統 2.0 (Online Quiz System)

一個功能完整的線上測驗系統，採用模組化設計，支援單選題和多選題，具備題目管理、成績統計等功能。

## 🆕 版本 2.0 特色

- 🏗️ **模組化架構**：採用MVC分層設計，易於維護和擴展
- 🔌 **RESTful API**：完整的API接口支援
- 🎯 **智能隨機**：進階隨機出題算法，支援多種配置
- 📊 **詳細統計**：全面的數據分析和報表
- 🔒 **數據驗證**：完善的輸入驗證和錯誤處理
- 🚀 **高效能**：優化的數據庫查詢和索引設計
- 🧹 **乾淨架構**：經過專業整理的檔案結構，適合生產環境

## 功能特色

- ✅ **多種題型支援**：單選題、多選題
- ✅ **智能去重**：使用SHA-256演算法自動去除重複題目
- ✅ **進階隨機抽題**：支援題型比例、難度分配、選項亂序等
- ✅ **測驗會話管理**：完整的測驗生命週期管理
- ✅ **成績統計**：詳細的答題結果與分析
- ✅ **管理後台**：題目管理、批量導入、數據統計
- ✅ **RESTful API**：支援第三方整合
- ✅ **美觀界面**：現代化響應式設計
- ✅ **數據持久化**：SQLite資料庫儲存

## 系統需求

- Python 3.7 或以上版本
- 支援的作業系統：Windows、macOS、Linux

## 安裝指南

### 1. 克隆或下載專案
```bash
# 下載專案到本地目錄
git clone <repository-url>
cd Test_Web
```

### 2. 建立虛擬環境（推薦）
```bash
# 建立虛擬環境
python -m venv .venv

# 啟動虛擬環境
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3. 安裝依賴套件
```bash
# 安裝必要的依賴套件
pip install -r requirements.txt
```

### 4. 環境設定
```bash
# 複製環境變數範例文件
cp .env.example .env

# 編輯 .env 文件設定必要參數
# FLASK_ENV=development
# SECRET_KEY=your-secret-key
# DATABASE_PATH=quiz_database.db
```

### 5. 初始化資料庫
```bash
# 自動創建資料庫表結構並導入初始數據
python init_db.py
```

## 啟動系統

### 方法一：使用新的啟動腳本（推薦）
```bash
python run.py
```

### 方法二：使用Flask命令（開發模式）
```bash
# 設定環境變數
export FLASK_APP=run.py
export FLASK_ENV=development

# 啟動應用程式
flask run
```

啟動成功後，在瀏覽器中開啟：
- **主要入口**：http://localhost:5000
- **管理後台**：http://localhost:5000/admin
- **API文檔**：http://localhost:5000/api

## 使用說明

### 一般用戶功能

#### 開始測驗
1. 開啟首頁 (http://localhost:5000)
2. 選擇測驗題數（5-20題）
3. 點擊「開始測驗」

#### 答題流程
1. 仔細閱讀題目
2. **單選題**：選擇一個答案
3. **多選題**：可選擇多個答案（題目會標示「多選題」）
4. 點擊「下一題」繼續
5. 完成所有題目後查看成績

#### 查看結果
- 總分與答對率
- 逐題解析與正確答案
- 答題統計資訊

## API使用指南

系統提供完整的RESTful API接口，支援第三方整合。

### 基礎URL
```
http://localhost:5000/api
```

### 主要API端點

#### 題目管理
- `GET /api/questions` - 獲取題目列表
- `GET /api/questions/{id}` - 獲取單個題目
- `POST /api/questions` - 添加新題目
- `DELETE /api/questions/{id}` - 刪除題目
- `GET /api/questions/random` - 獲取隨機題目

#### 測驗管理
- `POST /api/quiz/create` - 創建測驗
- `POST /api/quiz/{session_id}/submit` - 提交答案
- `POST /api/quiz/{session_id}/complete` - 完成測驗

#### 統計信息
- `GET /api/statistics` - 獲取系統統計信息

### API使用範例

#### 創建測驗
```bash
curl -X POST http://localhost:5000/api/quiz/create \
  -H "Content-Type: application/json" \
  -d '{
    "count": 10,
    "category": "Python基礎",
    "difficulty": "中等"
  }'
```

#### 獲取隨機題目
```bash
curl "http://localhost:5000/api/questions/random?count=5&category=機器學習"
```

## 進階功能

### 智能隨機出題
系統支援多種進階隨機出題配置：

1. **題型比例控制**：指定單選題和多選題的比例
2. **難度分佈**：按難度等級分配題目
3. **分類篩選**：從特定分類中抽取題目
4. **選項亂序**：隨機打亂選項順序
5. **去重機制**：自動避免重複題目

### 測驗會話管理
- 會話狀態追蹤
- 答題進度保存
- 自動超時處理
- 詳細結果分析

### 數據驗證
- 輸入格式驗證
- 業務邏輯檢查
- 錯誤信息提示
- 安全性保護

## 題目格式

### JSON格式範例
```json
{
  "questions": [
    {
      "question": "Python是什麼類型的程式語言？",
      "type": "single",
      "options": [
        "編譯型語言",
        "解釋型語言",
        "組合語言",
        "機器語言"
      ],
      "correct_answer": [1],
      "explanation": "Python是一種解釋型的高階程式語言。"
    },
    {
      "question": "以下哪些是Python的特點？",
      "type": "multiple",
      "options": [
        "語法簡潔",
        "跨平台",
        "開源免費",
        "效能最快"
      ],
      "correct_answer": [0, 1, 2],
      "explanation": "Python具有語法簡潔、跨平台、開源免費等特點，但執行效能不是最快的。"
    }
  ]
}
```

### 格式說明
- `question`：題目內容
- `type`：題目類型（"single" = 單選，"multiple" = 多選）
- `options`：選項陣列
- `correct_answer`：正確答案索引陣列（從0開始）
- `explanation`：題目解析（選填）

## 目錄結構（模組化設計）

```
Test_Web/
├── .env.example               # 環境變數範例檔案
├── .gitignore                 # Git忽略清單
├── run.py                     # 應用程式入口點
├── init_db.py                 # 資料庫初始化腳本
├── requirements.txt           # Python依賴清單
├── README.md                  # 主要說明文檔
├── README_TECHNICAL.md        # 技術說明文檔
├── CLEANUP_REPORT.md          # 檔案清理報告
├── config/                    # 配置模組
│   └── config.py              # 應用程式配置
├── app/                       # 主應用程式模組
│   ├── __init__.py            # 應用程式工廠
│   ├── models/                # 數據模型層
│   │   ├── __init__.py
│   │   ├── base.py            # 基礎模型類
│   │   ├── question.py        # 題目模型
│   │   └── quiz_session.py    # 測驗會話模型
│   ├── services/              # 業務邏輯層
│   │   ├── __init__.py
│   │   ├── question_service.py # 題目服務
│   │   └── quiz_service.py     # 測驗服務
│   ├── routes/                # 路由控制層
│   │   ├── __init__.py
│   │   ├── main.py            # 主要路由
│   │   ├── quiz.py            # 測驗路由
│   │   ├── admin.py           # 管理路由
│   │   └── api.py             # API路由
│   └── utils/                 # 工具模組
│       ├── __init__.py
│       ├── validators.py      # 數據驗證
│       ├── error_handlers.py  # 錯誤處理
│       └── context_processors.py # 上下文處理
├── templates/                 # HTML模板
│   ├── base.html              # 基礎模板
│   ├── index.html             # 首頁模板
│   ├── quiz.html              # 測驗頁面模板
│   ├── results.html           # 結果頁面模板
│   ├── admin/                 # 管理相關模板
│   │   └── index.html         # 管理面板首頁
│   └── errors/                # 錯誤頁面模板
│       ├── 404.html           # 404錯誤頁面
│       └── 500.html           # 500錯誤頁面
├── static/                    # 靜態資源
│   └── style.css              # 主要樣式檔案
├── base/                      # 初始題庫檔案
│   ├── quiz_complete.json
│   └── quiz_complete02.json
└── quiz_database.db          # SQLite資料庫檔案
```

## 常見問題

### Q: 如何新增新的題目？
A: 有兩種方式：
1. 透過管理後台手動新增
2. 準備JSON格式檔案，使用批量導入功能

### Q: 系統會重複匯入相同題目嗎？
A: 不會。系統使用hash演算法自動檢測並跳過重複題目。

### Q: 可以修改題目數量嗎？
A: 可以。在首頁選擇5-20題之間的任意數量。

### Q: 如何備份題目資料？
A: 直接複製 `quiz_database.db` 檔案即可備份所有題目。

### Q: 如何重置系統？
A: 刪除 `quiz_database.db` 檔案，重新啟動系統即可重置。

## 技術支援

如有問題或建議，請聯繫開發團隊或提交Issue。

## 授權條款

本專案採用 MIT 授權條款。

---

**版本**：1.0.0  
**最後更新**：2024年
