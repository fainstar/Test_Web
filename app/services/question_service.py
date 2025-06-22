"""
題目服務層
處理題目相關的業務邏輯
"""
import json
import random
from datetime import datetime
from typing import List, Dict, Any, Optional
from app.models import Question
from config.config import get_config

class QuestionService:
    """題目服務類"""
    
    def __init__(self):
        config = get_config()
        self.question_model = Question(config.DATABASE_PATH)
    
    def get_total_count(self) -> int:
        """獲取題目總數"""
        try:
            stats = self.question_model.get_statistics()
            return stats.get('total_questions', 0)
        except Exception as e:
            print(f"Error getting total count: {e}")
            return 0
    
    def get_current_time(self) -> str:
        """獲取當前時間"""
        return datetime.now().isoformat()
    
    def add_question(self, question_data: Dict[str, Any]) -> Dict[str, Any]:
        """添加題目"""
        # 數據驗證
        if not self._validate_question_data(question_data):
            return {'success': False, 'message': '題目數據格式不正確'}
        
        # 標準化數據
        normalized_data = self._normalize_question_data(question_data)
        
        # 添加到數據庫
        question_id, is_new = self.question_model.add(normalized_data)
        
        if is_new:
            return {'success': True, 'message': '題目添加成功', 'question_id': question_id}
        else:
            return {'success': False, 'message': '題目已存在', 'question_id': question_id}
    
    def get_question(self, question_id: int) -> Optional[Dict[str, Any]]:
        """獲取單個題目"""
        return self.question_model.get_by_id(question_id)
    
    def get_questions(self, page: int = 1, per_page: int = 20, 
                     filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """獲取題目列表"""
        filters = filters or {}
        
        return self.question_model.get_all(
            page=page,
            per_page=per_page,
            category=filters.get('category'),
            difficulty=filters.get('difficulty'),
            question_type=filters.get('question_type')
        )
    
    def get_random_questions(self, count: int = 10, 
                           filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """獲取隨機題目"""
        filters = filters or {}
        
        return self.question_model.get_random(
            count=count,
            category=filters.get('category'),
            difficulty=filters.get('difficulty'),
            question_type=filters.get('question_type')
        )
    
    def get_advanced_random_questions(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """進階隨機題目獲取"""
        questions = []
        
        # 如果指定了題型比例
        if 'type_ratios' in config:
            type_ratios = config['type_ratios']
            total_count = config.get('count', 10)
            
            for question_type, ratio in type_ratios.items():
                type_count = int(total_count * ratio)
                if type_count > 0:
                    type_questions = self.question_model.get_random(
                        count=type_count,
                        category=config.get('category'),
                        difficulty=config.get('difficulty'),
                        question_type=question_type
                    )
                    questions.extend(type_questions)
        else:
            # 普通隨機獲取
            questions = self.get_random_questions(
                count=config.get('count', 10),
                filters=config
            )
        
        # 如果啟用選項亂序
        if config.get('shuffle_options', False):
            questions = self._shuffle_question_options(questions)
        
        # 打亂題目順序
        if config.get('shuffle_questions', True):
            random.shuffle(questions)
        
        return questions[:config.get('count', 10)]  # 確保不超過要求數量
    
    def delete_question(self, question_id: int) -> Dict[str, Any]:
        """刪除題目"""
        success = self.question_model.delete(question_id)
        
        if success:
            return {'success': True, 'message': '題目刪除成功'}
        else:
            return {'success': False, 'message': '題目不存在或刪除失敗'}
    
    def import_questions_from_json(self, json_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """從JSON數據批量導入題目"""
        results = {
            'success': 0,
            'skipped': 0,
            'failed': 0,
            'errors': []
        }
        
        for i, question_data in enumerate(json_data):
            try:
                result = self.add_question(question_data)
                if result['success']:
                    results['success'] += 1
                else:
                    results['skipped'] += 1
            except Exception as e:
                results['failed'] += 1
                results['errors'].append(f'第{i+1}題: {str(e)}')
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """獲取題目統計信息"""
        return self.question_model.get_statistics()
    
    def _validate_question_data(self, data: Dict[str, Any]) -> bool:
        """驗證題目數據格式"""
        required_fields = ['question', 'type', 'options', 'correct_answer']
        
        # 檢查必需字段
        for field in required_fields:
            if field not in data:
                return False
        
        # 檢查題目類型
        if data['type'] not in ['single', 'multiple']:
            return False
        
        # 檢查選項
        if not isinstance(data['options'], list) or len(data['options']) < 2:
            return False
        
        # 檢查正確答案
        correct_answer = data['correct_answer']
        if isinstance(correct_answer, int):
            if correct_answer < 0 or correct_answer >= len(data['options']):
                return False
        elif isinstance(correct_answer, list):
            for answer in correct_answer:
                if not isinstance(answer, int) or answer < 0 or answer >= len(data['options']):
                    return False
        else:
            return False
        
        return True
    
    def _normalize_question_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """標準化題目數據"""
        # 確定題目類型
        question_type = 'single_choice' if data['type'] == 'single' else 'multiple_choice'
        
        # 處理正確答案
        correct_answer = data['correct_answer']
        if isinstance(correct_answer, int):
            correct_answers = [correct_answer]
            correct_answer_single = str(correct_answer)
        else:
            correct_answers = correct_answer
            correct_answer_single = None
        
        return {
            'question_text': data['question'].strip(),
            'question_type': question_type,
            'options': [opt.strip() for opt in data['options']],
            'correct_answer': correct_answer_single,
            'correct_answers': correct_answers,
            'category': data.get('category', '一般'),
            'difficulty': data.get('difficulty', '中等'),
            'explanation': data.get('explanation', '')
        }
    
    def _shuffle_question_options(self, questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """打亂題目選項順序"""
        shuffled_questions = []
        
        for question in questions:
            shuffled_question = question.copy()
            
            # 創建選項索引映射
            original_options = question['options']
            original_answers = question['correct_answer']
            
            # 創建新的順序
            indices = list(range(len(original_options)))
            random.shuffle(indices)
            
            # 重新排列選項
            new_options = [original_options[i] for i in indices]
            
            # 更新正確答案索引
            new_answers = []
            for ans in original_answers:
                new_index = indices.index(ans)
                new_answers.append(new_index)
            
            shuffled_question['options'] = new_options
            shuffled_question['correct_answer'] = new_answers
            
            shuffled_questions.append(shuffled_question)
        
        return shuffled_questions
    
    def normalize_question_format(self, question_data: Dict[str, Any]) -> Dict[str, Any]:
        """標準化不同格式的題目數據"""
        # 基本字段映射
        normalized = {
            'question': question_data.get('question', ''),
            'options': question_data.get('options', []),
            'category': question_data.get('category', '一般'),
            'difficulty': question_data.get('difficulty', '中等'),
            'explanation': question_data.get('explanation', '')
        }
        
        # 處理題目類型
        question_type = question_data.get('type', question_data.get('question_type', 'single'))
        if question_type in ['single_choice', 'single']:
            normalized['type'] = 'single'
        elif question_type in ['multiple_choice', 'multiple']:
            normalized['type'] = 'multiple'
        else:
            normalized['type'] = 'single'  # 默認為單選
        
        # 處理正確答案
        correct_answer = question_data.get('correct_answer')
        
        if isinstance(correct_answer, str):
            # 如果正確答案是文字，需要找到對應的索引
            try:
                answer_index = normalized['options'].index(correct_answer)
                normalized['correct_answer'] = [answer_index] if normalized['type'] == 'multiple' else answer_index
            except ValueError:
                # 如果找不到匹配的選項，設為第一個選項
                normalized['correct_answer'] = [0] if normalized['type'] == 'multiple' else 0
        
        elif isinstance(correct_answer, list):
            # 如果是列表
            answer_indices = []
            for ans in correct_answer:
                if isinstance(ans, str):
                    try:
                        answer_indices.append(normalized['options'].index(ans))
                    except ValueError:
                        continue
                elif isinstance(ans, int):
                    answer_indices.append(ans)
            
            if normalized['type'] == 'multiple':
                normalized['correct_answer'] = answer_indices
            else:
                normalized['correct_answer'] = answer_indices[0] if answer_indices else 0
        
        elif isinstance(correct_answer, int):
            # 如果已經是索引
            normalized['correct_answer'] = [correct_answer] if normalized['type'] == 'multiple' else correct_answer
        
        else:
            # 默認設置
            normalized['correct_answer'] = [0] if normalized['type'] == 'multiple' else 0
        
        return normalized
