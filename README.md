# 線上測驗系統 2.0 (Online Quiz System)

一個功能完整的線上測驗系統，採用模組化設計，支援單選題和多選題，具備題目管理、成績統計等功能。

## 🆕 版本 2.0 特色

- 🏗️ **模組化架構**：採用MVC分層設計，易於維護和擴展
- 🔌 **RESTful API**：完整的API接口支援，已修正CSRF保護問題
- 🎯 **智能隨機**：進階隨機出題算法，支援多種配置
- 📊 **詳細統計**：全面的數據分析和報表
- 🔒 **數據驗證**：完善的輸入驗證和錯誤處理
- 🚀 **高效能**：優化的數據庫查詢和索引設計
- 🧹 **乾淨架構**：經過專業整理的檔案結構，完全重構並清理
- ✨ **生產就緒**：模組化設計，適合部署和長期維護
- 🧪 **完整測試**：統一的測試架構，包含系統檢查和功能驗證
- ✅ **多選題支援**：完整的多選題載入、顯示和判分功能

## 功能特色

- ✅ **多種題型支援**：單選題、多選題（已完整實現並測試）
- ✅ **智能去重**：使用SHA-256演算法自動去除重複題目
- ✅ **進階隨機抽題**：支援題型比例、難度分配、選項亂序等
- ✅ **測驗會話管理**：完整的測驗生命週期管理
- ✅ **成績統計**：詳細的答題結果與分析
- ✅ **管理後台**：題目管理、批量導入、數據統計
- ✅ **RESTful API**：支援第三方整合，API端點正常運作
- ✅ **美觀界面**：現代化響應式設計，優化顏色對比度
- ✅ **數據持久化**：SQLite資料庫儲存
- ✅ **一鍵部署**：完整的初始化腳本和配置管理
- ✅ **專業清理**：移除所有舊版檔案，架構乾淨現代
- ✅ **多格式導入**：支援3種JSON格式，智能轉換文字答案
- ✅ **容錯處理**：格式錯誤自動跳過，詳細錯誤報告
- ✅ **界面優化**：修正顏色對比度，支援深色模式，無障礙設計
- ✅ **完整測試架構**：專用test資料夾，包含系統檢查和功能測試
- ✅ **多選題完全支援**：載入、顯示、判分全流程正常運作

## 專案重構成果

本專案已完成全面重構，從原有的單一檔案架構升級為現代化的模組化設計：

### 🔄 重構前 vs 重構後

| 項目 | 重構前 | 重構後 |
|------|--------|--------|
| **架構** | 單一檔案 `app.py` | MVC分層架構 |
| **檔案數** | 5-6個檔案 | 30+個模組化檔案 |
| **資料庫** | 簡單查詢 | 專業ORM模式 |
| **API** | 無 | 完整RESTful API |
| **錯誤處理** | 基礎 | 專業驗證與處理 |
| **測試** | 手動 | 結構化測試支援 |
| **維護性** | 困難 | 易於維護和擴展 |

### 🧹 檔案清理報告

- **已移除**: 15+個舊版、備份、臨時檔案
- **新增**: 模組化架構，30+個專業組織的檔案
- **優化**: 專案體積減少，結構清晰
- **結果**: 生產就緒的乾淨架構
- **題目導入**: 完善的多格式支援和智能轉換

詳細清理報告請參閱：[CLEANUP_REPORT.md](CLEANUP_REPORT.md)

## 系統需求

- Python 3.7 或以上版本
- 支援的作業系統：Windows、macOS、Linux
- 磁碟空間：約50MB（包含虛擬環境）
- 記憶體：最少256MB

## 安裝指南

### 快速開始（推薦新用戶）

```bash
# 1. 下載專案
git clone <repository-url>
cd Test_Web

# 2. 一鍵設置環境
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux  
source .venv/bin/activate

# 3. 安裝依賴並初始化
pip install -r requirements.txt
python init_db.py

# 4. 啟動系統
python run.py
```

### 詳細安裝步驟

#### 1. 克隆或下載專案
```bash
# 下載專案到本地目錄
git clone <repository-url>
cd Test_Web
```

#### 2. 建立虛擬環境（推薦）
```bash
# 建立虛擬環境
python -m venv .venv

# 啟動虛擬環境
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

#### 3. 安裝依賴套件
```bash
# 安裝必要的依賴套件
pip install -r requirements.txt
```

#### 4. 環境設定
```bash
# 複製環境變數範例文件
cp .env.example .env

# 編輯 .env 文件設定必要參數
# FLASK_ENV=development
# SECRET_KEY=your-secret-key
# DATABASE_PATH=dev_quiz_database.db
```

#### 5. 初始化資料庫
```bash
# 自動創建資料庫表結構並導入初始數據
python init_db.py
```

## 啟動系統

### 方法一：Docker部署（推薦生產環境）

#### 快速部署
```bash
# 克隆項目
git clone <repository-url>
cd Test_Web

# Windows用戶
deploy-docker.bat

# Linux/Mac用戶
chmod +x deploy-docker.sh
./deploy-docker.sh
```

#### 手動Docker部署
```bash
# 1. 創建環境變數文件
cp .env.docker.example .env
# 編輯 .env 文件設置密鑰

# 2. 構建並啟動
docker-compose up -d

# 3. 可選：啟動Nginx反向代理
docker-compose --profile with-nginx up -d
```

#### Docker部署特點
- ✅ **生產就緒**：使用Gunicorn WSGI服務器
- ✅ **數據持久化**：資料庫和日誌自動保存
- ✅ **健康檢查**：自動監控服務狀態
- ✅ **擴展性**：支援Nginx反向代理和Redis緩存
- ✅ **安全性**：非root用戶運行，隔離環境

### 方法二：本地開發模式
```bash
python run.py
```

### 方法三：使用Flask命令（開發模式）
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

### Docker服務管理

```bash
# 查看服務狀態
docker-compose ps

# 查看日誌
docker-compose logs -f

# 停止服務
docker-compose down

# 重啟服務
docker-compose restart

# 清理數據（注意：會刪除所有數據）
docker-compose down -v
```

## 🎯 專案狀態

### ✅ 已完成功能
- 完整的題目管理系統（增刪查改）
- 智能隨機出題算法
- 單選題和多選題支援
- 測驗會話管理
- 成績統計與分析
- RESTful API接口
- 管理後台界面
- 響應式前端設計
- 資料庫自動初始化
- 模組化架構重構
- 檔案結構清理優化
- **多格式題目導入**：支援3種JSON格式
- **智能格式轉換**：文字答案自動轉索引
- **容錯導入機制**：自動跳過錯誤格式
- **界面色彩優化**：修正白底白字問題，增強對比度
- **無障礙設計**：支援深色模式，提升可訪問性

### 🚀 生產環境就緒
- **架構穩定**：MVC分層設計，代碼結構清晰
- **性能優化**：SQLite索引優化，查詢高效
- **錯誤處理**：完善的異常處理和用戶友好提示
- **安全性**：輸入驗證，SQL注入防護
- **維護性**：模組化設計，易於擴展和維護
- **部署友好**：一鍵初始化，配置簡單
- **界面優化**：修正顏色對比度問題，支援深色模式
- **無障礙設計**：符合WCAG可訪問性標準

### 📋 可選擴展（未來版本）
- 用戶認證與權限管理
- 題目分類和標籤系統
- 測驗歷史記錄
- 導出功能（PDF、Excel）
- 多語言支援
- 更多題型支援

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

系統支援多種JSON格式的題目導入，具備智能格式轉換功能。

### 格式 1：標準格式（推薦）
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
      "correct_answer": 1,
      "explanation": "Python是一種解釋型的高階程式語言。"
    }
  ]
}
```

### 格式 2：嵌套格式（相容quiz_complete02.json等）
```json
{
  "quiz": {
    "title": "機器學習與AI服務測驗",
    "questions": [
      {
        "question": "您可以在哪一層套用內容篩選？",
        "type": "single_choice",
        "options": ["metaprompt", "模型", "安全系統", "用戶體驗"],
        "correct_answer": "安全系統"
      }
    ]
  }
}
```

### 格式 3：直接陣列格式
```json
[
  {
    "question": "以下哪些是Python的特點？",
    "type": "multiple",
    "options": ["語法簡潔", "跨平台", "開源免費", "效能最快"],
    "correct_answer": [0, 1, 2]
  }
]
```

### 智能格式轉換功能

#### 答案格式自動轉換
- **文字轉索引**：`"解釋型語言" → 1`（自動查找選項位置）
- **類型標準化**：`"single_choice" → "single"`
- **多選支援**：支援文字和索引混合格式

#### 容錯處理
- 自動跳過格式錯誤的題目
- 提供詳細的錯誤報告
- 智能預設值填充
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
├── .env.docker.example        # Docker環境變數範例檔案
├── .gitignore                 # Git忽略清單
├── .dockerignore              # Docker忽略清單
├── Dockerfile                 # Docker鏡像配置
├── Dockerfile.prod            # 生產環境Docker配置
├── docker-compose.yml         # Docker Compose配置
├── deploy-docker.sh           # Linux/Mac部署腳本
├── deploy-docker.bat          # Windows部署腳本
├── run.py                     # 應用程式入口點
├── init_db.py                 # 資料庫初始化腳本
├── requirements.txt           # Python依賴清單
├── README.md                  # 主要說明文檔
├── README_TECHNICAL.md        # 技術說明文檔
├── CLEANUP_REPORT.md          # 檔案清理報告
├── IMPORT_GUIDE.md            # 題目導入指南
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
├── test/                      # 測試相關檔案 🧪
│   ├── README.md              # 測試說明文檔
│   ├── system_check.py        # 系統全面檢查
│   ├── check_multiple_choice.py # 多選題檢查
│   ├── check_db.py            # 資料庫檢查
│   ├── check_docker_env.py    # Docker環境檢查
│   ├── test_import.py         # 導入功能測試
│   ├── test_index.py          # 首頁功能測試
│   ├── test_quiz.py           # 測驗功能測試
│   ├── fix_api.py             # API修復工具
│   ├── init_db_fixed.py       # 修正版資料庫初始化
│   ├── debug_stats.py         # 除錯統計工具
│   ├── test.json              # 測試資料檔案
│   └── test02.json            # 測試資料檔案
├── nginx/                     # Nginx配置（Docker用）
│   ├── nginx.conf             # Nginx主配置
│   └── ssl/                   # SSL證書目錄
├── volumes/                   # Docker數據持久化
│   ├── database/              # 資料庫文件
│   ├── logs/                  # 日誌文件
│   ├── uploads/               # 上傳文件
│   └── README.md              # Volumes使用說明
└── dev_quiz_database.db      # SQLite資料庫檔案
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
A: 直接複製 `dev_quiz_database.db` 檔案即可備份所有題目。

### Q: 如何重置系統？
A: 刪除 `dev_quiz_database.db` 檔案，重新啟動系統即可重置。

### Q: 如何執行系統測試？
A: 使用 `test/` 資料夾中的測試腳本：
- 執行 `python test/system_check.py` 進行全面檢查
- 執行 `python test/check_multiple_choice.py` 檢查多選題
- 更多測試選項請參考 `test/README.md`

### Q: 系統出現問題時該如何排除？
A: 按以下順序排除：
1. 執行 `python test/system_check.py` 檢查整體狀態
2. 檢查 `test/` 資料夾中的相關測試腳本
3. 查看錯誤日誌和輸出信息
4. 參考 `test/README.md` 中的故障排除指南

## 技術細節

### 技術特點
- **設計模式**：MVC分層架構
- **數據庫**：SQLite（可輕鬆升級到PostgreSQL/MySQL）
- **ORM**：自訂輕量化ORM，支援SQLite優化
- **前端**：Jinja2模板 + 現代CSS + Bootstrap 5
- **API**：RESTful設計，JSON格式，CSRF保護已優化
- **界面**：響應式設計，深色模式支援，無障礙優化
- **測試架構**：專用測試資料夾，自動化檢查腳本

### 性能特點
- **題目去重**：SHA-256哈希算法，O(1)查重複
- **隨機算法**：Fisher-Yates洗牌，均勻分佈
- **數據庫優化**：索引優化，批量操作
- **內存管理**：連接池，資源自動回收
- **多選題優化**：專門的索引處理，高效判分算法

### 安全性
- **輸入驗證**：嚴格的數據格式檢查
- **SQL防護**：ORM防止SQL注入
- **CSRF保護**：選擇性CSRF保護，API端點已優化
- **錯誤處理**：友好的錯誤頁面，不洩露內部信息
- **文件安全**：限制檔案類型和大小
- **界面安全**：防XSS攻擊，CSP安全策略
- **無障礙性**：符合WCAG 2.1 AA標準，支援螢幕閱讀器

### 測試和維護
- **自動化測試**：完整的系統檢查腳本
- **多選題驗證**：專門的多選題檢查工具
- **一鍵測試**：跨平台測試執行腳本
- **詳細報告**：完整的測試報告和錯誤診斷

## 故障排除

### Docker相關問題

**Q: Docker構建失敗，提示"No matching distribution found for sqlite3"**
```bash
# SQLite3是Python內建模組，不需要安裝
# 運行修復腳本
fix-docker.bat  # Windows
# 或手動清理requirements.txt中的sqlite3行
```

**Q: Docker映像構建成功但推送失敗**
```bash
# 確保已登入Docker Hub
docker login

# 檢查映像名稱格式
docker build -t username/image-name:tag .
docker push username/image-name:tag
```

**Q: 容器啟動後無法訪問**
```bash
# 檢查端口映射
docker run -d -p 5000:5000 image-name

# 檢查容器日誌
docker logs container-name
```

### 常見問題

**Q: 介面顏色看不清楚怎麼辦？**
```bash
# 系統已修正所有顏色對比度問題
# 支援自動深色模式切換
# 如仍有問題，請檢查瀏覽器設置或回報問題
```

**Q: 啟動時出現 "Module not found" 錯誤**
```bash
# 確保虛擬環境已激活並安裝依賴
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

**Q: 資料庫初始化失敗**
```bash
# 刪除現有資料庫檔案重新初始化
del dev_quiz_database.db
python init_db.py
```

**Q: 題目沒有正確導入**
```bash
# 檢查題庫檔案格式，確保在 base/ 目錄下
# 支援的格式：.json, .txt, .csv
python init_db.py  # 重新執行初始化
```

**Q: 端口5000被占用**
```bash
# 修改 run.py 中的端口設置
# 或者終止占用端口的進程
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

## 界面設計特色

### 🎨 現代化視覺設計
- **Bootstrap 5**：最新版本的響應式框架
- **Font Awesome 6**：豐富的圖標庫
- **自適應佈局**：完美支援桌面、平板、手機
- **動畫效果**：流暢的過渡和懸停效果

### 🌙 深色模式支援
- **自動檢測**：根據系統偏好自動切換
- **完整覆蓋**：所有頁面和組件都支援深色模式
- **對比度優化**：確保在任何模式下都有良好的可讀性

### ♿ 無障礙設計
- **WCAG 2.1 AA標準**：符合國際無障礙標準
- **鍵盤導航**：完整的鍵盤操作支援
- **螢幕閱讀器**：相容主流輔助技術
- **顏色對比度**：修正所有白底白字問題

### 📱 響應式體驗
- **移動優先**：針對移動設備優化的界面
- **觸控友好**：適合觸控操作的按鈕和控件
- **快速載入**：優化的CSS和JavaScript資源

## 開發指南

### 本地開發
```bash
# 開發模式啟動（自動重載）
export FLASK_ENV=development  # Linux/Mac
set FLASK_ENV=development     # Windows
python run.py
```

### 代碼結構說明
- `app/models/`: 數據模型定義
- `app/services/`: 業務邏輯實現
- `app/routes/`: HTTP路由處理
- `app/utils/`: 輔助工具函數
- `config/`: 應用程式配置
- `templates/`: HTML模板
- `static/`: 靜態資源

### 新增功能
1. 在對應的`models/`中定義數據結構
2. 在`services/`中實現業務邏輯
3. 在`routes/`中添加API端點
4. 在`templates/`中創建前端界面

## 技術支援

如有問題或建議，請聯繫開發團隊或提交Issue。

## 授權條款

本專案採用 MIT 授權條款。

---

**版本**：2.1.1  
**最後更新**：2025年6月22日  
**重構狀態**：✅ 完成全面重構與檔案清理  
**生產就緒**：✅ 模組化架構，適合生產環境部署  
**界面優化**：✅ 修正顏色對比度，支援深色模式與無障礙設計  
**Docker支援**：✅ 完整的容器化部署方案，生產級別配置  
**健康檢查**：✅ API健康檢查修復完成，容器監控正常

### 🔄 最新更新 (v2.1.1)
- **修復**：API健康檢查端點 (`/api/health`) 
- **改進**：Docker容器健康狀態監控
- **新增**：完整的故障排除文檔
- **優化**：系統穩定性和可靠性
