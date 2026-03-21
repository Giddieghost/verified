from flask import Flask
from .config import DevelopmentConfig, ProductionConfig, TestingConfig
from .database.db import db
from .routes.auth_routes import auth_bp
from .routes.user_routes import user_bp
from .routes.admin_routes import admin_bp
from .routes.movie_routes import movie_bp
from .routes.series_routes import series_bp
from .routes.payment_routes import payment_bp
from .routes.review_routes import review_bp
from .routes.download_routes import download_bp
from .routes.analytics_routes import analytics_bp


def create_app(config_name=None):
    app = Flask(__name__, static_folder='../static', template_folder='../frontend')
    if config_name is None:
        config_name = app.config.get('FLASK_ENV', 'development')

    if config_name == 'production':
        app.config.from_object(ProductionConfig)
    elif config_name == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    db.init_app(app)

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(movie_bp, url_prefix='/api/movies')
    app.register_blueprint(series_bp, url_prefix='/api/series')
    app.register_blueprint(payment_bp, url_prefix='/api/payments')
    app.register_blueprint(review_bp, url_prefix='/api/reviews')
    app.register_blueprint(download_bp, url_prefix='/api/downloads')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')

    @app.route('/health')
    def health():
        return {'status': 'ok'}, 200

    @app.route('/api')
    def api_root():
        return {'version': '1.0', 'service': 'Get Movies Streaming API'}, 200

    return app
