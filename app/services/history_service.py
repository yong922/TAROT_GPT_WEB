from app.models import db, Chat, ChatMessage

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
    chat_message = ChatMessage(chat_id=chat_id, msg_num=msg_num, sender=role, message=message)
    db.session.add(chat_message)
    db.session.commit()

def get_latest_chat_id(user_id):
    """
    ✅ 가장 최근의 chat_id 조회
    """
    last_chat = Chat.query.filter_by(user_id=user_id).order_by(Chat.created_at.desc()).first()
    return last_chat.chat_id if last_chat else None


def get_chat_list(user_id):
    """
    ✅ chat list 조회
    """
    chats = Chat.query.filter_by(user_id=user_id)
    return chats

def get_chat_messages(user_id, chat_id):
    """
    ✅ 특정 user_id의 특정 chat_id에 해당하는 첫 번째 메시지의 15글자만 가져오기
    """
    # chat = check_user_chat(user_id, chat_id)
    # if not chat:
        # return None  # 해당 유저의 채팅이 아닐 경우

    messages = ChatMessage.query.filter_by(chat_id=chat_id).order_by(ChatMessage.msg_num).all()

    # 첫 번째 메시지 가져오기 (없으면 빈 문자열 반환)
    first_message = messages[0].message if messages else ""

    # 첫 번째 메시지의 처음 15글자만 가져오기
    preview_message = first_message[:15]

    return preview_message
