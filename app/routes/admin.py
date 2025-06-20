"""
管理員路由
處理管理功能
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
import json
from app.services import QuestionService, QuizService

admin_bp = Blueprint('admin', __name__)

# 初始化服務
question_service = QuestionService()
quiz_service = QuizService()

@admin_bp.route('/')
def index():
    """管理員首頁"""
    try:
        question_stats = question_service.get_statistics()
        quiz_stats = quiz_service.get_statistics()
        recent_sessions = quiz_service.get_recent_sessions(limit=5)
        
        return render_template('admin/index.html',
                             question_stats=question_stats,
                             quiz_stats=quiz_stats,
                             recent_sessions=recent_sessions)
    except Exception as e:
        flash(f'載入管理員首頁失敗: {str(e)}', 'error')
        # 提供預設的統計數據結構
        default_question_stats = {
            'total_questions': 0,
            'type_stats': {'single_choice': 0, 'multiple_choice': 0},
            'category_stats': {},
            'difficulty_stats': {}
        }
        default_quiz_stats = {
            'total_sessions': 0,
            'average_score': 0,
            'average_duration': 0,
            'highest_score': 0
        }
        return render_template('admin/index.html',
                             question_stats=default_question_stats,
                             quiz_stats=default_quiz_stats,
                             recent_sessions=[])

@admin_bp.route('/questions')
def questions():
    """題目管理"""
    try:
        page = request.args.get('page', 1, type=int)
        category = request.args.get('category')
        difficulty = request.args.get('difficulty')
        question_type = request.args.get('question_type')
        
        filters = {}
        if category:
            filters['category'] = category
        if difficulty:
            filters['difficulty'] = difficulty
        if question_type:
            filters['question_type'] = question_type
        
        result = question_service.get_questions(page=page, per_page=20, filters=filters)
        stats = question_service.get_statistics()
        
        return render_template('admin/questions.html',
                             questions=result['questions'],
                             pagination=result,
                             stats=stats,
                             filters=filters)
    except Exception as e:
        flash(f'載入題目列表失敗: {str(e)}', 'error')
        return render_template('admin/questions.html',
                             questions=[],
                             pagination={},
                             stats={},
                             filters={})

@admin_bp.route('/questions/add', methods=['GET', 'POST'])
def add_question():
    """添加題目"""
    if request.method == 'GET':
        return render_template('admin/add_question.html')
    
    elif request.method == 'POST':
        try:
            # 獲取表單數據
            question_data = {
                'question': request.form.get('question'),
                'type': request.form.get('type'),
                'options': request.form.getlist('options'),
                'category': request.form.get('category', '一般'),
                'difficulty': request.form.get('difficulty', '中等'),
                'explanation': request.form.get('explanation', '')
            }
            
            # 處理正確答案
            if question_data['type'] == 'single':
                question_data['correct_answer'] = int(request.form.get('correct_answer'))
            else:
                question_data['correct_answer'] = [int(x) for x in request.form.getlist('correct_answers')]
            
            # 過濾空選項
            question_data['options'] = [opt for opt in question_data['options'] if opt.strip()]
            
            # 添加題目
            result = question_service.add_question(question_data)
            
            if result['success']:
                flash('題目添加成功！', 'success')
                return redirect(url_for('admin.questions'))
            else:
                flash(result['message'], 'warning')
                return render_template('admin/add_question.html', question_data=question_data)
                
        except Exception as e:
            flash(f'添加題目失敗: {str(e)}', 'error')
            return render_template('admin/add_question.html')

@admin_bp.route('/questions/<int:question_id>/delete', methods=['POST'])
def delete_question(question_id):
    """刪除題目"""
    try:
        result = question_service.delete_question(question_id)
        
        if result['success']:
            flash('題目刪除成功！', 'success')
        else:
            flash(result['message'], 'error')
            
    except Exception as e:
        flash(f'刪除題目失敗: {str(e)}', 'error')
    
    return redirect(url_for('admin.questions'))

@admin_bp.route('/import', methods=['GET', 'POST'])
def import_questions():
    """批量導入題目"""
    if request.method == 'GET':
        return render_template('admin/import.html')
    
    elif request.method == 'POST':
        try:
            # 獲取上傳的文件或JSON數據
            if 'file' in request.files:
                file = request.files['file']
                if file.filename == '':
                    flash('請選擇文件', 'error')
                    return redirect(url_for('admin.import_questions'))
                
                # 讀取文件內容
                content = file.read().decode('utf-8')
                json_data = json.loads(content)
                
            elif request.form.get('json_data'):
                # 直接從表單獲取JSON數據
                json_data = json.loads(request.form.get('json_data'))
            else:
                flash('請提供JSON數據或上傳文件', 'error')
                return redirect(url_for('admin.import_questions'))
            
            # 處理不同的JSON格式
            if 'questions' in json_data:
                questions = json_data['questions']
            elif isinstance(json_data, list):
                questions = json_data
            else:
                flash('JSON格式不正確', 'error')
                return redirect(url_for('admin.import_questions'))
            
            # 執行導入
            result = question_service.import_questions_from_json(questions)
            
            flash(f'導入完成！成功: {result["success"]}, 跳過: {result["skipped"]}, 失敗: {result["failed"]}', 'info')
            
            if result['errors']:
                flash(f'錯誤詳情: {"; ".join(result["errors"])}', 'warning')
            
            return redirect(url_for('admin.questions'))
            
        except json.JSONDecodeError:
            flash('JSON格式錯誤', 'error')
            return redirect(url_for('admin.import_questions'))
        except Exception as e:
            flash(f'導入失敗: {str(e)}', 'error')
            return redirect(url_for('admin.import_questions'))

@admin_bp.route('/sessions')
def sessions():
    """測驗會話管理"""
    try:
        sessions = quiz_service.get_recent_sessions(limit=50)
        stats = quiz_service.get_statistics()
        
        return render_template('admin/sessions.html',
                             sessions=sessions,
                             stats=stats)
    except Exception as e:
        flash(f'載入會話列表失敗: {str(e)}', 'error')
        return render_template('admin/sessions.html',
                             sessions=[],
                             stats={})

@admin_bp.route('/statistics')
def statistics():
    """統計信息"""
    try:
        question_stats = question_service.get_statistics()
        quiz_stats = quiz_service.get_statistics()
        
        return render_template('admin/statistics.html',
                             question_stats=question_stats,
                             quiz_stats=quiz_stats)
    except Exception as e:
        flash(f'載入統計信息失敗: {str(e)}', 'error')
        return render_template('admin/statistics.html',
                             question_stats={},
                             quiz_stats={})
