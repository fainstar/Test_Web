"""
API路由
提供RESTful API接口
"""
from flask import Blueprint, jsonify, request
from app.services import QuestionService, QuizService

api_bp = Blueprint('api', __name__)

# 初始化服務
question_service = QuestionService()
quiz_service = QuizService()

@api_bp.route('/questions', methods=['GET'])
def get_questions():
    """獲取題目列表API"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
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
        
        result = question_service.get_questions(page=page, per_page=per_page, filters=filters)
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
    """獲取單個題目API"""
    try:
        question = question_service.get_question(question_id)
        
        if question:
            return jsonify({
                'success': True,
                'data': question
            })
        else:
            return jsonify({
                'success': False,
                'error': '題目不存在'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/questions', methods=['POST'])
def add_question():
    """添加題目API"""
    try:
        question_data = request.get_json()
        
        if not question_data:
            return jsonify({
                'success': False,
                'error': '請提供題目數據'
            }), 400
        
        result = question_service.add_question(question_data)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': result['message'],
                'question_id': result['question_id']
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': result['message']
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    """刪除題目API"""
    try:
        result = question_service.delete_question(question_id)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': result['message']
            })
        else:
            return jsonify({
                'success': False,
                'error': result['message']
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/questions/random', methods=['GET'])
def get_random_questions():
    """獲取隨機題目API"""
    try:
        count = request.args.get('count', 10, type=int)
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
        
        questions = question_service.get_random_questions(count=count, filters=filters)
        
        return jsonify({
            'success': True,
            'data': questions
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/questions/import', methods=['POST'])
def import_questions():
    """批量導入題目API"""
    try:
        json_data = request.get_json()
        
        if not json_data:
            return jsonify({
                'success': False,
                'error': '請提供JSON數據'
            }), 400
        
        # 處理不同的JSON格式
        if 'questions' in json_data:
            questions = json_data['questions']
        elif isinstance(json_data, list):
            questions = json_data
        else:
            return jsonify({
                'success': False,
                'error': 'JSON格式不正確'
            }), 400
        
        result = question_service.import_questions_from_json(questions)
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/quiz/create', methods=['POST'])
def create_quiz():
    """創建測驗API"""
    try:
        quiz_config = request.get_json()
        
        if not quiz_config:
            return jsonify({
                'success': False,
                'error': '請提供測驗配置'
            }), 400
        
        result = quiz_service.create_quiz_session(quiz_config)
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': {
                    'session_id': result['session_id'],
                    'questions': result['questions'],
                    'quiz_info': result['quiz_info']
                }
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': result['message']
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/quiz/<session_id>/submit', methods=['POST'])
def submit_quiz_answer(session_id):
    """提交測驗答案API"""
    try:
        data = request.get_json()
        question_id = data.get('question_id')
        user_answer = data.get('answer')
        
        if question_id is None or user_answer is None:
            return jsonify({
                'success': False,
                'error': '請提供題目ID和答案'
            }), 400
        
        result = quiz_service.submit_answer(session_id, question_id, user_answer)
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': {
                    'is_correct': result['is_correct'],
                    'correct_answer': result['correct_answer']
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': result['message']
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/quiz/<session_id>/complete', methods=['POST'])
def complete_quiz(session_id):
    """完成測驗API"""
    try:
        data = request.get_json()
        start_time = data.get('start_time')
        
        if not start_time:
            return jsonify({
                'success': False,
                'error': '請提供開始時間'
            }), 400
        
        result = quiz_service.complete_quiz(session_id, start_time)
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': result['results']
            })
        else:
            return jsonify({
                'success': False,
                'error': result['message']
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """獲取統計信息API"""
    try:
        question_stats = question_service.get_statistics()
        quiz_stats = quiz_service.get_statistics()
        
        return jsonify({
            'success': True,
            'data': {
                'questions': question_stats,
                'quiz': quiz_stats
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
