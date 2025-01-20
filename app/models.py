from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

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

