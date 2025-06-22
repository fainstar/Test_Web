# 線上測驗系統 - AI Agent 技術文件

本文件為AI agent提供系統架構、數據流、關鍵技術點與維護重點的技術參考。

## 系統架構概覽

### 技術棧
- **後端**：Python 3.7+ + Flask 3.0.0
- **資料庫**：SQLite 3 (單檔案資料庫)
- **前端**：HTML5 + CSS3 + JavaScript (原生)
- **哈希演算法**：SHA-256 (題目去重)

### 核心模組
```
app.py                 # Flask主應用，路由與業務邏輯
database_manager.py    # 資料庫管理，CRUD操作，hash去重
import_base_questions.py # 批量導入腳本
```

## 資料流與架構

### 1. 題目導入流程
```
JSON檔案 → hash計算 → 重複檢查 → 資料庫插入 → 索引更新
```

**關鍵實作**：
- `database_manager.py::calculate_question_hash()` - SHA-256雜湊計算
- `database_manager.py::add_question()` - 自動去重插入
- `database_manager.py::import_questions_from_json()` - 批量處理

### 2. 測驗執行流程
```
隨機抽題 → Session儲存 → 逐題顯示 → 答案收集 → 成績計算 → 結果展示
```

**關鍵實作**：
- `app.py::/start_quiz` - 隨機抽題並初始化session
- `app.py::/quiz/<int:question_id>` - 題目顯示與答案處理
- `app.py::/results` - 成績計算與統計

### 3. 管理後台流程
```
題目CRUD → 批量導入 → 統計查詢 → 資料維護
```

## 資料庫結構

### 主表：questions
```sql
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

## 修復記錄

### 2025年6月22日 - API健康檢查修復
**問題**：`/api/health` 路由出現 `'QuestionService' object has no attribute 'get_total_count'` 錯誤

**修復方案**：
在 `app/services/question_service.py` 中新增缺少的方法：
- `get_total_count()` - 獲取題目總數
- `get_current_time()` - 獲取當前時間

**影響範圍**：
- ✅ 修復健康檢查API (`/api/health`)
- ✅ 確保Docker容器健康狀態檢查正常
- ✅ 維持所有其他API功能正常

**驗證結果**：
- Docker容器狀態：healthy
- API回應：所有端點正常 (200狀態碼)
- Web界面：正常運作

---

**技術版本**：Flask 3.0.0 + SQLite 3 + Python 3.7+  
**架構模式**：MVC + 單體應用  
**最後更新**：2025年6月22日
