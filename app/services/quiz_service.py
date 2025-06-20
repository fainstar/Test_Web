"""
測驗服務層
處理測驗相關的業務邏輯
"""
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from app.models import QuizSession
from app.services.question_service import QuestionService
from config.config import get_config

class QuizService:
    """測驗服務類"""
    
    def __init__(self):
        config = get_config()
        self.session_model = QuizSession(config.DATABASE_PATH)
        self.question_service = QuestionService()
    
    def create_quiz_session(self, quiz_config: Dict[str, Any]) -> Dict[str, Any]:
        """創建測驗會話"""
        # 生成會話ID
        session_id = str(uuid.uuid4())
        
        # 獲取題目
        if quiz_config.get('advanced', False):
            questions = self.question_service.get_advanced_random_questions(quiz_config)
        else:
            questions = self.question_service.get_random_questions(
                count=quiz_config.get('count', 10),
                filters=quiz_config
            )
        
        if not questions:
            return {'success': False, 'message': '沒有找到符合條件的題目'}
        
        # 創建會話記錄
        try:
            self.session_model.create_session(session_id, questions, quiz_config)
            
            return {
                'success': True,
                'session_id': session_id,
                'questions': questions,
                'quiz_info': {
                    'title': quiz_config.get('title', '測驗'),
                    'description': quiz_config.get('description', ''),
                    'question_count': len(questions)
                }
            }
        except Exception as e:
            return {'success': False, 'message': f'創建測驗會話失敗: {str(e)}'}
    
    def submit_answer(self, session_id: str, question_id: int, 
                     user_answer: Any) -> Dict[str, Any]:
        """提交答案"""
        # 獲取題目信息
        question = self.question_service.get_question(question_id)
        if not question:
            return {'success': False, 'message': '題目不存在'}
        
        # 檢查答案正確性
        is_correct = self._check_answer(question, user_answer)
        
        # 記錄答案
        try:
            self.session_model.add_answer(session_id, question_id, user_answer, is_correct)
            
            return {
                'success': True,
                'is_correct': is_correct,
                'correct_answer': question['correct_answer']
            }
        except Exception as e:
            return {'success': False, 'message': f'提交答案失敗: {str(e)}'}
    
    def complete_quiz(self, session_id: str, start_time: str) -> Dict[str, Any]:
        """完成測驗"""
        try:
            # 計算持續時間
            start_dt = datetime.fromisoformat(start_time)
            end_dt = datetime.now()
            duration_minutes = (end_dt - start_dt).total_seconds() / 60
            
            # 獲取會話信息
            session = self.session_model.get_session(session_id)
            if not session:
                return {'success': False, 'message': '會話不存在'}
            
            # 獲取答題記錄
            answers = self.session_model.get_session_answers(session_id)
            
            # 計算分數
            total_questions = len(answers)
            correct_answers = sum(1 for answer in answers if answer['is_correct'])
            score_percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
            
            # 更新會話狀態
            self.session_model.complete_session(session_id, score_percentage, duration_minutes)
            
            return {
                'success': True,
                'results': {
                    'session_id': session_id,
                    'total_questions': total_questions,
                    'correct_answers': correct_answers,
                    'score_percentage': round(score_percentage, 2),
                    'duration_minutes': round(duration_minutes, 2),
                    'detailed_answers': self._format_detailed_answers(answers)
                }
            }
        except Exception as e:
            return {'success': False, 'message': f'完成測驗失敗: {str(e)}'}
    
    def get_quiz_results(self, session_id: str) -> Optional[Dict[str, Any]]:
        """獲取測驗結果"""
        session = self.session_model.get_session(session_id)
        if not session:
            return None
        
        answers = self.session_model.get_session_answers(session_id)
        
        return {
            'session_info': session,
            'detailed_answers': self._format_detailed_answers(answers),
            'summary': {
                'total_questions': session['total_questions'],
                'correct_answers': session['correct_answers'],
                'score_percentage': session['score_percentage'],
                'duration_minutes': session['duration_minutes']
            }
        }
    
    def get_recent_sessions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """獲取最近的測驗會話"""
        return self.session_model.get_recent_sessions(limit)
    
    def get_statistics(self) -> Dict[str, Any]:
        """獲取測驗統計信息"""
        return self.session_model.get_statistics()
    
    def _check_answer(self, question: Dict[str, Any], user_answer: Any) -> bool:
        """檢查答案是否正確"""
        correct_answers = question['correct_answer']
        
        if question['type'] == 'single':
            # 單選題
            if isinstance(user_answer, list):
                user_answer = user_answer[0] if user_answer else -1
            return user_answer in correct_answers
        else:
            # 多選題
            if not isinstance(user_answer, list):
                user_answer = [user_answer]
            
            # 排序後比較
            return sorted(user_answer) == sorted(correct_answers)
    
    def _format_detailed_answers(self, answers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """格式化詳細答案信息"""
        formatted_answers = []
        
        for answer in answers:
            user_answer = answer['user_answer']
            correct_answers = answer['correct_answers']
            options = answer['options']
            
            # 格式化用戶答案
            if isinstance(user_answer, list):
                user_answer_text = [options[i] for i in user_answer if i < len(options)]
            else:
                user_answer_text = [options[user_answer]] if user_answer < len(options) else ['未選擇']
            
            # 格式化正確答案
            correct_answer_text = [options[i] for i in correct_answers if i < len(options)]
            
            formatted_answers.append({
                'question_id': answer['question_id'],
                'question_text': answer['question_text'],
                'user_answer': user_answer,
                'user_answer_text': user_answer_text,
                'correct_answers': correct_answers,
                'correct_answer_text': correct_answer_text,
                'is_correct': answer['is_correct'],
                'options': options
            })
        
        return formatted_answers
