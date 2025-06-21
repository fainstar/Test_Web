"""
數據庫初始化腳本
創建數據庫表結構並可選擇導入初始數據
"""
import os
import sys
import json
from pathlib import Path

# 添加專案根目錄到Python路徑
sys.path.insert(0, str(Path(__file__).parent))

from app.models import Question, QuizSession
from config.config import get_config

def init_database():
    """初始化數據庫"""
    print("🔄 正在初始化數據庫...")
    
    config = get_config()
    db_path = config.DATABASE_PATH
    
    # 確保數據庫目錄存在
    db_dir = Path(db_path).parent
    if db_dir != Path('.'):
        db_dir.mkdir(parents=True, exist_ok=True)
        print(f"📁 數據庫目錄: {db_dir}")
    
    print(f"🗄️ 數據庫路徑: {db_path}")
    
    try:
        # 初始化模型（會自動創建表）
        question_model = Question(db_path)
        session_model = QuizSession(db_path)
        
        print("✅ 數據庫表結構創建完成")
        
        # 檢查是否需要導入初始數據
        base_dir = Path(__file__).parent / 'base'
        if base_dir.exists():
            import_initial_data(question_model, base_dir)
        
        print("🎉 數據庫初始化完成！")
    except Exception as e:
        print(f"❌ 數據庫初始化失敗: {e}")
        raise

def import_initial_data(question_model, base_dir):
    """導入初始數據"""
    print("📥 正在導入初始題目數據...")
    
    json_files = list(base_dir.glob('*.json'))
    if not json_files:
        print("⚠️  未找到初始數據文件")
        return
    
    total_success = 0
    total_skipped = 0
    
    for json_file in json_files:
        print(f"📖 正在處理: {json_file.name}")
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
              # 處理不同的JSON格式
            if 'quiz' in data and 'questions' in data['quiz']:
                questions = data['quiz']['questions']
            elif 'questions' in data:
                questions = data['questions']
            elif isinstance(data, list):
                questions = data
            else:
                print(f"⚠️  {json_file.name} 格式不正確，跳過")
                continue
            
            success_count = 0
            skip_count = 0
            
            for question_data in questions:
                # 轉換格式
                normalized_data = normalize_question_format(question_data)
                
                if normalized_data:
                    question_id, is_new = question_model.add(normalized_data)
                    if is_new:
                        success_count += 1
                    else:
                        skip_count += 1
            
            print(f"✅ {json_file.name}: 新增 {success_count} 題，跳過 {skip_count} 題")
            total_success += success_count
            total_skipped += skip_count
            
        except Exception as e:
            print(f"❌ 處理 {json_file.name} 時出錯: {e}")
    
    print(f"📊 總計: 新增 {total_success} 題，跳過 {total_skipped} 題")

def normalize_question_format(question_data):
    """標準化題目格式"""
    try:
        # 處理不同的題目格式
        if 'question' in question_data:
            question_text = question_data['question']
        elif 'question_text' in question_data:
            question_text = question_data['question_text']
        else:
            return None
        
        # 處理題目類型
        question_type = question_data.get('type', 'single')
        if question_type in ['single_choice', 'single']:
            question_type = 'single_choice'
        elif question_type in ['multiple_choice', 'multiple']:
            question_type = 'multiple_choice'
        else:
            question_type = 'single_choice'
        
        # 處理選項
        options = question_data.get('options', [])
        if not options:
            return None
        
        # 處理正確答案
        correct_answer = None
        correct_answers = []
        
        if 'correct_answer' in question_data:
            ca = question_data['correct_answer']
            
            if isinstance(ca, str):
                # 如果是文字答案，找到對應的索引
                try:
                    ca_index = options.index(ca)
                    correct_answer = str(ca_index)
                    correct_answers = [ca_index]
                except ValueError:
                    print(f"⚠️  找不到答案 '{ca}' 在選項中")
                    return None
            elif isinstance(ca, int):
                correct_answer = str(ca)
                correct_answers = [ca]
            elif isinstance(ca, list):
                # 處理多選答案
                correct_answers = []
                for ans in ca:
                    if isinstance(ans, str):
                        try:
                            ans_index = options.index(ans)
                            correct_answers.append(ans_index)
                        except ValueError:
                            print(f"⚠️  找不到答案 '{ans}' 在選項中")
                            return None
                    elif isinstance(ans, int):
                        correct_answers.append(ans)
                
                if question_type == 'single_choice' and correct_answers:
                    correct_answer = str(correct_answers[0])
                    
        elif 'correct_answers' in question_data:
            correct_answers = question_data['correct_answers']
            if isinstance(correct_answers, list) and correct_answers:
                if question_type == 'single_choice':
                    correct_answer = str(correct_answers[0])
        
        # 如果沒有找到正確答案，跳過這個題目
        if not correct_answers:
            print(f"⚠️  題目缺少正確答案: {question_text[:50]}...")
            return None
        
        return {
            'question_text': question_text,
            'question_type': question_type,
            'options': options,
            'correct_answer': correct_answer,
            'correct_answers': correct_answers,
            'category': question_data.get('category', '一般'),
            'difficulty': question_data.get('difficulty', '中等'),
            'explanation': question_data.get('explanation', '')
        }
        
    except Exception as e:
        print(f"⚠️  標準化題目格式時出錯: {e}")
        return None

if __name__ == '__main__':
    init_database()
