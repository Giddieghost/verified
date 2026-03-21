from flask import Blueprint, request, jsonify, g
from backend.database.db import db
from backend.models.movie import Movie
from backend.models.review import Review
from backend.utils.auth import token_required, admin_required

movie_bp = Blueprint('movie', __name__)


@movie_bp.route('/', methods=['GET'])
def get_movies():
    category = request.args.get('category', '')
    page = request.args.get('page', 1, type=int)
    per_page = 12

    query = Movie.query
    if category:
        query = query.filter_by(category=category)

    movies = query.paginate(page=page, per_page=per_page)
    return jsonify({
        'movies': [m.to_dict() for m in movies.items],
        'total': movies.total,
        'pages': movies.pages
    }), 200


@movie_bp.route('/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({'error': 'movie not found'}), 404
    return jsonify(movie.to_dict()), 200


@movie_bp.route('/', methods=['POST'])
@admin_required
def create_movie():
    data = request.get_json() or {}
    
    movie = Movie(
        title=data.get('title'),
        description=data.get('description'),
        category=data.get('category'),
        price=float(data.get('price', 10.0)),
        duration=int(data.get('duration', 0)),
        thumbnail_url=data.get('thumbnail_url'),
        trailer_url=data.get('trailer_url'),
        video_url=data.get('video_url'),
        upload_by_admin_id=g.current_user.id
    )
    
    db.session.add(movie)
    db.session.commit()
    return jsonify(movie.to_dict()), 201


@movie_bp.route('/<int:movie_id>', methods=['PUT'])
@admin_required
def update_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({'error': 'movie not found'}), 404

    data = request.get_json() or {}
    if 'title' in data:
        movie.title = data['title']
    if 'description' in data:
        movie.description = data['description']
    if 'price' in data:
        movie.price = float(data['price'])
    if 'thumbnail_url' in data:
        movie.thumbnail_url = data['thumbnail_url']

    db.session.commit()
    return jsonify(movie.to_dict()), 200


@movie_bp.route('/<int:movie_id>/reviews', methods=['GET'])
def get_movie_reviews(movie_id):
    reviews = Review.query.filter_by(movie_id=movie_id).all()
    return jsonify([r.to_dict() for r in reviews]), 200


@movie_bp.route('/<int:movie_id>/reviews', methods=['POST'])
@token_required
def add_review(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({'error': 'movie not found'}), 404

    data = request.get_json() or {}
    review = Review(
        user_id=g.current_user.id,
        movie_id=movie_id,
        rating=int(data.get('rating', 5)),
        comment=data.get('comment', '')
    )
    
    db.session.add(review)
    db.session.commit()
    return jsonify(review.to_dict()), 201
