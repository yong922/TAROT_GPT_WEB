from flask import current_app
from app import db
from app.models import ChatHistory

def create_chat_history(user_id, topic, memory):
    """새로운 대화 기록을 DB에 생성"""
    with current_app.app_context():  # ✅ Flask 애플리케이션 컨텍스트 가져오기
        chat = ChatHistory(
            user_id=user_id,
            topic=topic,
            message=[]
        )
        db.session.add(chat)
        db.session.commit()
        return chat.chat_id

def update_chat_history(chat_id, memory):
    """기존 대화 내용을 업데이트"""
    with current_app.app_context():  # ✅ Flask 애플리케이션 컨텍스트 가져오기
        chat = ChatHistory.query.filter_by(chat_id=chat_id).first()
        if chat:
            messages = [
                {"role": "user", "text": m.content} if m.type == "human" else
                {"role": "bot", "text": m.content}
                for m in memory.chat_memory.messages
            ]
            chat.message = messages
            db.session.commit()
