from flask import render_template, jsonify, Response, request
from flask_login import login_required, current_user
from app.services.tarot_service import TarotReader
from app.services.history_service import create_chat, save_message, get_latest_chat_id, get_chat_list, get_chat_messages
from . import chat_bp

tarot_reader = TarotReader()


@chat_bp.route("/topic_update", methods=["POST"])
def topic_update():
    """ ✅ 토픽을 업데이트하는 API """
    data = request.get_json()
    topic = data.get("topic")

    if not topic:
        return jsonify({"error": "토픽이 없습니다."}), 400
    
    # 토픽 업데이트
    updated_topic = tarot_reader.topic_update(topic)

    return jsonify({"message": "토픽 업데이트 성공", "topic": updated_topic}), 200


@chat_bp.route("/draw_tarot", methods=["POST"])
def draw_tarot():
    """ ✅ 타로 카드를 랜덤으로 뽑고 이미지 URL을 반환하는 API """
    # 카드 3장 랜덤으로 뽑기 (conversation_state["cards"] 업데이트)
    drawn_cards = tarot_reader.draw_tarot_cards()
    # 이미지 URL 가져오기
    card_images_url = tarot_reader.card_images_url(drawn_cards)

    # 카드를 응답으로 반환
    return jsonify({ "cards": drawn_cards, "card_images_url": card_images_url })


@chat_bp.route("/stream", methods=["POST"])
def chat():
    """
    ✔ Chunk 단위로 응답을 스트리밍하는 API
    """
    data = request.json
    user_id = current_user.id
    user_message = data.get("message", "").strip()
    topic = data.get("topic","").strip()
    chat_id = data.get("chat_id")

    if not user_message:
        return Response("No message received", status=400)

    if not chat_id :
        chat_id = create_chat(user_id, topic)

    save_message(chat_id, user_message, "human")

    return Response(
        tarot_reader.process_query(user_message, user_id),
        content_type="text/plain"
    )


@chat_bp.route("/get_latest_chat_id", methods=["GET"])
def get_latest_chat():
    """
    ✅ 사용자의 가장 최근 `chat_id` 반환
    """
    user_id = current_user.id
    chat_id = get_latest_chat_id(user_id)

    if chat_id:
        return jsonify({"chat_id": chat_id})
    return jsonify({"error": "No active chat found"}), 400


@chat_bp.route("/save_bot_response", methods=["POST"])
def save_bot_response():
    """
    ✅ TarotReader의 memory에서 마지막 메시지를 확인하여 DB 저장
    """
    data = request.json
    chat_id = data.get("chat_id")

    chat_history = tarot_reader.memory.chat_memory.messages  

    if not chat_history:
        return {"status": "empty", "message": "No chat history found."}

    last_message = chat_history[-1].content # string

    save_message(chat_id, last_message, "ai")

    return jsonify({"status": "success", "message": "Bot response saved."})


@chat_bp.route("/", methods=['GET'])
@login_required
def tarot_chat():
    """채팅 기록을 가져오는 API"""
    chat_icon_list = [
        {'topic': '애정운', 'icon': 'fa-heart'},
        {'topic': '재물운', 'icon': 'fa-coins'},
        {'topic': '학업운', 'icon': 'fa-briefcase'},
        {'topic': '건강운', 'icon': 'fa-medkit'},
        {'topic': '미래운', 'icon': 'fa-crystal-ball'},
    ]

    user_id = current_user.id
    chat_list = []

    if user_id:
        # DB에서 사용자별 채팅 기록 가져오기
        chats = get_chat_list(user_id)
        chat_list = [
        {
            "chat_id": chat.chat_id,
            "topic": chat.topic,
            "preview_message": get_chat_messages(user_id, chat.chat_id)  # 첫 번째 메시지의 15글자만 가져옴
        }
        for chat in chats
    ]

    else:
        return jsonify({"error": "user_id is required"}), 400
    
    return render_template("tarot_chat.html", chat_list=chat_list, chat_icon_list=chat_icon_list)


@chat_bp.route("/chat_list", methods=["GET"])
def get_chats():
    user_id = current_user.id
    
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    
    chats = get_chat_list(user_id)  # -> Chat.query.filter_b

    chat_list = [
        {
            "chat_id": chat.chat_id,
            "topic": chat.topic,
            "preview_message": get_chat_messages(user_id, chat.chat_id)  # 첫 번째 메시지의 15글자만 가져옴
        }
        for chat in chats
    ]
    
    return jsonify({"chat_list": chat_list})