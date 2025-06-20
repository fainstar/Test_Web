"""
測驗路由
處理測驗相關功能
"""
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from datetime import datetime
from app.services import QuizService, QuestionService

quiz_bp = Blueprint('quiz', __name__)

# 初始化服務
quiz_service = QuizService()
question_service = QuestionService()

@quiz_bp.route('/start', methods=['GET', 'POST'])
def start_quiz():
    """開始測驗"""
    if request.method == 'GET':
        # 直接開始測驗配置，如果沒有參數就重定向到首頁
        count = request.args.get('count', 10, type=int)
        difficulty = request.args.get('difficulty')
        category = request.args.get('category')
        
        try:
            # 創建測驗配置
            quiz_config = {
                'count': count,
                'difficulty': difficulty,
                'category': category
            }
            
            # 獲取隨機題目
            questions = question_service.get_random_questions(
                count=quiz_config['count'],
                filters={k: v for k, v in quiz_config.items() if v}
            )
            
            if not questions:
                flash('沒有找到符合條件的題目', 'warning')
                return redirect(url_for('main.index'))
            
            # 建立測驗會話
            session_id = quiz_service.create_session(questions, quiz_config)
            
            # 儲存到Flask session
            session['quiz_session_id'] = session_id
            session['quiz_questions'] = questions
            session['current_question'] = 0
            session['quiz_info'] = {
                'start_time': quiz_service.session_model.execute_query(
                    'SELECT created_at FROM quiz_sessions WHERE session_id = ?',
                    [session_id]
                )[0]['created_at'],
                'total_questions': len(questions),
                'config': quiz_config
            }
            
            return redirect(url_for('quiz.take_quiz'))
            
        except Exception as e:
            flash(f'建立測驗失敗: {str(e)}', 'error')
            return redirect(url_for('main.index'))
    
    elif request.method == 'POST':
        try:
            # 獲取配置
            if request.is_json:
                quiz_config = request.get_json()
            else:
                quiz_config = {
                    'count': int(request.form.get('count', 10)),
                    'category': request.form.get('category') or None,
                    'difficulty': request.form.get('difficulty') or None,
                    'question_type': request.form.get('question_type') or None,
                    'shuffle_questions': request.form.get('shuffle_questions') == 'on',
                    'shuffle_options': request.form.get('shuffle_options') == 'on'
                }
            
            # 創建測驗會話
            result = quiz_service.create_quiz_session(quiz_config)
            
            if not result['success']:
                if request.is_json:
                    return jsonify({'error': result['message']}), 400
                else:
                    flash(result['message'], 'error')
                    return redirect(url_for('quiz.start_quiz'))
            
            # 儲存會話信息到Flask session
            session['quiz_session_id'] = result['session_id']
            session['quiz_questions'] = result['questions']
            session['quiz_info'] = result['quiz_info']
            session['current_question'] = 0
            session['start_time'] = datetime.now().isoformat()
            session['user_answers'] = {}
            
            if request.is_json:
                return jsonify({'redirect_url': url_for('quiz.take_quiz')})
            else:
                return redirect(url_for('quiz.take_quiz'))
                
        except Exception as e:
            if request.is_json:
                return jsonify({'error': f'創建測驗失敗: {str(e)}'}), 500
            else:
                flash(f'創建測驗失敗: {str(e)}', 'error')
                return redirect(url_for('quiz.start_quiz'))

@quiz_bp.route('/take')
def take_quiz():
    """進行測驗"""
    # 檢查會話
    if 'quiz_session_id' not in session or 'quiz_questions' not in session:
        flash('測驗會話已過期，請重新開始', 'warning')
        return redirect(url_for('quiz.start_quiz'))
    
    questions = session['quiz_questions']
    current_index = session.get('current_question', 0)
    
    # 檢查是否已完成所有題目
    if current_index >= len(questions):
        return redirect(url_for('quiz.results'))
    
    # 獲取當前題目
    current_question = questions[current_index]
    
    return render_template('quiz.html', 
                         question=current_question,
                         question_number=current_index + 1,
                         total_questions=len(questions),
                         quiz_info=session.get('quiz_info', {}))

@quiz_bp.route('/submit_answer', methods=['POST'])
def submit_answer():
    """提交答案"""
    try:
        data = request.get_json()
        question_id = data.get('question_id')
        user_answer = data.get('answer')
        
        if 'quiz_session_id' not in session:
            return jsonify({'error': '測驗會話已過期'}), 400
        
        session_id = session['quiz_session_id']
        
        # 提交答案到服務層
        result = quiz_service.submit_answer(session_id, question_id, user_answer)
        
        if not result['success']:
            return jsonify({'error': result['message']}), 400
        
        # 儲存答案到Flask session
        if 'user_answers' not in session:
            session['user_answers'] = {}
        session['user_answers'][str(question_id)] = user_answer
        session.modified = True
        
        return jsonify({
            'success': True,
            'is_correct': result['is_correct']
        })
        
    except Exception as e:
        return jsonify({'error': f'提交答案失敗: {str(e)}'}), 500

@quiz_bp.route('/next_question', methods=['POST'])
def next_question():
    """下一題"""
    if 'current_question' not in session:
        return jsonify({'error': '測驗會話已過期'}), 400
    
    session['current_question'] = session.get('current_question', 0) + 1
    session.modified = True
    
    questions = session.get('quiz_questions', [])
    current_index = session['current_question']
    
    if current_index >= len(questions):
        # 已完成所有題目
        return jsonify({'redirect_url': url_for('quiz.results')})
    else:
        # 還有下一題
        return jsonify({'redirect_url': url_for('quiz.take_quiz')})

@quiz_bp.route('/results')
def results():
    """顯示測驗結果"""
    if 'quiz_session_id' not in session:
        flash('測驗會話已過期，請重新開始', 'warning')
        return redirect(url_for('quiz.start_quiz'))
    
    try:
        session_id = session['quiz_session_id']
        start_time = session.get('start_time')
        
        # 完成測驗並獲取結果
        result = quiz_service.complete_quiz(session_id, start_time)
        
        if not result['success']:
            flash(result['message'], 'error')
            return redirect(url_for('main.index'))
        
        # 清理session
        quiz_keys = ['quiz_session_id', 'quiz_questions', 'quiz_info', 
                    'current_question', 'start_time', 'user_answers']
        for key in quiz_keys:
            session.pop(key, None)
        
        return render_template('results.html', results=result['results'])
        
    except Exception as e:
        flash(f'獲取測驗結果失敗: {str(e)}', 'error')
        return redirect(url_for('main.index'))

@quiz_bp.route('/history')
def history():
    """測驗歷史記錄"""
    try:
        sessions = quiz_service.get_recent_sessions(limit=20)
        return render_template('quiz_history.html', sessions=sessions)
    except Exception as e:
        flash(f'載入測驗歷史失敗: {str(e)}', 'error')
        return render_template('quiz_history.html', sessions=[])

@quiz_bp.route('/session/<session_id>')
def view_session(session_id):
    """查看特定測驗會話詳情"""
    try:
        results = quiz_service.get_quiz_results(session_id)
        if not results:
            flash('測驗會話不存在', 'error')
            return redirect(url_for('quiz.history'))
        
        return render_template('session_detail.html', results=results)
    except Exception as e:
        flash(f'載入測驗詳情失敗: {str(e)}', 'error')
        return redirect(url_for('quiz.history'))
