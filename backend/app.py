from flask import Flask, jsonify
from dotenv import load_dotenv
import os

# Load environment variables early
load_dotenv()

# Config
from backend.config import DevelopmentConfig, ProductionConfig, TestingConfig

# Extensions
from backend.database.db import db
from flask_migrate import Migrate
from flask_cors import CORS

# Blueprints
from backend.routes.auth_routes import auth_bp
from backend.routes.user_routes import user_bp
from backend.routes.admin_routes import admin_bp
from backend.routes.movie_routes import movie_bp
from backend.routes.series_routes import series_bp
from backend.routes.payment_routes import payment_bp
from backend.routes.review_routes import review_bp
from backend.routes.download_routes import download_bp
from backend.routes.analytics_routes import analytics_bp


migrate = Migrate()


def create_app(config_name=None):
    app = Flask(
        __name__,
        static_folder='../static',
        template_folder='../frontend'
    )

    # 🔐 Get environment config properly
    config_name = config_name or os.getenv("FLASK_ENV", "development")

    if config_name == "production":
        app.config.from_object(ProductionConfig)
    elif config_name == "testing":
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # 🔐 Security checks
    if not app.config.get("SECRET_KEY"):
        raise ValueError("SECRET_KEY is not set in environment")

    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise ValueError("DATABASE_URL is not set")

    # 🔌 Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)  # Allow frontend access

    # 📦 Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(movie_bp, url_prefix='/api/movies')
    app.register_blueprint(series_bp, url_prefix='/api/series')
    app.register_blueprint(payment_bp, url_prefix='/api/payments')
    app.register_blueprint(review_bp, url_prefix='/api/reviews')
    app.register_blueprint(download_bp, url_prefix='/api/downloads')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')

    # ❤️ Health check
    @app.route('/health')
    def health():
        return jsonify({'status': 'ok'}), 200

    # 📡 API root
    @app.route('/api')
    def api_root():
        return jsonify({
            'version': '1.0',
            'service': 'Get Movies Streaming API'
        }), 200

    # ❌ Global error handler (VERY IMPORTANT)
    @app.errorhandler(Exception)
    def handle_exception(e):
        return jsonify({
            "error": str(e)
        }), 500

    return app
