from flask import Blueprint, request, jsonify
from backend.models.user import User
from backend.models.movie import Movie
from backend.models.series import Series
from backend.models.review import Review
from backend.database.db import db
from backend.utils.auth import admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

@admin_bp.route('/users/<int:user_id>/promote', methods=['PATCH'])
@admin_required
def promote_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    user.is_admin = True
    db.session.commit()
    return jsonify({'message': 'User promoted to admin', 'user': user.to_dict()})

@admin_bp.route('/stats', methods=['GET'])
@admin_required
def stats():
    return jsonify({
        'user_count': User.query.count(),
        'movie_count': Movie.query.count(),
        'series_count': Series.query.count(),
        'review_count': Review.query.count(),
    })
