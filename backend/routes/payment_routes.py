from flask import Blueprint, request, jsonify, g
from datetime import datetime
from backend.database.db import db
from backend.models.payment import Payment
from backend.models.purchase import Purchase
from backend.models.movie import Movie
from backend.models.series import Series
from backend.utils.auth import token_required

payment_bp = Blueprint('payment', __name__)


from backend.services.daraja_service import DarajaService

@payment_bp.route('/initiate', methods=['POST'])
@token_required
def initiate_payment():
    data = request.get_json() or {}
    
    movie_id = data.get('movie_id')
    series_id = data.get('series_id')
    amount = float(data.get('amount', 49.0))
    phone = data.get('phone_number')

    if not phone:
        return jsonify({'error': 'phone number required'}), 400

    # Format phone to 254...
    if phone.startswith('0'):
        phone = '254' + phone[1:]
    elif phone.startswith('+'):
        phone = phone[1:]

    payment = Payment(
        user_id=g.current_user.id,
        amount=amount,
        currency='KES',
        method='mpesa',
        phone_number=phone,
        status='pending',
        description=f"Get Movies: {'Movie '+str(movie_id) if movie_id else 'Series '+str(series_id)}"
    )

    db.session.add(payment)
    db.session.commit()

    # Call Daraja STK Push
    res, status_code = DarajaService.initiate_stk_push(
        phone_number=phone,
        amount=1, # Setting to 1 KES for testing per Daraja sandbox rules if needed, or stick to amount
        account_reference=f"PAY-{payment.id}",
        transaction_desc="Payment for Get Movies Content"
    )

    if status_code == 200:
        payment.checkout_request_id = res.get('CheckoutRequestID')
        db.session.commit()
        return jsonify({
            'payment_id': payment.id,
            'checkout_request_id': payment.checkout_request_id,
            'status': 'initiated',
            'message': 'Check your phone for STK push'
        }), 201
    
    return jsonify({'error': 'M-Pesa push failed', 'details': res}), status_code


@payment_bp.route('/query/<int:payment_id>', methods=['GET'])
@token_required
def query_payment_status(payment_id):
    payment = Payment.query.get(payment_id)
    if not payment or payment.user_id != g.current_user.id:
        return jsonify({'error': 'payment not found'}), 404
    
    if not payment.checkout_request_id:
        return jsonify({'status': payment.status}), 200

    res, status_code = DarajaService.query_stk_status(payment.checkout_request_id)
    if status_code == 200:
        result_code = res.get('ResultCode')
        if result_code == '0':
            payment.status = 'completed'
            db.session.commit()
            # Note: Purchase normally handled in callback, but for UX we can check here
        elif result_code:
            payment.status = 'failed'
            db.session.commit()
        
    return jsonify({'status': payment.status, 'details': res}), 200


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
    
    # In a real app, this would be verified via M-Pesa Callback
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
