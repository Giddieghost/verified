from flask import Blueprint, jsonify, g, request
from backend.database.db import db
from backend.models.user import User
from backend.utils.auth import token_required
from backend.utils.security import hash_password, verify_password

user_bp = Blueprint('user', __name__)


@user_bp.route('/profile', methods=['GET'])
@token_required
def get_profile():
    user = g.current_user
    return jsonify(user.to_dict()), 200


@user_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile():
    user = g.current_user
    data = request.get_json() or {}

    if 'full_name' in data:
        user.full_name = data['full_name']
    if 'theme' in data:
        user.theme = data['theme']  # dark or light

    db.session.commit()
    return jsonify(user.to_dict()), 200


@user_bp.route('/profile/picture', methods=['POST'])
@token_required
def upload_profile_picture():
    user = g.current_user
    if 'file' not in request.files:
        return jsonify({'error': 'no file provided'}), 400
    
    file = request.files['file']
    # Placeholder for actual file upload handling
    # In production, upload to S3/external storage
    user.profile_picture = f'/uploads/profiles/{user.id}_{file.filename}'
    db.session.commit()
    return jsonify({'url': user.profile_picture}), 200


@user_bp.route('/change-password', methods=['POST'])
@token_required
def change_password():
    user = g.current_user
    data = request.get_json() or {}
    
    old_password = data.get('old_password', '')
    new_password = data.get('new_password', '')

    if not verify_password(old_password, user.password_hash):
        return jsonify({'error': 'current password incorrect'}), 401

    user.password_hash = hash_password(new_password)
    db.session.commit()
    return jsonify({'message': 'password changed'}), 200


@user_bp.route('/list', methods=['GET'])
def list_users():
    users = User.query.filter_by(is_admin=False).limit(50).all()
    return jsonify([u.to_dict() for u in users]), 200
