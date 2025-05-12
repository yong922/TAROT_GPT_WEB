import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_current_user():
    mock_user = MagicMock()
    mock_user.id = "testuser"
    mock_user.nickname = "테스트유저"
    mock_user.get_id.return_value = "testuser"
    return mock_user

def test_login_success(client, mock_current_user):
    with patch("app.routes.auth_routes.authenticate_user", return_value={'success': True, 'user': mock_current_user}), \
         patch("flask_login.login_user"):
        response = client.post("/", data={
            'id': 'testuser',
            'pw': 'password123'
        }, follow_redirects=True)
        assert response.status_code == 200

def test_login_failure(client):
    with patch("app.routes.auth_routes.authenticate_user", return_value={'success': False, 'message': 'Invalid credentials'}):
        response = client.post("/", data={
            'id': 'wronguser',
            'pw': 'wrongpassword'
        }, follow_redirects=True)
        assert response.status_code == 200

def test_signup_success(client):
    with patch("app.routes.auth_routes.register_user", return_value={'success': True, 'message': 'Registration successful'}):
        response = client.post("/signup/", data={
            'id': 'newuser',
            'pw': 'password123',
            'nickname': 'New User'
        }, follow_redirects=True)
        assert response.status_code == 200

def test_signup_failure(client):
    with patch("app.routes.auth_routes.register_user", return_value={'success': False, 'message': 'ID already taken'}):
        response = client.post("/signup/", data={
            'id': 'takenuser',
            'pw': 'password123',
            'nickname': 'Taken User'
        }, follow_redirects=True)
        assert response.status_code == 200

def test_check_id_available(client):
    with patch("app.routes.auth_routes.id_available", return_value={'available': True}):
        response = client.post("/check_id/", json={'user_id': 'newuser'})
        data = response.get_json()
        assert response.status_code == 200
        assert data['available'] is True

def test_check_id_unavailable(client):
    with patch("app.routes.auth_routes.id_available", return_value={'available': False}):
        response = client.post("/check_id/", json={'user_id': 'takenuser'})
        data = response.get_json()
        assert response.status_code == 200
        assert data['available'] is False

def test_logout(client):
    with patch("flask_login.logout_user"):
        response = client.get("/logout/", follow_redirects=True)
        assert response.status_code == 200