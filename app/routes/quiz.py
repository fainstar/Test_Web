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
            print(f"DEBUG: Starting quiz with count={count}, difficulty={difficulty}, category={category}")
            
            # 創建測驗配置
            quiz_config = {
                'count': count,
                'difficulty': difficulty,
                'category': category
            }
            
            # 獲取隨機題目
            print(f"DEBUG: Getting random questions with config: {quiz_config}")
            questions = question_service.get_random_questions(
                count=quiz_config['count'],
                filters={k: v for k, v in quiz_config.items() if v}
            )
            
            print(f"DEBUG: Got {len(questions) if questions else 0} questions")
            
            if not questions:
                flash('沒有找到符合條件的題目', 'warning')
                return redirect(url_for('main.index'))
              # 建立測驗會話
            print(f"DEBUG: Creating quiz session")
            session_id = quiz_service.create_session(questions, quiz_config)
            print(f"DEBUG: Created session with ID: {session_id}")
            
            # 儲存到Flask session（簡化版本）
            session.permanent = True  # 設置為永久會話
            session['quiz_session_id'] = session_id
            session['total_questions'] = len(questions)
            session['current_question'] = 0
            
            print(f"DEBUG: Session set successfully: {session_id}")
            print(f"DEBUG: Session keys after setting: {list(session.keys())}")
            
            # 暫時使用 URL 參數傳遞會話ID，避開 session 問題
            return redirect(url_for('quiz.take_quiz', session_id=session_id, question_index=0))
            
        except Exception as e:
            import traceback
            error_msg = f'建立測驗失敗: {str(e)}'
            print(f"ERROR in start_quiz: {error_msg}")
            print(f"Traceback: {traceback.format_exc()}")
            flash(error_msg, 'error')
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
            session.permanent = True  # 設置為永久會話
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
    print(f"DEBUG: take_quiz called")
    
    # 從 URL 參數獲取會話ID和問題索引
    session_id = request.args.get('session_id')
    question_index = request.args.get('question_index', 0, type=int)
    
    print(f"DEBUG: URL params - session_id: {session_id}, question_index: {question_index}")
    
    # 檢查會話
    if not session_id:
        print(f"DEBUG: No session_id in URL params, redirecting to start_quiz")
        flash('測驗會話已過期，請重新開始', 'warning')
        return redirect(url_for('quiz.start_quiz'))
    
    # 獲取會話信息
    try:
        session_data = quiz_service.session_model.execute_query(
            'SELECT total_questions FROM quiz_sessions WHERE session_id = ?',
            [session_id]
        )
        
        if not session_data:
            print(f"DEBUG: Session not found in database")
            flash('測驗會話不存在', 'error')
            return redirect(url_for('quiz.start_quiz'))
        
        total_questions = session_data[0]['total_questions']
        
        print(f"DEBUG: session_id: {session_id}")
        print(f"DEBUG: question_index: {question_index}, total questions: {total_questions}")
        
        # 檢查是否已完成所有題目
        if question_index >= total_questions:
            return redirect(url_for('quiz.results', session_id=session_id))
        
        # 從服務層獲取當前題目
        current_question = quiz_service.get_current_question(session_id, question_index)
        if not current_question:
            flash('無法獲取當前題目', 'error')
            return redirect(url_for('quiz.start_quiz'))
            
        print(f"DEBUG: Rendering quiz.html with question {question_index + 1}")
        return render_template('quiz.html', 
                             question=current_question,
                             question_number=question_index + 1,
                             total_questions=total_questions,
                             quiz_info={'session_id': session_id})
                             
    except Exception as e:
        print(f"DEBUG: Error in take_quiz: {e}")
        flash(f'獲取題目失敗: {str(e)}', 'error')
        return redirect(url_for('quiz.start_quiz'))

@quiz_bp.route('/submit_answer', methods=['POST'])
def submit_answer():
    """提交答案"""
    try:
        # 支援 JSON 和表單提交兩種方式
        if request.is_json:
            # JSON提交（AJAX）
            data = request.get_json()
            question_id = data.get('question_id')
            user_answer = data.get('answer')
            session_id = session.get('quiz_session_id')
            
            if not session_id:
                return jsonify({'error': '測驗會話已過期'}), 400
        else:
            # 表單提交
            # 從 URL 參數或表單中獲取需要的信息
            session_id = request.args.get('session_id') or request.form.get('session_id')
            question_id = request.form.get('question_id')
            question_index = request.args.get('question_index', 0, type=int)
            
            # 處理答案 - 檢查是否為多選題
            answer_list = request.form.getlist('answer')
            
            print(f"DEBUG: submit_answer - question_id: {question_id}")
            print(f"DEBUG: submit_answer - answer_list: {answer_list}")
            
            if not answer_list:
                # 沒有選擇任何答案
                user_answer = None
            elif len(answer_list) == 1:
                # 單選題或只選了一個選項的多選題
                try:
                    user_answer = int(answer_list[0])
                except ValueError:
                    user_answer = answer_list[0]
            else:
                # 多選題 - 轉換為整數列表
                try:
                    user_answer = [int(ans) for ans in answer_list]
                except ValueError:
                    user_answer = answer_list
            
            print(f"DEBUG: submit_answer - processed user_answer: {user_answer} (type: {type(user_answer)})")
            
            if not session_id:
                flash('測驗會話已過期', 'warning')
                return redirect(url_for('quiz.start_quiz'))
            
            if user_answer is None:
                flash('請選擇一個答案', 'warning')
                return redirect(url_for('quiz.take_quiz', session_id=session_id, question_index=question_index))
        
        # 提交答案到服務層
        result = quiz_service.submit_answer(session_id, question_id, user_answer)
        
        if not result['success']:
            if request.is_json:
                return jsonify({'error': result['message']}), 400
            else:
                flash(result['message'], 'error')
                return redirect(url_for('quiz.take_quiz', session_id=session_id, question_index=question_index))
        
        # 儲存答案到Flask session（如果使用session-based會話）
        if 'user_answers' not in session:
            session['user_answers'] = {}
        session['user_answers'][str(question_id)] = user_answer
        session.modified = True
        
        if request.is_json:
            # JSON回應
            return jsonify({
                'success': True,
                'is_correct': result['is_correct']
            })
        else:
            # 表單提交 - 重定向到下一題
            next_question_index = question_index + 1
            
            # 檢查是否完成所有題目
            session_data = quiz_service.session_model.execute_query(
                'SELECT total_questions FROM quiz_sessions WHERE session_id = ?',
                [session_id]
            )
            
            if session_data and next_question_index >= session_data[0]['total_questions']:
                # 完成所有題目，跳轉到結果頁
                return redirect(url_for('quiz.results', session_id=session_id))
            else:
                # 跳轉到下一題
                return redirect(url_for('quiz.take_quiz', session_id=session_id, question_index=next_question_index))
        
    except Exception as e:
        if request.is_json:
            return jsonify({'error': f'提交答案失敗: {str(e)}'}), 500
        else:
            flash(f'提交答案失敗: {str(e)}', 'error')
            return redirect(url_for('quiz.start_quiz'))

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
    # 從 URL 參數或 session 獲取 session_id
    session_id = request.args.get('session_id') or session.get('quiz_session_id')
    
    print(f"DEBUG: results route called with session_id: {session_id}")
    print(f"DEBUG: session contents: {dict(session)}")
    
    if not session_id:
        print("DEBUG: No session_id found, redirecting to start_quiz")
        flash('測驗會話已過期，請重新開始', 'warning')
        return redirect(url_for('quiz.start_quiz'))
    
    try:
        # 從多個來源嘗試獲取 start_time
        start_time = session.get('start_time')
        if not start_time:
            # 嘗試從 quiz_info 獲取
            quiz_info = session.get('quiz_info', {})
            start_time = quiz_info.get('start_time')
        
        print(f"DEBUG: start_time from session: {start_time}")
        print(f"DEBUG: quiz_info: {session.get('quiz_info', {})}")
        
        # 完成測驗並獲取結果
        result = quiz_service.complete_quiz(session_id, start_time)
        print(f"DEBUG: complete_quiz result: {result}")
        
        if not result['success']:
            print(f"DEBUG: complete_quiz failed: {result['message']}")
            flash(result['message'], 'error')
            return redirect(url_for('main.index'))
        
        # 清理session
        quiz_keys = ['quiz_session_id', 'quiz_questions', 'quiz_info', 
                    'current_question', 'start_time', 'user_answers']
        for key in quiz_keys:
            session.pop(key, None)
        
        print(f"DEBUG: Rendering results.html with results: {result['results'].keys()}")
        return render_template('results.html', results=result['results'])
        
    except Exception as e:
        print(f"DEBUG: Exception in results route: {str(e)}")
        import traceback
        traceback.print_exc()
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
