"""
服務層初始化文件
導出所有服務類和服務管理器
"""
from .question_service import QuestionService
from .quiz_service import QuizService

class ServiceManager:
    """服務管理器類"""
    
    def __init__(self):
        self._question_service = None
        self._quiz_service = None
    
    @property
    def question_service(self):
        """獲取題目服務實例"""
        if self._question_service is None:
            self._question_service = QuestionService()
        return self._question_service
    
    @property
    def quiz_service(self):
        """獲取測驗服務實例"""
        if self._quiz_service is None:
            self._quiz_service = QuizService()
        return self._quiz_service

# 全局服務管理器實例
services = ServiceManager()

__all__ = ['QuestionService', 'QuizService', 'services']
