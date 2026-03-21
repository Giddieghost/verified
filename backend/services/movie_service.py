from backend.models.movie import Movie
from backend.models.series import Series
from backend.database.db import db

class MovieService:
    @staticmethod
    def get_movies(category=None, page=1, per_page=12):
        query = Movie.query
        if category:
            query = query.filter_by(category=category)
        return query.paginate(page=page, per_page=per_page)

    @staticmethod
    def get_movie_by_id(movie_id):
        return Movie.query.get(movie_id)

    @staticmethod
    def get_popular_series(page=1, per_page=12):
        return Series.query.paginate(page=page, per_page=per_page)

    @staticmethod
    def get_series_by_id(series_id):
        return Series.query.get(series_id)

    @staticmethod
    def create_movie(data, admin_id):
        movie = Movie(
            title=data.get('title'),
            description=data.get('description'),
            category=data.get('category'),
            price=float(data.get('price', 10.0)),
            duration=int(data.get('duration', 0)),
            thumbnail_url=data.get('thumbnail_url'),
            trailer_url=data.get('trailer_url'),
            video_url=data.get('video_url'),
            upload_by_admin_id=admin_id
        )
        db.session.add(movie)
        db.session.commit()
        return movie
