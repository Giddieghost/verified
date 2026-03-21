from functools import wraps
from flask import request, jsonify
from backend.utils.security import decode_token
from backend.models.user import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid token'}), 401
        token = auth_header.split(' ')[1]
        data = decode_token(token)
        if not data:
            return jsonify({'error': 'Invalid or expired token'}), 401
        user = User.query.get(data.get('user_id'))
        if not user:
            return jsonify({'error': 'User not found'}), 404
        request.user = user
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid token'}), 401
        token = auth_header.split(' ')[1]
        data = decode_token(token)
        if not data:
            return jsonify({'error': 'Invalid or expired token'}), 401
        user = User.query.get(data.get('user_id'))
        if not user or not user.is_admin:
            return jsonify({'error': 'Admin privileges required'}), 403
        request.user = user
        return f(*args, **kwargs)
    return decorated
