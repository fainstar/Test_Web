"""
錯誤處理器
統一處理應用程式錯誤
"""
from flask import render_template, jsonify, request

def register_error_handlers(app):
    """註冊錯誤處理器"""
    
    @app.errorhandler(404)
    def not_found(error):
        if request.is_json:
            return jsonify({
                'success': False,
                'error': '頁面不存在',
                'error_code': 404
            }), 404
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        if request.is_json:
            return jsonify({
                'success': False,
                'error': '伺服器內部錯誤',
                'error_code': 500
            }), 500
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden(error):
        if request.is_json:
            return jsonify({
                'success': False,
                'error': '沒有權限訪問',
                'error_code': 403
            }), 403
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(400)
    def bad_request(error):
        if request.is_json:
            return jsonify({
                'success': False,
                'error': '請求格式錯誤',
                'error_code': 400
            }), 400
        return render_template('errors/400.html'), 400
