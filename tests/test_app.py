# Add the project root to the sys.path
import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_items(client):
    response = client.get('/items')
    assert response.status_code == 200
    assert response.get_json() == []

def test_create_item(client):
    response = client.post('/items', json={'id': 1, 'name': 'Test Item'})
    assert response.status_code == 201
    assert response.get_json() == {'id': 1, 'name': 'Test Item'}

def test_get_item(client):
    client.post('/items', json={'id': 1, 'name': 'Test Item'})
    response = client.get('/items/1')
    assert response.status_code == 200
    assert response.get_json() == {'id': 1, 'name': 'Test Item'}

def test_update_item(client):
    client.post('/items', json={'id': 1, 'name': 'Test Item'})
    response = client.put('/items/1', json={'name': 'Updated Item'})
    assert response.status_code == 200
    assert response.get_json() == {'id': 1, 'name': 'Updated Item'}

def test_delete_item(client):
    client.post('/items', json={'id': 1, 'name': 'Test Item'})
    response = client.delete('/items/1')
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Item deleted'}
    response = client.get('/items/1')
    assert response.status_code == 404
