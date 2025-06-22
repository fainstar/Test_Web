# 線上測驗系統 - 技術文件 v2.0

本文件提供系統架構、數據流、關鍵技術點與維護重點的完整技術參考。

## 🏗️ 系統架構概覽

### 技術棧
- **後端**：Python 3.10+ + Flask 3.0.0
- **資料庫**：SQLite 3 (單檔案資料庫，支援高並發)
- **前端**：HTML5 + CSS3 + JavaScript (現代化響應式設計)
- **哈希演算法**：SHA-256 (題目去重)
- **架構模式**：MVC分層架構
- **API設計**：RESTful，支援JSON格式

### 🔧 核心模組架構
```
app/
├── __init__.py              # 應用工廠，CSRF保護配置
├── models/                  # 數據模型層
│   ├── question.py         # 題目模型，支援多選題
│   └── quiz_session.py     # 測驗會話模型
├── services/               # 業務邏輯層
│   ├── question_service.py # 題目服務，智能轉換
│   └── quiz_service.py     # 測驗服務，判分邏輯
├── routes/                 # 路由控制層
│   ├── main.py            # 主要路由
│   ├── quiz.py            # 測驗路由
│   ├── admin.py           # 管理路由
│   └── api.py             # API路由，CSRF已優化
└── utils/                 # 工具模組
    ├── validators.py      # 數據驗證
    ├── error_handlers.py  # 錯誤處理
    └── context_processors.py # 上下文處理
```

## 📊 數據流與架構

### 1. 多選題導入流程 (已優化)
```
JSON檔案 → 格式標準化 → 文字答案轉索引 → hash計算 → 重複檢查 → 資料庫插入
```

**關鍵實作**：
- `question_service.py::normalize_question_format()` - 多格式JSON支援
- `init_db.py::normalize_question_format()` - 文字答案自動轉索引
- `question.py::add()` - SHA-256雜湊計算與去重
- `question.py::_format_question()` - 多選題正確答案處理

### 2. 測驗執行流程 (多選題完整支援)
```
隨機抽題 → Session儲存 → 逐題顯示 → 答案收集 → 多選題判分 → 結果展示
```

**關鍵實作**：
- `quiz_service.py::create_quiz_session()` - 隨機抽題算法
- `quiz_service.py::submit_answer()` - 多選題判分邏輯
- `quiz_service.py::calculate_score()` - 成績計算與統計
- `quiz.py::/quiz/<int:question_id>` - 動態題目顯示

### 3. API流程 (CSRF已修正)
```
API請求 → CSRF檢查(已排除) → 業務邏輯 → JSON響應
```

**關鍵實作**：
- `__init__.py::init_extensions()` - API藍圖CSRF排除
- `api.py` - RESTful API端點
- `quiz_service.py` - 統一的業務邏輯服務

## 🗄️ 資料庫結構 (已更新)

### 主表：questions
```sql
CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_hash TEXT UNIQUE NOT NULL,     -- SHA-256 hash用於去重
    question_text TEXT NOT NULL,            -- 題目內容
    question_type TEXT NOT NULL,            -- 題型：single_choice/multiple_choice
    options TEXT NOT NULL,                  -- JSON格式選項陣列
    correct_answer TEXT NOT NULL,           -- 單選：索引字串，多選：逗號分隔索引
    correct_answers TEXT,                   -- JSON格式正確答案索引陣列
    category TEXT DEFAULT '一般',           -- 題目分類
    difficulty TEXT DEFAULT '中等',         -- 難度級別
    explanation TEXT,                       -- 題目解析
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 會話表：quiz_sessions
```sql
CREATE TABLE quiz_sessions (
    id TEXT PRIMARY KEY,                    -- UUID會話ID
    quiz_config TEXT NOT NULL,             -- JSON格式測驗配置
    questions TEXT NOT NULL,               -- JSON格式題目列表
    user_answers TEXT,                     -- JSON格式用戶答案
    score INTEGER,                         -- 總分
    total_questions INTEGER NOT NULL,      -- 總題數
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);
```

### 索引設計
- `question_hash` 欄位：UNIQUE約束，確保題目唯一性，支援O(1)去重
- `question_type` 欄位：B-tree索引，加速題型分類查詢
- `category` 欄位：B-tree索引，支援分類過濾
- `created_at` 欄位：時間排序索引，支援時間範圍查詢

## 🔐 Hash去重機制 (已優化)

### 演算法實作
```python
def calculate_question_hash(question_data):
    # 標準化輸入數據，確保一致性
    normalized_data = {
        'question': question_data['question_text'].strip(),
        'type': question_data['question_type'],
        'options': sorted([opt.strip() for opt in question_data['options']]),
CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hash TEXT UNIQUE NOT NULL,           -- SHA-256雜湊值，去重用
    question TEXT NOT NULL,              -- 題目內容
    type TEXT NOT NULL,                  -- 'single' 或 'multiple'
    options TEXT NOT NULL,               -- JSON格式選項陣列
    correct_answer TEXT NOT NULL,        -- JSON格式正確答案索引
    explanation TEXT,                    -- 題目解析
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 索引設計
- `hash` 欄位：UNIQUE約束，確保題目唯一性
- `type` 欄位：可建立索引加速分類查詢
- `created_at` 欄位：時間排序索引

## Hash去重機制

### 演算法實作
```python
def calculate_question_hash(question_data):
    # 標準化輸入數據
    normalized_data = {
        'question': question_data['question'].strip(),
        'type': question_data['type'],
        'options': sorted([opt.strip() for opt in question_data['options']]),
        'correct_answer': sorted(question_data['correct_answer'])
    }
    # 計算SHA-256雜湊值
    content = json.dumps(normalized_data, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(content.encode('utf-8')).hexdigest()
```

### 去重邏輯
1. **數據標準化**：去除空格、排序選項、統一格式
2. **雜湊計算**：SHA-256確保唯一性與安全性  
3. **資料庫約束**：UNIQUE約束防止重複插入
4. **衝突處理**：重複題目自動跳過，不中斷導入流程

## API/路由架構

### 公開路由
- `GET /` - 首頁，測驗入口
- `POST /start_quiz` - 開始測驗，初始化session
- `GET /quiz/<int:question_id>` - 顯示題目
- `POST /quiz/<int:question_id>` - 提交答案
- `GET /results` - 顯示測驗結果

### API路由
- `GET /api/` - API根路由，重定向說明
- `GET /api/health` - 系統健康檢查
- `GET /api/questions` - 獲取題目列表
- `GET /api/statistics` - 獲取系統統計資料
- `POST /api/questions` - 新增題目 (管理員)
- `DELETE /api/questions/<int:question_id>` - 刪除題目 (管理員)
- `GET /admin` - 管理後台首頁
- `GET /admin/questions` - 題目管理列表
- `POST /admin/add_question` - 新增題目
- `POST /admin/delete_question/<int:question_id>` - 刪除題目
- `GET /admin/import` - 導入頁面
- `POST /admin/import` - 執行導入

### Session管理
```python
# 測驗狀態儲存
session['quiz_questions'] = [question_ids...]
session['current_question'] = 0
session['user_answers'] = {question_id: answer...}
session['quiz_start_time'] = timestamp
```

## 批量導入機制

### 自動導入腳本
```python
# import_base_questions.py
def import_all_json_files():
    base_dir = Path(__file__).parent / 'base'
    for json_file in base_dir.glob('*.json'):
        dm.import_questions_from_json(str(json_file))
```

### 導入流程控制
1. **檔案掃描**：自動發現base/目錄下所有.json檔
2. **格式驗證**：檢查JSON結構完整性
3. **批量處理**：逐題計算hash並插入
4. **錯誤處理**：記錄失敗項目，繼續處理後續
5. **統計報告**：返回成功/失敗/重複統計

## 關鍵維護點

### 1. 效能優化
```python
# 大量導入時的批量操作
def batch_import_questions(questions_data, batch_size=100):
    for i in range(0, len(questions_data), batch_size):
        batch = questions_data[i:i+batch_size]
        # 批量插入邏輯
```

### 2. 記憶體管理
- Session清理：測驗完成後及時清理session數據
- 大檔案處理：分塊讀取大型JSON檔案
- 連接池：資料庫連接重用與及時關閉

### 3. 錯誤處理
```python
# 資料庫操作錯誤處理
try:
    cursor.execute(sql, params)
    conn.commit()
except sqlite3.IntegrityError:
    # 重複題目，跳過
    pass
except Exception as e:
    # 記錄錯誤，繼續處理
    logger.error(f"Database error: {e}")
```

### 4. 數據一致性
- 事務管理：關鍵操作使用事務確保一致性
- 外鍵約束：維護資料關聯完整性
- 定期備份：自動備份資料庫檔案

## 擴展建議

### 水平擴展
1. **資料庫分片**：按題目類別或時間分片
2. **快取層**：Redis快取熱點題目
3. **負載均衡**：多實例部署

### 功能擴展
1. **用戶系統**：登入、權限管理
2. **題目分類**：科目、難度分級
3. **統計分析**：答題趨勢、難度分析
4. **API化**：RESTful API支援第三方整合

### 安全加固
1. **輸入驗證**：SQL注入防護
2. **CSRF保護**：跨站請求偽造防護  
3. **訪問控制**：管理功能權限控制

## 監控與除錯

### 日誌記錄
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 關鍵操作記錄
logger.info(f"Question imported: {question_id}")
logger.error(f"Import failed: {error_msg}")
```

### 效能監控
- 資料庫查詢時間
- 記憶體使用量
- 並發用戶數

### 常見問題排查
1. **導入失敗**：檢查JSON格式、編碼問題
2. **重複題目**：驗證hash計算邏輯
3. **Session丟失**：檢查Flask配置、記憶體限制
4. **資料庫鎖定**：檢查並發訪問、長事務

## 部署注意事項

### 生產環境配置
```python
# 安全配置
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True

# 資料庫配置
DATABASE_PATH = '/path/to/production/database.db'
```

### 資料庫維護
```sql
-- 定期整理資料庫
VACUUM;

-- 重建索引
REINDEX;

-- 檢查資料庫完整性
PRAGMA integrity_check;
```

## 🧪 測試架構 (v2.0新增)

### 測試資料夾結構
```
test/
├── README.md                   # 測試說明文檔
├── run_all_tests.py           # 一鍵執行所有測試
├── run_tests.bat              # Windows批處理檔案
├── run_tests.sh               # Linux/Mac執行腳本
├── ORGANIZE_REPORT.md         # 檔案整理報告
├── system_check.py            # 系統全面檢查
├── check_multiple_choice.py   # 多選題專項檢查
├── check_db.py                # 資料庫檢查
├── check_docker_env.py        # Docker環境檢查
├── test_import.py             # 導入功能測試
├── test_index.py              # 首頁功能測試
├── test_quiz.py               # 測驗功能測試
├── fix_api.py                 # API修復工具
├── init_db_fixed.py           # 修正版資料庫初始化
└── debug_stats.py             # 除錯統計工具
```

### 核心測試腳本
#### 1. 系統全面檢查 (`system_check.py`)
- **功能**：驗證資料庫、API、網頁、測驗功能
- **技術**：自動化HTTP請求測試，SQLite查詢驗證
- **輸出**：詳細的通過/失敗報告

#### 2. 多選題專項檢查 (`check_multiple_choice.py`)
- **功能**：驗證多選題載入、格式、答案索引
- **技術**：直接SQL查詢，數據格式驗證
- **關鍵指標**：多選題數量、答案格式正確性

#### 3. 一鍵測試執行器 (`run_all_tests.py`)
- **功能**：自動執行所有測試腳本並生成報告
- **技術**：subprocess調用，結果彙總
- **跨平台**：支援Windows (.bat) 和 Linux/Mac (.sh)

### 測試驗證重點
- ✅ 多選題完整流程：載入 → 顯示 → 判分
- ✅ API端點功能：CSRF保護已優化
- ✅ 資料庫完整性：題目數量、格式驗證
- ✅ 前端功能：頁面載入、表單提交

## 🔧 修復記錄與技術更新

### 2025年6月22日 - 多選題完整修復
**問題**：多選題載入、顯示和判分問題

**修復方案**：
1. **資料庫初始化優化** (`init_db_fixed.py`)
   - 文字答案自動轉換為索引格式
   - 支援多種JSON格式智能解析
   - 多選題正確答案格式：`"1,2,3"` (逗號分隔索引)

2. **API CSRF保護修復** (`app/__init__.py`)
   - 排除API藍圖的CSRF保護：`csrf.exempt(api_bp)`
   - 修正測驗創建API的400錯誤

3. **業務邏輯優化** (`quiz_service.py`)
   - 多選題判分算法優化
   - 正確答案比較邏輯修正
   - 支援動態答案格式轉換

**驗證結果**：
- ✅ 資料庫：72題總計，16題多選題，56題單選題
- ✅ API：所有端點正常回應 (201/200狀態碼)
- ✅ 測驗創建：會話ID正常生成，題目正確返回
- ✅ 多選題：載入、顯示、判分全流程正常

### 2025年6月22日 - 檔案結構重組
**目標**：統一測試檔案管理，提升維護效率

**重組內容**：
- 建立專用 `test/` 資料夾
- 移動12個測試相關檔案
- 修正相對路徑引用
- 建立跨平台執行腳本

**技術影響**：
- 📁 結構更專業化，符合軟體開發最佳實踐
- 🔧 便於CI/CD整合
- 📖 完整的測試文檔和使用指南

### 歷史修復記錄
#### API健康檢查修復 (初期)
- 新增 `get_total_count()` 和 `get_current_time()` 方法
- 修復Docker容器健康狀態檢查
- 確保API端點正常回應

---

**技術版本**：Flask 3.0.0 + SQLite 3 + Python 3.10+  
**架構模式**：MVC分層架構 + 模組化設計  
**測試覆蓋**：資料庫、API、前端、多選題專項測試  
**最後更新**：2025年6月22日 - 多選題功能完整修復與測試架構建立
