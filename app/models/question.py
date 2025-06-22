"""
題目數據模型
處理題目相關的數據庫操作
"""
import hashlib
import json
import random
from typing import List, Dict, Any, Optional
from .base import BaseModel

class Question(BaseModel):
    """題目模型"""
    
    def __init__(self, db_path: str):
        super().__init__(db_path)
        self.init_table()
    
    def init_table(self):
        """初始化題目表"""
        query = '''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_hash TEXT UNIQUE NOT NULL,
                question_text TEXT NOT NULL,
                question_type TEXT NOT NULL CHECK (question_type IN ('single_choice', 'multiple_choice')),
                options TEXT NOT NULL,
                correct_answer TEXT,
                correct_answers TEXT,
                category TEXT DEFAULT '一般',
                difficulty TEXT DEFAULT '中等',
                explanation TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        '''
        self.execute_query(query)
        
        # 創建索引
        self.execute_query('CREATE INDEX IF NOT EXISTS idx_question_hash ON questions (question_hash)')
        self.execute_query('CREATE INDEX IF NOT EXISTS idx_question_type ON questions (question_type)')
        self.execute_query('CREATE INDEX IF NOT EXISTS idx_category ON questions (category)')
        self.execute_query('CREATE INDEX IF NOT EXISTS idx_difficulty ON questions (difficulty)')
    
    def generate_hash(self, question_text: str, options: List[str]) -> str:
        """生成題目的hash值"""
        content = question_text + '|' + '|'.join(sorted(options))
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def add(self, question_data: Dict[str, Any]) -> tuple[int, bool]:
        """
        添加題目
        
        Returns:
            tuple: (question_id, is_new)
        """
        question_hash = self.generate_hash(
            question_data['question_text'], 
            question_data['options']
        )
        
        # 檢查是否已存在
        existing = self.execute_query(
            'SELECT id FROM questions WHERE question_hash = ?', 
            (question_hash,)
        )
        
        if existing:
            return existing[0]['id'], False
        
        # 插入新題目
        query = '''
            INSERT INTO questions (
                question_hash, question_text, question_type, options, 
                correct_answer, correct_answers, category, difficulty, explanation
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        params = (
            question_hash,
            question_data['question_text'],
            question_data['question_type'],
            json.dumps(question_data['options'], ensure_ascii=False),
            question_data.get('correct_answer'),
            json.dumps(question_data.get('correct_answers', []), ensure_ascii=False),
            question_data.get('category', '一般'),
            question_data.get('difficulty', '中等'),
            question_data.get('explanation', '')
        )
        
        question_id = self.execute_insert(query, params)
        return question_id, True
    
    def get_by_id(self, question_id: int) -> Optional[Dict[str, Any]]:
        """根據ID獲取題目"""
        rows = self.execute_query(
            'SELECT * FROM questions WHERE id = ?', 
            (question_id,)
        )
        
        if not rows:
            return None
        
        return self._format_question(rows[0])
    
    def update(self, question_id: int, question_data: Dict[str, Any]) -> bool:
        """更新題目"""
        try:
            # 生成新的hash值
            question_hash = self.generate_hash(
                question_data['question_text'], 
                question_data['options']
            )
            
            # 檢查是否與其他題目重複（排除自己）
            existing = self.execute_query(
                'SELECT id FROM questions WHERE question_hash = ? AND id != ?', 
                (question_hash, question_id)
            )
            
            if existing:
                return False  # 與其他題目重複
            
            # 更新題目
            query = '''
                UPDATE questions SET 
                    question_hash = ?, question_text = ?, question_type = ?, options = ?,
                    correct_answer = ?, correct_answers = ?, category = ?, difficulty = ?, 
                    explanation = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            '''
            
            params = (
                question_hash,
                question_data['question_text'],
                question_data['question_type'],
                json.dumps(question_data['options'], ensure_ascii=False),
                question_data.get('correct_answer'),
                json.dumps(question_data.get('correct_answers', []), ensure_ascii=False),
                question_data.get('category', '一般'),
                question_data.get('difficulty', '中等'),
                question_data.get('explanation', ''),
                question_id
            )
            
            result = self.execute_query(query, params)
            return True
            
        except Exception as e:
            print(f"Error updating question: {e}")
            return False
    
    def get_all(self, page: int = 1, per_page: int = 20, 
                category: str = None, difficulty: str = None,
                question_type: str = None) -> Dict[str, Any]:
        """獲取所有題目（分頁）"""
        offset = (page - 1) * per_page
        
        # 構建查詢條件
        where_conditions = []
        params = []
        
        if category:
            where_conditions.append('category = ?')
            params.append(category)
        
        if difficulty:
            where_conditions.append('difficulty = ?')
            params.append(difficulty)
        
        if question_type:
            where_conditions.append('question_type = ?')
            params.append(question_type)
        
        where_clause = ' WHERE ' + ' AND '.join(where_conditions) if where_conditions else ''
        
        # 獲取總數
        count_query = f'SELECT COUNT(*) as total FROM questions{where_clause}'
        total = self.execute_query(count_query, tuple(params))[0]['total']
        
        # 獲取數據
        data_query = f'''
            SELECT * FROM questions{where_clause} 
            ORDER BY created_at DESC 
            LIMIT ? OFFSET ?
        '''
        params.extend([per_page, offset])
        rows = self.execute_query(data_query, tuple(params))
        
        questions = [self._format_question(row) for row in rows]
        
        return {
            'questions': questions,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        }
    
    def get_random(self, count: int = 10, category: str = None, 
                   difficulty: str = None, question_type: str = None) -> List[Dict[str, Any]]:
        """隨機獲取題目"""
        # 構建查詢條件
        where_conditions = []
        params = []
        
        if category:
            where_conditions.append('category = ?')
            params.append(category)
        
        if difficulty:
            where_conditions.append('difficulty = ?')
            params.append(difficulty)
        
        if question_type:
            where_conditions.append('question_type = ?')
            params.append(question_type)
        
        where_clause = ' WHERE ' + ' AND '.join(where_conditions) if where_conditions else ''
        
        query = f'SELECT * FROM questions{where_clause} ORDER BY RANDOM() LIMIT ?'
        params.append(count)
        
        rows = self.execute_query(query, tuple(params))
        return [self._format_question(row) for row in rows]
    
    def delete(self, question_id: int) -> bool:
        """刪除題目"""
        affected = self.execute_delete(
            'DELETE FROM questions WHERE id = ?', 
            (question_id,)
        )
        return affected > 0
    
    def get_statistics(self) -> Dict[str, Any]:
        """獲取題目統計信息"""
        # 總題目數
        total = self.execute_query('SELECT COUNT(*) as count FROM questions')[0]['count']
        
        # 按類型統計
        type_stats = {}
        rows = self.execute_query('''
            SELECT question_type, COUNT(*) as count 
            FROM questions 
            GROUP BY question_type
        ''')
        for row in rows:
            type_stats[row['question_type']] = row['count']
        
        # 按分類統計
        category_stats = {}
        rows = self.execute_query('''
            SELECT category, COUNT(*) as count 
            FROM questions 
            GROUP BY category
        ''')
        for row in rows:
            category_stats[row['category']] = row['count']        
        # 按難度統計
        difficulty_stats = {}
        rows = self.execute_query('''
            SELECT difficulty, COUNT(*) as count 
            FROM questions 
            GROUP BY difficulty
        ''')
        for row in rows:
            difficulty_stats[row['difficulty']] = row['count']
        
        return {
            'total_questions': total,            'type_stats': type_stats,
            'category_stats': category_stats,
            'difficulty_stats': difficulty_stats
        }
    
    def _format_question(self, row) -> Dict[str, Any]:
        """格式化題目數據"""
        options = json.loads(row['options'])
        
        # 處理正確答案
        if row['question_type'] == 'multiple_choice':
            # 多選題：從 correct_answers 字段讀取
            if row['correct_answers']:
                try:
                    correct_answer_data = json.loads(row['correct_answers'])
                    # 確保是索引列表
                    if isinstance(correct_answer_data, list):
                        correct_answer = [int(x) for x in correct_answer_data if isinstance(x, (int, str)) and str(x).isdigit()]
                    else:
                        correct_answer = []
                except (json.JSONDecodeError, TypeError):
                    # 如果 correct_answers 解析失敗，嘗試從 correct_answer 字段解析
                    if row['correct_answer'] and ',' in str(row['correct_answer']):
                        try:
                            correct_answer = [int(x.strip()) for x in str(row['correct_answer']).split(',')]
                        except ValueError:
                            correct_answer = []
                    else:
                        correct_answer = []
            else:
                # 如果 correct_answers 為空，嘗試從 correct_answer 字段解析
                if row['correct_answer'] and ',' in str(row['correct_answer']):
                    try:
                        correct_answer = [int(x.strip()) for x in str(row['correct_answer']).split(',')]
                    except ValueError:
                        correct_answer = []
                else:
                    correct_answer = []
        else:
            # 單選題：從 correct_answer 字段讀取
            if row['correct_answer'] is not None:
                try:
                    correct_answer = int(row['correct_answer'])
                except (ValueError, TypeError):
                    correct_answer = 0
            else:
                correct_answer = 0        
        return {
            'id': row['id'],
            'question': row['question_text'],
            'type': 'single' if row['question_type'] == 'single_choice' else ('multiple' if row['question_type'] == 'multiple_choice' else row['question_type']),
            'options': options,
            'correct_answer': correct_answer,
            'category': row['category'],
            'difficulty': row['difficulty'],
            'explanation': row['explanation'],
            'created_at': row['created_at']
        }
