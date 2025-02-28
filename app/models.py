from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.dialects.mysql import JSON

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(20), primary_key=True)  
    pw = db.Column(db.String(255), nullable=False) 
    nickname = db.Column(db.String(15), nullable=False) 
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp()) 
    
    def __init__(self, id, pw, nickname):
        self.id = id
        self.pw = pw
        self.nickname = nickname

    def __repr__(self):
        return f"<User {self.id}>"


class Chat(db.Model):
    """
    💫 대화 테이블
    - chat_id : PK, 자동 증가
    - user_id : FK, users 테이블 참조
    - topic : 대화 주제
    - created_at : 생성 시간
    """

    __tablename__ = 'chats'

    chat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(20), db.ForeignKey('users.id'), nullable=False)
    topic = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('chats', lazy=True))

    def __repr__(self):
        return f"<Chat {self.chat_id}, User {self.user_id}, Topic {self.topic}>"


class ChatMessage(db.Model):
    """
    💫 개별 메시지 테이블
    - msg_id : PK, 자동 증가
    - chat_id : FK, chats 테이블 참조
    - sender : human 또는 ai
    - message : 메시지 내용
    """
    __tablename__ = 'chat_messages'

    msg_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.chat_id'), nullable=False)
    msg_num = db.Column(db.Integer, nullable=False)
    sender = db.Column(db.String(5), nullable=False)  
    message = db.Column(db.Text, nullable=False)

    chat = db.relationship('Chat', backref=db.backref('messages', lazy=True))

    def __repr__(self):
        return f"<ChatMessage {self.msg_id}, Chat {self.chat_id}, Sender {self.sender}>"