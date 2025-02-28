from flask import render_template, jsonify, Response, request
from flask_login import login_required, current_user
from app.services.tarot_service import TarotReader
from app.services.history_service import create_chat, save_user_message, save_bot_message, get_latest_chat_id
from . import chat_bp

tarot_reader = TarotReader()

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

    print(f"📡 [input] user_id: {user_id}, 받은 chat_id: {data.get('chat_id')}")

    if not user_message:
        return Response("No message received", status=400)

    if not chat_id :
        chat_id = create_chat(user_id, topic)

    save_user_message(chat_id, user_message)

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

    print(f"📡 [get_latest_chat_id] user_id: {user_id}, 반환된 chat_id: {chat_id}")

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

    last_message = chat_history[-1].content

    save_bot_message(chat_id, last_message)

    return jsonify({"status": "success", "message": "Bot response saved."})


@chat_bp.route("/", methods=['GET'])
@login_required
def tarot_chat():
    chat_icon_list = [
        {'topic': '애정운', 'icon': 'fa-heart'},
        {'topic': '금전운', 'icon': 'fa-coins'},
        {'topic': '취업운', 'icon': 'fa-briefcase'},
        {'topic': '건강운', 'icon': 'fa-medkit'},
    ]
    chat_list = [
        {'topic': '애정운', 'title': '애정운대화1'}, 
        {'topic': '금전운', 'title': '금전운대화2'}, 
        {'topic': '취업운', 'title': '취업운대화3'},
        {'topic': '건강운', 'title': '건강운대화4'},
        ]
    username = 'qwer'
    return render_template("tarot_chat.html", chat_list=chat_list, username=username, chat_icon_list=chat_icon_list)
