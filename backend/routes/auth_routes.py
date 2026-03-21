from flask import Blueprint, request, jsonify
from backend.database.db import db
from backend.models.user import User
from backend.utils.security import hash_password, verify_password, generate_token
from backend.utils.validators import validate_email, validate_password

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    email = data.get('email', '').strip()
    password = data.get('password', '')
    username = data.get('username', '').strip()
    full_name = data.get('full_name', '').strip()

    if not email or not password or not username:
        return jsonify({'error': 'email, username, and password required'}), 400
    if not validate_email(email) or not validate_password(password):
        return jsonify({'error': 'invalid email or password format'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'email already exists'}), 409
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'username already exists'}), 409

    new_user = User(
        email=email,
        username=username,
        password_hash=hash_password(password),
        full_name=full_name
    )
    db.session.add(new_user)
    db.session.commit()

    token = generate_token(new_user.id)
    return jsonify({'token': token, 'user': new_user.to_dict()}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'error': 'email and password required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not verify_password(password, user.password_hash):
        return jsonify({'error': 'invalid credentials'}), 401

    token = generate_token(user.id, expires_hours=720)  # 30 days
    return jsonify({'token': token, 'user': user.to_dict()}), 200


@auth_bp.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json() or {}
    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'error': 'email and password required'}), 400

    user = User.query.filter_by(email=email, is_admin=True).first()
    if not user or not verify_password(password, user.password_hash):
        return jsonify({'error': 'invalid admin credentials'}), 401

    token = generate_token(user.id, expires_hours=720)
    return jsonify({'token': token, 'user': user.to_dict()}), 200
