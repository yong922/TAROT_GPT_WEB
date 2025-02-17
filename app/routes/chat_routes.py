from flask import render_template, jsonify, Response, request
from flask_login import login_required
from app.services.tarot_service import TarotReader
from . import chat_bp

tarot_reader = TarotReader()

@chat_bp.route("/stream", methods=["POST"])
def chat():
    """Chunk 단위로 응답을 스트리밍하는 API"""
    data = request.json
    user_message = data.get("message", "").strip()
    topic = data.get("topic","").strip()

    if not user_message:
        return Response("No message received", status=400)

    return Response(
        tarot_reader.process_query(user_message, topic),
        content_type="text/plain"
    )


@chat_bp.route("/", methods=['GET'])
@login_required
def tarot_chat():
    return render_template("tarot_chat copy 2.html")

@chat_bp.route("/chat_page/", methods=['GET'])
def chat_page():
    return render_template("tarot_chat.html")

@chat_bp.route('/get_initial_message/', methods=['GET'])
def get_initial_message():
    response_messages = chat_service.get_initial_message()
    return jsonify(response_messages)
