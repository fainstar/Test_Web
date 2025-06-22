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
            
            return {                'success': True,
                'is_correct': is_correct,
                'correct_answer': question['correct_answer']
            }
        except Exception as e:
            return {'success': False, 'message': f'提交答案失敗: {str(e)}'}

    def complete_quiz(self, session_id: str, start_time: str) -> Dict[str, Any]:
        """完成測驗"""
        try:
            # 計算持續時間
            if start_time:
                start_dt = datetime.fromisoformat(start_time)
                end_dt = datetime.now()
                duration_minutes = (end_dt - start_dt).total_seconds() / 60
            else:
                duration_minutes = 0
            
            # 獲取會話信息
            session = self.session_model.get_session(session_id)
            if not session:
                return {'success': False, 'message': '會話不存在'}
            
            # 獲取答題記錄
            answers = self.session_model.get_session_answers(session_id)
            
            # 計算分數
            total_questions = len(answers)
            correct_count = sum(1 for answer in answers if answer['is_correct'])
            score_percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
            
            # 計算等級
            if score_percentage >= 90:
                grade = "優秀"
            elif score_percentage >= 80:
                grade = "良好"
            elif score_percentage >= 70:
                grade = "中等"
            elif score_percentage >= 60:
                grade = "及格"
            else:
                grade = "不及格"
            
            # 更新會話狀態
            self.session_model.complete_session(session_id, score_percentage, duration_minutes)
            
            # 格式化詳細結果
            detailed_results = self._format_detailed_results(answers)
            
            return {
                'success': True,
                'results': {
                    'session_id': session_id,
                    'total_questions': total_questions,
                    'correct_count': correct_count,
                    'score_percentage': round(score_percentage, 2),
                    'grade': grade,
                    'duration_minutes': round(duration_minutes, 2),
                    'detailed_results': detailed_results
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
            'session_info': session,            'detailed_answers': self._format_detailed_answers(answers),
            'summary': {
                'total_questions': session['total_questions'],
                'correct_answers': session['correct_answers'],
                'score_percentage': session['score_percentage'],
                'duration_minutes': session['duration_minutes']
            }
        }
    
    def get_recent_sessions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """獲取最近的測驗會話"""
        sessions = self.session_model.get_recent_sessions(limit)
        
        # 將日期字符串轉換為 datetime 對象
        for session in sessions:
            if session.get('started_at'):
                try:
                    session['started_at'] = datetime.fromisoformat(session['started_at'])
                except (ValueError, TypeError):
                    session['started_at'] = None
            
            if session.get('completed_at'):
                try:
                    session['completed_at'] = datetime.fromisoformat(session['completed_at'])
                except (ValueError, TypeError):
                    session['completed_at'] = None
        
        return sessions
    
    def get_statistics(self) -> Dict[str, Any]:
        """獲取測驗統計信息"""
        return self.session_model.get_statistics()
    
    def create_session(self, questions: List[Dict[str, Any]], quiz_config: Dict[str, Any]) -> str:
        """創建測驗會話（簡化版本）
        
        Args:
            questions: 題目列表
            quiz_config: 測驗配置
            
        Returns:
            str: 會話ID
        """
        # 生成會話ID
        session_id = str(uuid.uuid4())        # 創建會話記錄
        try:
            self.session_model.create_session(session_id, questions, quiz_config)
            return session_id
        except Exception as e:
            raise Exception(f'創建測驗會話失敗: {str(e)}')

    def _check_answer(self, question: Dict[str, Any], user_answer: Any) -> bool:
        """檢查答案是否正確"""
        correct_answers = question['correct_answer']
        
        print(f"DEBUG: _check_answer - question_id: {question.get('id')}")
        print(f"DEBUG: _check_answer - user_answer: {user_answer} (type: {type(user_answer)})")
        print(f"DEBUG: _check_answer - correct_answers: {correct_answers} (type: {type(correct_answers)})")
        
        if question['type'] == 'single':
            # 單選題：正確答案格式處理
            if isinstance(correct_answers, list):
                correct_answer = correct_answers[0] if correct_answers else 0
            else:
                correct_answer = correct_answers
            
            # 用戶答案格式處理
            if isinstance(user_answer, list):
                user_answer_value = user_answer[0] if user_answer else -1
            elif isinstance(user_answer, str) and user_answer.isdigit():
                user_answer_value = int(user_answer)
            else:
                user_answer_value = user_answer
            
            print(f"DEBUG: _check_answer - comparing {user_answer_value} == {correct_answer}")
            result = user_answer_value == correct_answer
            print(f"DEBUG: _check_answer - result: {result}")
            return result
        else:
            # 多選題
            if not isinstance(user_answer, list):
                if isinstance(user_answer, str) and user_answer.isdigit():
                    user_answer = [int(user_answer)]
                else:
                    user_answer = [user_answer]
            else:
                # 確保用戶答案是整數列表
                user_answer = [int(x) if isinstance(x, str) and x.isdigit() else x for x in user_answer]
            
            # 確保正確答案是列表
            if not isinstance(correct_answers, list):
                correct_answers = [correct_answers]
            
            # 排序後比較
            result = sorted(user_answer) == sorted(correct_answers)
            print(f"DEBUG: _check_answer - multiple choice result: {result}")
            return result

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

    def _format_detailed_results(self, answers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """格式化詳細結果供模板使用"""
        detailed_results = []
        
        for answer in answers:
            user_answer = answer['user_answer']
            correct_answers = answer['correct_answers']
            options = answer['options']
            question_id = answer.get('question_id')
            
            # 獲取題目的正確類型
            question_type = 'single'  # 默認值
            if question_id:
                try:
                    question = self.question_service.get_question(question_id)
                    if question:
                        question_type = question['type']  # 這應該是 'single' 或 'multiple'
                except:
                    # 如果獲取失敗，根據正確答案數量推斷
                    if isinstance(correct_answers, list) and len(correct_answers) > 1:
                        question_type = 'multiple'
                    else:
                        question_type = 'single'
            
            # 格式化選項
            formatted_options = options            # 格式化用戶答案文字
            if isinstance(user_answer, list):
                user_answer_text = []
                for i in user_answer:
                    try:
                        idx = int(i)  # 轉換為整數
                        if 0 <= idx < len(options):
                            user_answer_text.append(options[idx])
                    except (ValueError, TypeError):
                        continue  # 跳過無效的索引
            elif user_answer is not None and isinstance(user_answer, int) and user_answer < len(options):
                user_answer_text = options[user_answer]
            elif user_answer is not None and isinstance(user_answer, str) and user_answer.isdigit():
                # 處理字符串數字
                idx = int(user_answer)
                if idx < len(options):
                    user_answer_text = options[idx]
                else:
                    user_answer_text = "未作答"
            else:
                user_answer_text = "未作答"
              # 格式化正確答案文字
            if isinstance(correct_answers, list):
                correct_answer_text = []
                for i in correct_answers:
                    try:
                        idx = int(i)  # 轉換為整數
                        if 0 <= idx < len(options):
                            correct_answer_text.append(options[idx])
                    except (ValueError, TypeError):
                        continue  # 跳過無效的索引
                single_correct_answer = correct_answer_text[0] if correct_answer_text else "無"
            elif isinstance(correct_answers, int) and correct_answers < len(options):
                single_correct_answer = options[correct_answers]
                correct_answer_text = [single_correct_answer]
            elif isinstance(correct_answers, str) and correct_answers.isdigit():
                # 處理字符串數字
                idx = int(correct_answers)
                if idx < len(options):
                    single_correct_answer = options[idx]
                    correct_answer_text = [single_correct_answer]
                else:
                    single_correct_answer = "無"
                    correct_answer_text = []
            else:
                single_correct_answer = "無"
                correct_answer_text = []
            
            detailed_results.append({
                'question': answer['question_text'],
                'options': formatted_options,
                'user_answer': user_answer_text,
                'correct_answer': single_correct_answer,                'correct_answers': correct_answer_text,
                'is_correct': answer['is_correct'],
                'type': question_type  # 直接使用 question_type，應該是 'single' 或 'multiple'
            })
        
        return detailed_results
    
    def get_current_question(self, session_id: str, question_index: int) -> Optional[Dict[str, Any]]:
        """獲取測驗會話中的當前題目
        
        Args:
            session_id: 會話ID
            question_index: 題目索引
            
        Returns:
            Dict: 題目數據，如果找不到則返回None
        """
        try:
            # 從會話記錄中獲取題目配置和固定的題目列表
            session_data = self.session_model.execute_query(
                'SELECT quiz_config, questions_json FROM quiz_sessions WHERE session_id = ?',
                [session_id]
            )
            
            if not session_data:
                return None
                
            import json            # 首先嘗試從 questions_json 獲取固定的題目列表
            session_row = session_data[0]
            try:
                # 嘗試使用字典式訪問（sqlite3.Row 支持）
                questions_json = session_row['questions_json']
            except (KeyError, TypeError):
                questions_json = None
            if questions_json:
                try:
                    questions = json.loads(questions_json)
                    if questions and question_index < len(questions):
                        return questions[question_index]
                except (json.JSONDecodeError, TypeError):
                    pass
            
            # 如果沒有固定的題目列表，則重新生成（向後兼容）
            quiz_config = json.loads(session_data[0]['quiz_config'])
            
            # 重新獲取相同條件的題目（確保一致性）
            # 注意：這種方法不保證每次獲取的題目順序相同，應該儘量避免
            questions = self.question_service.get_random_questions(
                count=quiz_config.get('count', 10),
                filters={k: v for k, v in quiz_config.items() if v and k != 'count'}
            )
            
            if not questions or question_index >= len(questions):
                return None
                
            return questions[question_index]
            
        except Exception as e:
            print(f"Error getting current question: {e}")
            return None
