from flask import Blueprint, request, jsonify, g
from backend.database.db import db
from backend.models.series import Series
from backend.models.episode import Episode
from backend.models.review import Review
from backend.utils.auth import token_required, admin_required

series_bp = Blueprint('series', __name__)


@series_bp.route('/', methods=['GET'])
def get_series():
    category = request.args.get('category', '')
    page = request.args.get('page', 1, type=int)
    per_page = 12

    query = Series.query
    if category:
        query = query.filter_by(category=category)

    series_list = query.paginate(page=page, per_page=per_page)
    return jsonify({
        'series': [s.to_dict() for s in series_list.items],
        'total': series_list.total,
        'pages': series_list.pages
    }), 200


@series_bp.route('/', methods=['POST'])
@admin_required
def create_series():
    data = request.get_json() or {}
    
    series = Series(
        title=data.get('title'),
        description=data.get('description'),
        category=data.get('category'),
        price=float(data.get('price', 10.0)),
        thumbnail_url=data.get('thumbnail_url'),
        upload_by_admin_id=g.current_user.id
    )
    
    db.session.add(series)
    db.session.commit()
    return jsonify(series.to_dict()), 201


@series_bp.route('/<int:series_id>/episodes', methods=['GET'])
def get_episodes(series_id):
    episodes = Episode.query.filter_by(series_id=series_id).order_by(Episode.episode_number).all()
    if not episodes:
        return jsonify({'error': 'series not found'}), 404
    return jsonify([e.to_dict() for e in episodes]), 200


@series_bp.route('/<int:series_id>/episodes', methods=['POST'])
@admin_required
def add_episode(series_id):
    series = Series.query.get(series_id)
    if not series:
        return jsonify({'error': 'series not found'}), 404

    data = request.get_json() or {}
    episode = Episode(
        series_id=series_id,
        episode_number=int(data.get('episode_number')),
        title=data.get('title'),
        description=data.get('description'),
        duration=int(data.get('duration', 0)),
        video_url=data.get('video_url'),
        thumbnail_url=data.get('thumbnail_url')
    )
    
    db.session.add(episode)
    db.session.commit()
    return jsonify(episode.to_dict()), 201


@series_bp.route('/<int:series_id>/reviews', methods=['GET'])
def get_series_reviews(series_id):
    reviews = Review.query.filter_by(series_id=series_id).all()
    return jsonify([r.to_dict() for r in reviews]), 200


@series_bp.route('/<int:series_id>/reviews', methods=['POST'])
@token_required
def add_series_review(series_id):
    series = Series.query.get(series_id)
    if not series:
        return jsonify({'error': 'series not found'}), 404

    data = request.get_json() or {}
    review = Review(
        user_id=g.current_user.id,
        series_id=series_id,
        rating=int(data.get('rating', 5)),
        comment=data.get('comment', '')
    )
    
    db.session.add(review)
    db.session.commit()
    return jsonify(review.to_dict()), 201
