import pytest
from app import create_app, db
from app.models import User, Chat, ChatMessage
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

'''
✅ 테스트 환경 설정
- TestingConfig를 사용하여 테스트 환경에서 메모리 DB를 사용하도록 설정
'''
@pytest.fixture
def app():
    app = create_app(config_name='testing')
    app.config.update({
        "SERVER_NAME": "localhost.localdomain",  # ← URL 생성 문제 해결
        "TESTING": True,
        "WTF_CSRF_ENABLED": False  # 폼 관련 테스트 편의
    })
    with app.app_context():
        db.create_all()  # 데이터베이스 초기화
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    ''' Flask 테스트 클라이언트 생성 '''
    return app.test_client()

@pytest.fixture
def init_database(app):
    '''테스트용 초기 데이터 삽입'''

    user = User(id="testuser", pw=generate_password_hash("testpw"), nickname="cutty")
    db.session.add(user)
    db.session.commit()

    # history_service 테스트를 위한 데이터 반환
    return {"user_id": user.id}


@pytest.fixture
def history_test_data(app, init_database):
    '''history_service 테스트를 위한 채팅 및 메시지 데이터 생성'''
    user_id = init_database["user_id"]
    
    # 여러 채팅 생성 (시간 차이를 두어 순서 테스트 가능)
    chat1 = Chat(user_id=user_id, topic="건강운", created_at=datetime.now() - timedelta(hours=2))
    db.session.add(chat1)
    db.session.flush()  # chat_id를 얻기 위해 flush
    
    chat2 = Chat(user_id=user_id, topic="학업운", created_at=datetime.now() - timedelta(hours=1))
    db.session.add(chat2)
    db.session.flush()
    
    # 채팅에 메시지 추가
    msg1_1 = ChatMessage(chat_id=chat1.chat_id, msg_num=1, sender="human", message="chat1 msg1 human message")
    msg1_2 = ChatMessage(chat_id=chat1.chat_id, msg_num=2, sender="ai", message="chat1 msg2 ai message response")
    
    msg2_1 = ChatMessage(chat_id=chat2.chat_id, msg_num=1, sender="human", message="chat2 msg1 human message")
    msg2_2 = ChatMessage(chat_id=chat2.chat_id, msg_num=2, sender="ai", message="chat2 msg2 ai message response")
    
    db.session.add_all([msg1_1, msg1_2, msg2_1, msg2_2])
    db.session.commit()
    
    return {
        "user_id": user_id,
        "chat1_id": chat1.chat_id,
        "chat2_id": chat2.chat_id,
        "chat1_topic": chat1.topic,
        "chat2_topic": chat2.topic
    }

@pytest.fixture
def empty_chat(app, history_test_data):
    """메시지가 없는 빈 채팅방 생성"""
    user_id = history_test_data["user_id"]
    with app.app_context():
        empty_chat = Chat(user_id=user_id, topic="빈 채팅")
        db.session.add(empty_chat)
        db.session.commit()
        return empty_chat.chat_id