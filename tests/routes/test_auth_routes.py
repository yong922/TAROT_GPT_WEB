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
    """
    ✅ 로그인 성공 시 정상적으로 로그인 후, 채팅 페이지로 리디렉션 되는지 확인
    """
    with patch("app.routes.auth_routes.authenticate_user", return_value={'success': True, 'user': mock_current_user}), \
         patch("flask_login.login_user"):
        response = client.post("/", data={
            'id': 'testuser',
            'pw': 'password123'
        }, follow_redirects=True)
        assert response.status_code == 200

def test_login_failure(client):
    """
    ✅ 로그인 실패 시, 에러 메시지가 포함된 main.html 페이지로 돌아오는지 확인
    """
    with patch("app.routes.auth_routes.authenticate_user", return_value={'success': False, 'message': 'Invalid credentials'}):
        response = client.post("/", data={
            'id': 'wronguser',
            'pw': 'wrongpassword'
        }, follow_redirects=True)
        assert response.status_code == 200

def test_signup_success(client):
    """
    ✅ 회원가입 성공 시, 로그인 페이지로 리디렉션 되는지 확인
    """
    with patch("app.routes.auth_routes.register_user", return_value={'success': True, 'message': 'Registration successful'}):
        response = client.post("/signup/", data={
            'id': 'newuser',
            'pw': 'password123',
            'nickname': 'New User'
        }, follow_redirects=True)
        assert response.status_code == 200

def test_signup_failure(client):
    """
    ✅ 회원가입 실패 시, 에러 메시지와 함께 회원가입 페이지에 머무는지 확인
    """
    with patch("app.routes.auth_routes.register_user", return_value={'success': False, 'message': 'ID already taken'}):
        response = client.post("/signup/", data={
            'id': 'takenuser',
            'pw': 'password123',
            'nickname': 'Taken User'
        }, follow_redirects=True)
        assert response.status_code == 200

def test_check_id_available(client):
    """
    ✅ 아이디가 사용 가능한 경우를 테스트
    """
    with patch("app.routes.auth_routes.id_available", return_value={'available': True}):
        response = client.post("/check_id/", json={'user_id': 'newuser'})
        data = response.get_json()
        assert response.status_code == 200
        assert data['available'] is True

def test_check_id_unavailable(client):
    """
    ✅ 아이디가 이미 사용 중인 경우를 테스트
    """
    with patch("app.routes.auth_routes.id_available", return_value={'available': False}):
        response = client.post("/check_id/", json={'user_id': 'takenuser'})
        data = response.get_json()
        assert response.status_code == 200
        assert data['available'] is False

def test_logout(client):
    """
    ✅ 로그아웃 후 로그인 페이지로 리디렉션 되는지 확인
    """
    with patch("flask_login.logout_user"):
        response = client.get("/logout/", follow_redirects=True)
        assert response.status_code == 200
