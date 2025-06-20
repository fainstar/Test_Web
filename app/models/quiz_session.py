"""
測驗會話數據模型
處理測驗會話相關的數據庫操作
"""
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from .base import BaseModel

class QuizSession(BaseModel):
    """測驗會話模型"""
    
    def __init__(self, db_path: str):
        super().__init__(db_path)
        self.init_tables()
    
    def init_tables(self):
        """初始化相關表"""
        # 測驗會話表
        session_query = '''
            CREATE TABLE IF NOT EXISTS quiz_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                total_questions INTEGER NOT NULL,
                correct_answers INTEGER NOT NULL,
                score_percentage REAL NOT NULL,
                duration_minutes REAL NOT NULL,
                quiz_config TEXT,
                started_at TIMESTAMP NOT NULL,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        '''
        self.execute_query(session_query)
        
        # 答題記錄表
        answer_query = '''
            CREATE TABLE IF NOT EXISTS user_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                question_id INTEGER NOT NULL,
                user_answer TEXT,
                is_correct BOOLEAN NOT NULL,
                answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (question_id) REFERENCES questions (id)
            )
        '''
        self.execute_query(answer_query)
        
        # 創建索引
        self.execute_query('CREATE INDEX IF NOT EXISTS idx_session_id ON quiz_sessions (session_id)')
        self.execute_query('CREATE INDEX IF NOT EXISTS idx_user_answers_session ON user_answers (session_id)')
    
    def create_session(self, session_id: str, questions: List[Dict[str, Any]], 
                      quiz_config: Dict[str, Any] = None) -> int:
        """創建新的測驗會話"""
        query = '''
            INSERT INTO quiz_sessions (
                session_id, total_questions, correct_answers, 
                score_percentage, duration_minutes, quiz_config, started_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        
        params = (
            session_id,
            len(questions),
            0,  # 初始正確答案數
            0.0,  # 初始分數
            0.0,  # 初始持續時間
            json.dumps(quiz_config or {}, ensure_ascii=False),
            datetime.now().isoformat()
        )
        
        return self.execute_insert(query, params)
    
    def add_answer(self, session_id: str, question_id: int, 
                   user_answer: Any, is_correct: bool) -> int:
        """添加答題記錄"""
        query = '''
            INSERT INTO user_answers (session_id, question_id, user_answer, is_correct)
            VALUES (?, ?, ?, ?)
        '''
        
        params = (
            session_id,
            question_id,
            json.dumps(user_answer, ensure_ascii=False),
            is_correct
        )
        
        return self.execute_insert(query, params)
    
    def complete_session(self, session_id: str, score: float, 
                        duration_minutes: float) -> bool:
        """完成測驗會話"""
        # 計算正確答案數
        correct_count = self.execute_query('''
            SELECT COUNT(*) as count FROM user_answers 
            WHERE session_id = ? AND is_correct = 1
        ''', (session_id,))[0]['count']
        
        # 更新會話記錄
        query = '''
            UPDATE quiz_sessions 
            SET correct_answers = ?, score_percentage = ?, 
                duration_minutes = ?, completed_at = ?
            WHERE session_id = ?
        '''
        
        params = (
            correct_count,
            score,
            duration_minutes,
            datetime.now().isoformat(),
            session_id
        )
        
        affected = self.execute_update(query, params)
        return affected > 0
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """獲取測驗會話信息"""
        rows = self.execute_query('''
            SELECT * FROM quiz_sessions WHERE session_id = ?
        ''', (session_id,))
        
        if not rows:
            return None
        
        session = dict(rows[0])
        session['quiz_config'] = json.loads(session['quiz_config']) if session['quiz_config'] else {}
        
        return session
    
    def get_session_answers(self, session_id: str) -> List[Dict[str, Any]]:
        """獲取會話的所有答題記錄"""
        rows = self.execute_query('''
            SELECT ua.*, q.question_text, q.options, q.correct_answers
            FROM user_answers ua
            JOIN questions q ON ua.question_id = q.id
            WHERE ua.session_id = ?
            ORDER BY ua.answered_at
        ''', (session_id,))
        
        answers = []
        for row in rows:
            answer = dict(row)
            answer['user_answer'] = json.loads(answer['user_answer'])
            answer['options'] = json.loads(answer['options'])
            answer['correct_answers'] = json.loads(answer['correct_answers']) if answer['correct_answers'] else []
            answers.append(answer)
        
        return answers
    
    def get_recent_sessions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """獲取最近的測驗會話"""
        rows = self.execute_query('''
            SELECT * FROM quiz_sessions 
            ORDER BY completed_at DESC 
            LIMIT ?
        ''', (limit,))
        
        sessions = []
        for row in rows:
            session = dict(row)
            session['quiz_config'] = json.loads(session['quiz_config']) if session['quiz_config'] else {}
            sessions.append(session)
        
        return sessions
    
    def get_statistics(self) -> Dict[str, Any]:
        """獲取測驗統計信息"""
        # 總測驗次數
        total_sessions = self.execute_query('SELECT COUNT(*) as count FROM quiz_sessions')[0]['count']
        
        # 平均分數
        avg_score = self.execute_query('''
            SELECT AVG(score_percentage) as avg_score FROM quiz_sessions
            WHERE score_percentage > 0
        ''')[0]['avg_score'] or 0
        
        # 平均用時
        avg_duration = self.execute_query('''
            SELECT AVG(duration_minutes) as avg_duration FROM quiz_sessions
            WHERE duration_minutes > 0
        ''')[0]['avg_duration'] or 0
        
        # 最高分
        max_score = self.execute_query('''
            SELECT MAX(score_percentage) as max_score FROM quiz_sessions
        ''')[0]['max_score'] or 0
        
        return {
            'total_sessions': total_sessions,
            'average_score': round(avg_score, 2),
            'average_duration': round(avg_duration, 2),
            'highest_score': round(max_score, 2)
        }
