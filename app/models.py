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

class ChatHistory(db.Model):
    __tablename__ = 'chat_history'

    chat_id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    user_id = db.Column(db.String(20), db.ForeignKey('users.id'), nullable=False)  
    topic = db.Column(db.String(10), nullable=False)
    message = db.Column(JSON, nullable=False)  
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())  

    # 관계 설정
    user = db.relationship('User', backref=db.backref('chat_history', lazy=True))

    def __repr__(self):
        return f"<ChatHistory {self.chat_id}, User {self.user_id}>"