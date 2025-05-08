import pytest
from app.models import User, Chat, ChatMessage
from app import db, create_app

'''
✅ 모델에 대한 테스트 코드
- User, Chat, ChatMessage 모델에 대한 CRUD 테스트 코드 작성
'''

# ☑️ User
def test_create_user(app):
    with app.app_context():
        user = User(id="testuser", pw="password", nickname="TestUser")
        db.session.add(user)
        db.session.commit()

        # 사용자 존재 여부 확인
        created_user = User.query.filter_by(id="testuser").first()
        assert created_user.id is not None
        assert created_user.nickname == "TestUser"
        assert created_user.pw == "password"

def test_user_repr(app):
    with app.app_context():
        user = User(id="testuser", pw="password", nickname="TestUser")
        db.session.add(user)
        db.session.commit()

        created_user = User.query.filter_by(id="testuser").first()
        assert repr(created_user) == "<User testuser>"

# ☑️ Chat
def test_create_chat(app):
    with app.app_context():
        user = User(id="testuser", pw="password", nickname="Test User")
        db.session.add(user)
        db.session.commit()
        
        chat = Chat(user_id=user.id, topic="General")
        db.session.add(chat)
        db.session.commit()
        
        # 채팅 존재 여부 확인
        created_chat = Chat.query.filter_by(user_id=user.id).first()
        assert created_chat is not None
        assert created_chat.topic == "General"
        assert created_chat.user_id == user.id

def test_chat_repr(app):
    with app.app_context():
        user = User(id="testuser", pw="password", nickname="Test User")
        db.session.add(user)
        db.session.commit()

        chat = Chat(user_id=user.id, topic="General")
        db.session.add(chat)
        db.session.commit()

        # __repr__ 메서드 테스트
        created_chat = Chat.query.filter_by(user_id=user.id).first()
        assert repr(created_chat) == f"<Chat {created_chat.chat_id}, User {created_chat.user_id}, Topic {created_chat.topic}>"

# ChatMessage 모델에 대한 테스트
def test_create_chat_message(app):
    with app.app_context():
        user = User(id="testuser", pw="password", nickname="Test User")
        db.session.add(user)
        db.session.commit()

        chat = Chat(user_id=user.id, topic="General")
        db.session.add(chat)
        db.session.commit()

        chat_message = ChatMessage(chat_id=chat.chat_id, msg_num=1, sender="human", message="Hello")
        db.session.add(chat_message)
        db.session.commit()

        # 메시지 존재 여부 확인
        created_message = ChatMessage.query.filter_by(chat_id=chat.chat_id).first()
        assert created_message is not None
        assert created_message.message == "Hello"
        assert created_message.sender == "human"

def test_chat_message_repr(app):
    with app.app_context():

        user = User(id="testuser", pw="password", nickname="Test User")
        db.session.add(user)
        db.session.commit()

        chat = Chat(user_id=user.id, topic="General")
        db.session.add(chat)
        db.session.commit()

        chat_message = ChatMessage(chat_id=chat.chat_id, msg_num=1, sender="human", message="Hello")
        db.session.add(chat_message)
        db.session.commit()

        # __repr__ 메서드 테스트
        created_message = ChatMessage.query.filter_by(chat_id=chat.chat_id).first()
        assert repr(created_message) == f"<ChatMessage {created_message.msg_id}, Chat {created_message.chat_id}, Sender {created_message.sender}>"