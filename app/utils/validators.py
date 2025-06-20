"""
數據驗證工具
提供數據驗證功能
"""
from typing import Dict, Any, List
import re

class QuestionValidator:
    """題目數據驗證器"""
    
    @staticmethod
    def validate_question_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        驗證題目數據
        
        Returns:
            dict: {'valid': bool, 'errors': list}
        """
        errors = []
        
        # 檢查必需字段
        required_fields = ['question', 'type', 'options', 'correct_answer']
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f'缺少必需字段: {field}')
        
        if errors:
            return {'valid': False, 'errors': errors}
        
        # 驗證題目文本
        question_text = str(data['question']).strip()
        if len(question_text) < 5:
            errors.append('題目文本太短（至少5個字符）')
        elif len(question_text) > 1000:
            errors.append('題目文本太長（最多1000個字符）')
        
        # 驗證題目類型
        if data['type'] not in ['single', 'multiple']:
            errors.append('題目類型必須是 single 或 multiple')
        
        # 驗證選項
        options = data['options']
        if not isinstance(options, list):
            errors.append('選項必須是列表格式')
        elif len(options) < 2:
            errors.append('選項至少需要2個')
        elif len(options) > 10:
            errors.append('選項最多10個')
        else:
            # 檢查選項內容
            for i, option in enumerate(options):
                option_text = str(option).strip()
                if not option_text:
                    errors.append(f'選項{i+1}不能為空')
                elif len(option_text) > 200:
                    errors.append(f'選項{i+1}太長（最多200個字符）')
        
        # 驗證正確答案
        correct_answer = data['correct_answer']
        options_count = len(options) if isinstance(options, list) else 0
        
        if data['type'] == 'single':
            # 單選題
            if not isinstance(correct_answer, int):
                errors.append('單選題的正確答案必須是整數')
            elif correct_answer < 0 or correct_answer >= options_count:
                errors.append(f'單選題的正確答案索引超出範圍（0-{options_count-1}）')
        else:
            # 多選題
            if not isinstance(correct_answer, list):
                errors.append('多選題的正確答案必須是列表')
            elif not correct_answer:
                errors.append('多選題至少需要一個正確答案')
            else:
                for answer in correct_answer:
                    if not isinstance(answer, int):
                        errors.append('多選題的正確答案必須是整數列表')
                        break
                    elif answer < 0 or answer >= options_count:
                        errors.append(f'多選題的正確答案索引超出範圍（0-{options_count-1}）')
                        break
        
        # 驗證分類
        if 'category' in data:
            category = str(data['category']).strip()
            if len(category) > 50:
                errors.append('分類名稱太長（最多50個字符）')
        
        # 驗證難度
        if 'difficulty' in data:
            valid_difficulties = ['簡單', '中等', '困難']
            if data['difficulty'] not in valid_difficulties:
                errors.append(f'難度必須是: {", ".join(valid_difficulties)}')
        
        # 驗證解釋
        if 'explanation' in data:
            explanation = str(data['explanation']).strip()
            if len(explanation) > 500:
                errors.append('解釋太長（最多500個字符）')
        
        return {'valid': len(errors) == 0, 'errors': errors}

class QuizConfigValidator:
    """測驗配置驗證器"""
    
    @staticmethod
    def validate_quiz_config(config: Dict[str, Any]) -> Dict[str, Any]:
        """
        驗證測驗配置
        
        Returns:
            dict: {'valid': bool, 'errors': list}
        """
        errors = []
        
        # 驗證題目數量
        count = config.get('count', 10)
        if not isinstance(count, int) or count < 1 or count > 100:
            errors.append('題目數量必須是1-100之間的整數')
        
        # 驗證分類
        category = config.get('category')
        if category and len(str(category)) > 50:
            errors.append('分類名稱太長（最多50個字符）')
        
        # 驗證難度
        difficulty = config.get('difficulty')
        if difficulty:
            valid_difficulties = ['簡單', '中等', '困難']
            if difficulty not in valid_difficulties:
                errors.append(f'難度必須是: {", ".join(valid_difficulties)}')
        
        # 驗證題型比例
        if 'type_ratios' in config:
            type_ratios = config['type_ratios']
            if not isinstance(type_ratios, dict):
                errors.append('題型比例必須是字典格式')
            else:
                total_ratio = sum(type_ratios.values())
                if abs(total_ratio - 1.0) > 0.01:
                    errors.append('題型比例總和必須等於1.0')
        
        return {'valid': len(errors) == 0, 'errors': errors}

def sanitize_input(text: str, max_length: int = None) -> str:
    """清理用戶輸入"""
    if not isinstance(text, str):
        text = str(text)
    
    # 移除HTML標籤
    text = re.sub(r'<[^>]+>', '', text)
    
    # 移除多餘空白
    text = re.sub(r'\s+', ' ', text).strip()
    
    # 限制長度
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text
