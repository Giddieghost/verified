from flask import Blueprint, jsonify, g
from datetime import datetime, timedelta
from backend.database.db import db
from backend.models.user import User
from backend.models.payment import Payment
from backend.models.download import Download
from backend.utils.auth import admin_required

analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/overview', methods=['GET'])
@admin_required
def overview():
    total_users = User.query.filter_by(is_admin=False).count()
    active_users = User.query.filter_by(is_admin=False).count()  # Placeholder
    total_revenue = sum(p.amount for p in Payment.query.filter_by(status='completed').all() or [])
    total_downloads = Download.query.count()

    return jsonify({
        'total_users': total_users,
        'active_users': active_users,
        'total_revenue': total_revenue,
        'total_downloads': total_downloads
    }), 200


@analytics_bp.route('/revenue/7days', methods=['GET'])
@admin_required
def revenue_7days():
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    payments = Payment.query.filter(
        Payment.status == 'completed',
        Payment.updated_at >= seven_days_ago
    ).all()
    
    revenue_by_day = {}
    for p in payments:
        day = p.updated_at.date().isoformat()
        revenue_by_day[day] = revenue_by_day.get(day, 0) + p.amount

    return jsonify(revenue_by_day), 200


@analytics_bp.route('/revenue/monthly', methods=['GET'])
@admin_required
def revenue_monthly():
    # Placeholder for monthly revenue
    return jsonify({'revenue': 0}), 200


@analytics_bp.route('/users/registrations', methods=['GET'])
@admin_required
def user_registrations():
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    registrations = User.query.filter(User.created_at >= seven_days_ago).all()
    
    reg_by_day = {}
    for u in registrations:
        day = u.created_at.date().isoformat()
        reg_by_day[day] = reg_by_day.get(day, 0) + 1

    return jsonify(reg_by_day), 200
