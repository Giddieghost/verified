from flask import Blueprint, request, jsonify, g
from backend.database.db import db
from backend.models.movie import Movie
from backend.models.review import Review
from backend.utils.auth import token_required, admin_required

movie_bp = Blueprint('movie', __name__)


from backend.services.movie_service import MovieService

@movie_bp.route('/', methods=['GET'])
def get_movies():
    category = request.args.get('category', '')
    page = request.args.get('page', 1, type=int)
    
    movies_pagination = MovieService.get_movies(category=category, page=page)
    return jsonify({
        'movies': [m.to_dict() for m in movies_pagination.items],
        'total': movies_pagination.total,
        'pages': movies_pagination.pages
    }), 200


@movie_bp.route('/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = MovieService.get_movie_by_id(movie_id)
    if not movie:
        return jsonify({'error': 'movie not found'}), 404
    return jsonify(movie.to_dict()), 200


@movie_bp.route('/', methods=['POST'])
@admin_required
def create_movie():
    data = request.get_json() or {}
    movie = MovieService.create_movie(data, g.current_user.id)
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
