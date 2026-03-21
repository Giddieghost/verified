import pytest

def test_health_check(client):
    res = client.get('/health')
    assert res.status_code == 200
    assert res.json['status'] == 'ok'

def test_api_root(client):
    res = client.get('/api')
    assert res.status_code == 200
    assert 'Get Movies' in res.json['service']
