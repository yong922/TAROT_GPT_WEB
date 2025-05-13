from app.models import db, Chat, ChatMessage
from sqlalchemy import func

def last_msg_num(chat_id):
    """
    ✅ 사용자의 마지막 msg_num를 조회하는 함수
    """
    last_msg =ChatMessage.query.filter_by(chat_id=chat_id).order_by(ChatMessage.msg_num.desc()).first()
    new_msg_num = (last_msg.msg_num + 1) if last_msg else 1
    return new_msg_num

def create_chat(user_id, topic):
    """
    ✅ Chats에 새 대화 생성 후, chat_id를 가져오는 함수
    """
    chat = Chat(user_id=user_id, topic=topic)
    db.session.add(chat)
    db.session.commit()
    chat_id = chat.chat_id
    return chat_id

def save_message(chat_id, message, role):
    """
    ✅ 메시지를 DB에 저장하는 함수
    """
    msg_num = last_msg_num(chat_id)
    print("save_message의 msg_num", msg_num)
    chat_message = ChatMessage(chat_id=chat_id, msg_num=msg_num, sender=role, message=message)
    db.session.add(chat_message)
    db.session.commit()

def get_latest_chat_id(user_id):
    """
    ✅ 가장 최근의 chat_id 조회
    """
    last_chat = Chat.query.filter_by(user_id=user_id).order_by(Chat.created_at.desc()).first()
    return last_chat.chat_id if last_chat else None
  

################### 사이드바 #####################

def get_chat_list(user_id):
    """
    ✅ 사용자의 모든 대화 목록을 가져오는 함수
    """
    subquery = (
        db.session.query(
            ChatMessage.chat_id,
            db.func.min(ChatMessage.msg_num).label("first_msg_num")
        )
        .group_by(ChatMessage.chat_id)
        .subquery()
    )

    chats = (
        db.session.query(
            Chat.chat_id,
            Chat.topic,
            ChatMessage.message
        )
        .join(subquery, Chat.chat_id == subquery.c.chat_id)
        .join(ChatMessage, (ChatMessage.chat_id == subquery.c.chat_id) & (ChatMessage.msg_num == subquery.c.first_msg_num))
        .filter(Chat.user_id == user_id)
        .order_by(Chat.created_at.desc())
        .all()
    )

    chat_list = [
        {
            "chat_id": chat.chat_id,
            "topic": chat.topic,
            "preview_message": chat.message[:15] if chat.message else ""
        }
        for chat in chats
    ]
    
    return chat_list


def get_chat_messages(chat_id):
    """ 
    ✅ 해당 chat_id의 모든 메시지를 가져오는 함수 
    """
    messages = (
        db.session.query(ChatMessage)
        .filter(ChatMessage.chat_id == chat_id)
        .order_by(ChatMessage.msg_num)
        .all()
    )
    return [{"sender": msg.sender, "message": msg.message} for msg in messages]

def delete_chat_from_db(chat_id):
    """
    ✅ 주어진 chat_id의 채팅과 해당 채팅의 모든 메시지를 삭제하는 함수
    """
    try:
        # chat_id 존재 여부 확인
        chat_exists = Chat.query.get(chat_id)
        if not chat_exists:
            return False
        
        # chat_id 기록 삭제
        chat_message_deleted = ChatMessage.query.filter_by(chat_id=chat_id).delete()
        chat_deleted = Chat.query.filter_by(chat_id=chat_id).delete()

        db.session.commit()

        # 최종적으로 삭제가 되었는지 확인
        return chat_deleted > 0 and chat_message_deleted >=0
    except Exception as e:
        db.session.rollback()
        print(f"삭제 중 오류 발생: {e}")
        return False