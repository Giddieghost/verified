from flask import Blueprint, jsonify, g
from backend.models.download import Download
from backend.models.purchase import Purchase
from backend.utils.auth import token_required

download_bp = Blueprint('download', __name__)


@download_bp.route('/history', methods=['GET'])
@token_required
def download_history():
    downloads = Download.query.filter_by(user_id=g.current_user.id).all()
    return jsonify([d.to_dict() for d in downloads]), 200


@download_bp.route('/purchased', methods=['GET'])
@token_required
def get_purchased_content():
    purchases = Purchase.query.filter_by(user_id=g.current_user.id).all()
    result = []
    for p in purchases:
        if not p.is_expired():
            result.append(p.to_dict())
    return jsonify(result), 200
