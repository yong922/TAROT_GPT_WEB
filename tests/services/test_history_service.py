import pytest
from app.models import db, Chat, ChatMessage, User
from app.services import history_service
from werkzeug.security import generate_password_hash


def test_last_msg_num(history_test_data):
    """💚last_msg_num 함수 테스트"""
    # 기존 채팅의 다음 메시지 번호는 3이어야 함 (이미 2개의 메시지가 있음)
    chat1_new_msg_num = history_service.last_msg_num(history_test_data["chat1_id"])
    assert chat1_new_msg_num == 3
    chat2_new_msg_num = history_service.last_msg_num(history_test_data["chat1_id"])
    assert chat2_new_msg_num == 3

def test_create_chat(init_database):
    """💚create_chat 함수 테스트"""
    # 테스트 데이터
    user_id = init_database["user_id"]
    topic = "애정운"
    
    # 함수 실행
    chat_id = history_service.create_chat(user_id, topic)
    
    # 결과 검증
    assert chat_id is not None
    
    # DB에서 직접 조회하여 확인
    chat = Chat.query.get(chat_id)
    assert chat is not None
    assert chat.chat_id == chat_id
    assert chat.user_id == user_id
    assert chat.topic == topic

def test_save_message(history_test_data):
    """💚save_message 함수 테스트"""
    chat_id = history_test_data["chat1_id"]
    message = "New test message"
    role = "human"
    
    # 함수 실행
    history_service.save_message(chat_id, message, role)
    
    # 결과 검증 - msg_num이 3인 메시지가 생성되어야 함
    chat_message = ChatMessage.query.filter_by(chat_id=chat_id, msg_num=3).first()
    assert chat_message is not None
    assert chat_message.message == message
    assert chat_message.sender == role

def test_get_latest_chat_id(history_test_data):
    """💚get_latest_chat_id 함수 테스트 - 채팅 있을 때"""
    user_id = history_test_data["user_id"]
    
    # 가장 최근 chat은 chat2_id
    latest_chat_id = history_service.get_latest_chat_id(user_id)
    assert latest_chat_id == history_test_data["chat2_id"]


def test_get_latest_chat_id_no_chat(app, init_database):
    """💚get_latest_chat_id 함수 테스트 - 채팅 없는 사용자"""
    # 새로운 사용자 생성
    new_user = User(id="testuser2", pw=generate_password_hash("testpw2"), nickname="second")
    db.session.add(new_user)
    db.session.commit()

    user_id = new_user.id
    latest_chat_id = history_service.get_latest_chat_id(user_id)
    assert latest_chat_id is None

def test_get_latest_chat_id_nonexistent_user(app):
    """💚get_latest_chat_id 함수 테스트 - 존재하지 않는 사용자"""
    user_id = "nonexistent_user"
    latest_chat_id = history_service.get_latest_chat_id(user_id)
    assert latest_chat_id is None



########### 사이드바 ############
def test_get_chat_list(history_test_data):
    """💚get_chat_list 함수 테스트"""
    user_id = history_test_data["user_id"]
    
    # 함수 실행
    chat_list = history_service.get_chat_list(user_id)
    
    # 결과 검증 (최신 채팅(chat2)이 먼저 나와야 함)
    assert len(chat_list) == 2
    assert chat_list[0]["chat_id"] == history_test_data["chat2_id"]
    assert chat_list[0]["topic"] == history_test_data["chat2_topic"]
    assert "chat2 msg1 human message"[:15] in chat_list[0]["preview_message"]
    
    assert chat_list[1]["chat_id"] == history_test_data["chat1_id"]
    assert chat_list[1]["topic"] == history_test_data["chat1_topic"]
    assert "chat1 msg1 human message"[:15] in chat_list[1]["preview_message"]

def test_get_chat_messages(history_test_data):
    """💚get_chat_messages 함수 테스트"""
    chat_id = history_test_data["chat1_id"]
    
    # 함수 실행
    messages = history_service.get_chat_messages(chat_id)
    
    # 결과 검증
    assert len(messages) == 2
    assert messages[0]["sender"] == "human"
    assert messages[0]["message"] == "chat1 msg1 human message"
    assert messages[1]["sender"] == "ai"
    assert messages[1]["message"] == "chat1 msg2 ai message response"


def test_delete_chat_from_db(history_test_data):
    """💚delete_chat_from_db 함수 테스트 - 성공 케이스"""
    chat_id = history_test_data["chat1_id"]
    
    # 함수 실행
    result = history_service.delete_chat_from_db(chat_id)
    
    # 결과 검증
    assert result is True
    
    # DB에서 직접 조회하여 삭제 확인
    chat = Chat.query.get(chat_id)
    assert chat is None
    
    messages = ChatMessage.query.filter_by(chat_id=chat_id).all()
    assert len(messages) == 0

@pytest.mark.parametrize("chat_id, expected", [
    (None, False),
    (9999, False),
])
def test_delete_chat_from_db_invalid_input(chat_id, expected, init_database):
    """💚delete_chat_from_db 함수 테스트 - 실패 케이스"""
    result = history_service.delete_chat_from_db(chat_id)
    assert result == expected