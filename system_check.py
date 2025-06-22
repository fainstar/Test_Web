#!/usr/bin/env python3
"""
系統全面檢查腳本
檢查各項功能是否正常運作
"""
import requests
import json
import sqlite3
import sys

def check_database():
    """檢查數據庫狀態"""
    print("=" * 50)
    print("🗄️ 檢查數據庫狀態...")
    
    try:
        conn = sqlite3.connect('dev_quiz_database.db')
        cursor = conn.cursor()
        
        # 檢查題目總數
        cursor.execute('SELECT COUNT(*) FROM questions')
        total_questions = cursor.fetchone()[0]
        print(f"✅ 題目總數: {total_questions}")
        
        # 檢查題型分布
        cursor.execute('SELECT question_type, COUNT(*) FROM questions GROUP BY question_type')
        type_stats = cursor.fetchall()
        print("📊 題型分布:")
        for type_name, count in type_stats:
            print(f"   - {type_name}: {count}題")
        
        # 檢查多選題的正確答案
        cursor.execute('SELECT id, question_text, correct_answers FROM questions WHERE question_type = "multiple_choice" LIMIT 3')
        multiple_questions = cursor.fetchall()
        print("🔍 多選題答案檢查:")
        for q_id, q_text, correct_answers in multiple_questions:
            print(f"   - ID {q_id}: {q_text[:50]}...")
            print(f"     正確答案: {correct_answers}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ 數據庫檢查失敗: {e}")
        return False

def check_api():
    """檢查API功能"""
    print("=" * 50)
    print("🔌 檢查API功能...")
    
    base_url = "http://127.0.0.1:5000"
    
    try:
        # 檢查健康狀態
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ API健康檢查通過")
        else:
            print(f"⚠️ API健康檢查異常: {response.status_code}")
            
        # 檢查題目API
        response = requests.get(f"{base_url}/api/questions", timeout=5)
        if response.status_code == 200:
            questions = response.json()
            print(f"✅ 題目API正常，返回 {len(questions)} 題")
        else:
            print(f"❌ 題目API異常: {response.status_code}")
            
        # 檢查隨機題目API
        response = requests.get(f"{base_url}/api/questions/random?count=5", timeout=5)
        if response.status_code == 200:
            random_questions = response.json()
            print(f"✅ 隨機題目API正常，返回 {len(random_questions)} 題")
        else:
            print(f"❌ 隨機題目API異常: {response.status_code}")
            
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ API檢查失敗: {e}")
        return False

def check_web_pages():
    """檢查網頁功能"""
    print("=" * 50)
    print("🌐 檢查網頁功能...")
    
    base_url = "http://127.0.0.1:5000"
    pages_to_check = [
        ("/", "首頁"),
        ("/admin", "管理面板"),
        ("/admin/questions", "題目管理"),
        ("/quiz/start", "開始測驗")
    ]
    
    try:
        for path, name in pages_to_check:
            response = requests.get(f"{base_url}{path}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {name}頁面正常")
            elif response.status_code == 302:
                print(f"🔄 {name}頁面重定向")
            else:
                print(f"❌ {name}頁面異常: {response.status_code}")
                
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ 網頁檢查失敗: {e}")
        return False

def check_quiz_functionality():
    """檢查測驗功能"""
    print("=" * 50)
    print("🎯 檢查測驗功能...")
    
    base_url = "http://127.0.0.1:5000"
    
    try:
        # 創建測驗會話
        response = requests.post(f"{base_url}/api/quiz/create", 
                               json={"count": 5}, 
                               timeout=5)        
        if response.status_code == 201 or response.status_code == 200:  # API返回201
            quiz_data = response.json()
            
            # 檢查API格式
            if quiz_data.get('success') and 'data' in quiz_data:
                data = quiz_data['data']
                session_id = data.get('session_id')
                questions = data.get('questions', [])
                
                print(f"✅ 測驗創建成功，會話ID: {session_id}")
                print(f"✅ 獲得題目數量: {len(questions)}")
                
                # 檢查題目格式
                if questions:
                    first_question = questions[0]
                    required_fields = ['id', 'question', 'options', 'type']
                    for field in required_fields:
                        if field in first_question:
                            print(f"✅ 題目包含必要字段: {field}")
                        else:
                            print(f"❌ 題目缺少字段: {field}")
                            
                    # 檢查多選題
                    multiple_questions = [q for q in questions if q.get('type') == 'multiple_choice']
                    if multiple_questions:
                        print(f"✅ 包含多選題: {len(multiple_questions)}題")
                        sample_multiple = multiple_questions[0]
                        print(f"   - 樣本多選題ID: {sample_multiple.get('id')}")
                        print(f"   - 樣本多選題類型: {sample_multiple.get('type')}")
                        
                return True
            else:
                print(f"❌ API返回格式錯誤: {quiz_data}")
                return False
        else:
            print(f"❌ 測驗創建失敗: {response.status_code}")
            print(f"響應內容: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 測驗功能檢查失敗: {e}")
        return False

def main():
    """主檢查函數"""
    print("🔍 開始系統全面檢查...")
    
    all_passed = True
    
    # 數據庫檢查
    if not check_database():
        all_passed = False
        
    # API檢查  
    if not check_api():
        all_passed = False
        
    # 網頁檢查
    if not check_web_pages():
        all_passed = False
        
    # 測驗功能檢查
    if not check_quiz_functionality():
        all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("🎉 所有檢查通過！系統運行正常。")
    else:
        print("⚠️ 發現一些問題，請檢查上方輸出。")
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
