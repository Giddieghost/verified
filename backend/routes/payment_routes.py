from flask import Blueprint, request, jsonify, g
from datetime import datetime
from backend.database.db import db
from backend.models.payment import Payment
from backend.models.purchase import Purchase
from backend.models.movie import Movie
from backend.models.series import Series
from backend.utils.auth import token_required

payment_bp = Blueprint('payment', __name__)


@payment_bp.route('/initiate', methods=['POST'])
@token_required
def initiate_payment():
    data = request.get_json() or {}
    
    movie_id = data.get('movie_id')
    series_id = data.get('series_id')
    episode_ids = data.get('episode_ids', '')  # comma-separated for series
    amount = float(data.get('amount', 10.0))
    phone = data.get('phone_number')

    payment = Payment(
        user_id=g.current_user.id,
        amount=amount,
        currency='KES',
        method='mpesa',
        phone_number=phone,
        status='pending',
        description=f"Payment for movie_id={movie_id}, series_id={series_id}"
    )

    db.session.add(payment)
    db.session.commit()

    # Placeholder for M-Pesa STK Push
    # In production, call M-Pesa API
    return jsonify({
        'payment_id': payment.id,
        'status': 'initiated',
        'amount': amount,
        'phone': phone
    }), 201


@payment_bp.route('/<int:payment_id>/confirm', methods=['POST'])
@token_required
def confirm_payment(payment_id):
    payment = Payment.query.get(payment_id)
    if not payment:
        return jsonify({'error': 'payment not found'}), 404
    if payment.user_id != g.current_user.id:
        return jsonify({'error': 'unauthorized'}), 403

    data = request.get_json() or {}
    transaction_id = data.get('transaction_id')
    
    # Placeholder for M-Pesa verification
    payment.status = 'completed'
    payment.transaction_id = transaction_id
    db.session.commit()

    # Create purchase record
    purchase = Purchase(
        user_id=g.current_user.id,
        movie_id=data.get('movie_id'),
        series_id=data.get('series_id'),
        episode_ids=data.get('episode_ids', ''),
        payment_id=payment.id
    )
    purchase.set_expiry(7)  # 7-day access
    db.session.add(purchase)
    db.session.commit()

    return jsonify({'status': 'payment confirmed', 'purchase_id': purchase.id}), 200


@payment_bp.route('/history', methods=['GET'])
@token_required
def payment_history():
    payments = Payment.query.filter_by(user_id=g.current_user.id).all()
    return jsonify([p.to_dict() for p in payments]), 200


@payment_bp.route('/admin/revenue', methods=['GET'])
@token_required
def admin_revenue():
    if not g.current_user.is_admin:
        return jsonify({'error': 'admin only'}), 403
    
    payments = Payment.query.filter_by(status='completed').all()
    total_revenue = sum(p.amount for p in payments)
    
    return jsonify({'total_revenue': total_revenue, 'payment_count': len(payments)}), 200
