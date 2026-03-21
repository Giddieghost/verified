from flask import Blueprint, jsonify, g
from backend.models.review import Review
from backend.utils.auth import token_required

review_bp = Blueprint('review', __name__)


@review_bp.route('/user-reviews', methods=['GET'])
@token_required
def get_user_reviews():
    reviews = Review.query.filter_by(user_id=g.current_user.id).all()
    return jsonify([r.to_dict() for r in reviews]), 200
