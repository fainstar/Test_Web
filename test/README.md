# 測試資料夾說明

此資料夾包含所有測試相關的腳本和檔案。

## 📁 檔案結構

### 🔍 系統檢查腳本
- `system_check.py` - 全面的系統檢查腳本，驗證資料庫、API、網頁和測驗功能
- `check_multiple_choice.py` - 專門檢查多選題載入情況
- `check_db.py` - 資料庫檢查工具
- `check_docker_env.py` - Docker 環境檢查

### 🧪 功能測試腳本
- `test_import.py` - 測試題目匯入功能
- `test_index.py` - 測試首頁功能
- `test_quiz.py` - 測試測驗功能

### 🔧 修復和工具腳本
- `fix_api.py` - API 修復工具
- `init_db_fixed.py` - 修正版的資料庫初始化腳本
- `debug_stats.py` - 除錯統計工具

### � 測試執行器
- `run_all_tests.py` - 一鍵執行所有測試的 Python 腳本
- `run_tests.bat` - Windows 批處理檔案
- `run_tests.sh` - Linux/Mac 執行腳本

### �📊 測試資料
- `test.json` - 測試用題目資料（空檔案）
- `test02.json` - 第二組測試用題目資料（空檔案）

## 🚀 使用方法

### 🎯 一鍵執行所有測試 (推薦)

**Windows:**
```cmd
cd test
run_tests.bat
```

**Linux/Mac:**
```bash
cd test
chmod +x run_tests.sh
./run_tests.sh
```

**手動執行:**
```bash
cd test
python run_all_tests.py
```

### 執行系統全面檢查
```bash
cd test
python system_check.py
```

### 檢查多選題狀態
```bash
cd test
python check_multiple_choice.py
```

### 檢查資料庫
```bash
cd test
python check_db.py
```

### Docker 環境檢查
```bash
cd test
python check_docker_env.py
```

## ⚠️ 注意事項

1. 所有測試腳本都應該從專案根目錄或 test 資料夾執行
2. 確保 Flask 應用正在運行（針對 API 和網頁測試）
3. 資料庫路徑相對於專案根目錄（`../dev_quiz_database.db`）
4. 測試腳本需要安裝相關依賴套件（參考 `requirements.txt`）

## 📝 測試報告

執行測試後，檢查輸出中的：
- ✅ 成功通過的項目
- ❌ 失敗的項目
- ⚠️ 警告信息

如有問題，請檢查相關日誌和錯誤信息。
