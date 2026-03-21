import pytest
from backend.app import create_app
from backend.database.db import db

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_health_check(client):
    res = client.get('/health')
    assert res.status_code == 200
    assert res.json['status'] == 'ok'

def test_api_root(client):
    res = client.get('/api')
    assert res.status_code == 200
    assert 'Get Movies' in res.json['service']
