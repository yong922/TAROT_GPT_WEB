import pytest
from app.services import user_service

# DB id 조회 함수 확인
test_case_id_check = [
    ("testuser", True),
    ("testuser ", False),
    ("helloword", False),
    ("", False),
]
@pytest.mark.parametrize("user_id, expected", test_case_id_check)
def test_check_user_exists(user_id, expected, init_database):
    user = user_service.check_user_exists(user_id)
    assert (user is not None) == expected

    if expected:
        assert user.id == user_id

@pytest.mark.parametrize("user_id, expected", test_case_id_check)
def test_id_available(user_id, expected, init_database):
    result = user_service.id_available(user_id)
    assert result["success"] == (not expected)


# DB 유저 id, pw 조회 함수 확인
@pytest.mark.parametrize("user_id, password, expected",[
    ("testuser", "testpw", True),
    ("testuser ", "worngpw", False),
    ("helloword", "testpw", False),
    ("", "", False),
])
def test_authenticate_user(user_id, password, expected, init_database):
    result = user_service.authenticate_user(user_id, password)
    assert result["success"] == expected


# DB 유저 id, pw, nickname 등록 함수 확인
@pytest.mark.parametrize("user_id, password, nickname, expected", [
    ("testuser", "testpw", "cutty", False),
    ("helloword", "testpw", "meow", True),
])
def test_register_user(user_id, password, nickname, expected, init_database):
    result = user_service.register_user(user_id, password, nickname)
    assert result["success"] == expected