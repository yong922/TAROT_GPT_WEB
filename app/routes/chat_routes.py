from flask import render_template, jsonify, Response, request
from flask_login import login_required, current_user
from app.services.tarot_service import TarotReader
from app.services.history_service import create_chat, save_message, get_latest_chat_id, get_chat_list, get_chat_messages
from app.services.image_service import get_images_url
from . import chat_bp

tarot_reader = TarotReader()


@chat_bp.route("/", methods=['GET'])
@login_required
def tarot_chat():
    """ 
    ✅ 채팅 페이지 메인 API 
    """
    user_id = current_user.id
    user_name = current_user.nickname
    chat_list = get_chat_list(user_id)

    print("DEBUG: chat_list =", chat_list)

    return render_template("tarot_chat.html", 
                           chat_list=chat_list,
                           user_name = user_name)


@chat_bp.route("/set_topic", methods=["POST"])
def set_topic():
    """ 
    ✅ 모델의 토픽 변수 설정 API 
    """
    data = request.get_json()

    if not data or "topic" not in data:
        return jsonify({"status": "error", "message": "토픽 정보가 없습니다."}), 400

    tarot_reader.conversation_state["topic"] = data["topic"]
    
    return jsonify({"status": "success", "message": "토픽이 설정되었습니다."}), 200


@chat_bp.route("/draw_tarot", methods=["POST"])
def draw_tarot():
    """ 
    ✅ 타로 카드를 뽑고 이미지 URL을 반환하는 API 
    """
    drawn_cards = tarot_reader.draw_tarot_cards()
    card_images_url = get_images_url(drawn_cards)

    return jsonify({ "cards": drawn_cards, "card_images_url": card_images_url})


@chat_bp.route("/stream", methods=["POST"])
def chat():
    """
    ✅ Chunk 단위로 응답을 스트리밍하는 API
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
        tarot_reader.process_query(user_message, topic, user_id),
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


@chat_bp.route("/<int:chat_id>", methods=["GET"])
def fetch_chat_messages(chat_id):
    """ 
    ✅ 특정 대화의 메시지를 가져오는 API 
    """
    messages = get_chat_messages(chat_id)
    return jsonify(messages)

