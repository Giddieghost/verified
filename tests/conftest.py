import pytest
import os
from backend.app import create_app
from backend.database.db import db

@pytest.fixture
def app():
    # Ensure database directory exists for tests
    os.makedirs(os.path.join(os.path.dirname(__file__), '../database'), exist_ok=True)
    
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
