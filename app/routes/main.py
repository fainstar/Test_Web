"""
主要路由
處理首頁和基本功能
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services import QuestionService, QuizService

main_bp = Blueprint('main', __name__)

# 初始化服務
question_service = QuestionService()
quiz_service = QuizService()

@main_bp.route('/')
def index():
    """首頁"""
    try:
        # 獲取統計信息
        question_stats = question_service.get_statistics()
        quiz_stats = quiz_service.get_statistics()
        
        # 轉換數據格式以配合模板
        total_questions = question_stats.get('total_questions', 0)
        type_stats = question_stats.get('type_stats', {})
        single_choice = type_stats.get('single_choice', 0)
        multiple_choice = type_stats.get('multiple_choice', 0)
        
        return render_template('index.html', 
                             quiz_title='機器學習與AI服務測驗',
                             quiz_description='歡迎參加線上測驗系統，測試您對機器學習和AI服務的理解程度',
                             total_questions=total_questions,
                             single_choice=single_choice,
                             multiple_choice=multiple_choice,
                             question_stats=question_stats,
                             quiz_stats=quiz_stats)
    except Exception as e:
        flash(f'載入首頁失敗: {str(e)}', 'error')
        return render_template('index.html', 
                             quiz_title='機器學習與AI服務測驗',
                             quiz_description='歡迎參加線上測驗系統',
                             total_questions=0,
                             single_choice=0,
                             multiple_choice=0,
                             question_stats={},
                             quiz_stats={})

@main_bp.route('/about')
def about():
    """關於頁面"""
    return render_template('about.html')

@main_bp.route('/help')
def help():
    """幫助頁面"""
    return render_template('help.html')
