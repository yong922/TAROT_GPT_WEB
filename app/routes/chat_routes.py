from flask import render_template, jsonify, Response, request
from flask_login import login_required
from app.services.chat_service import ChatService
from app.services.tarot_service import TarotReader
from . import chat_bp

chat_service = ChatService()
tarot_reader = TarotReader()

@chat_bp.route("/stream", methods=["POST"])
def chat():
    """Chunk 단위로 응답을 스트리밍하는 API"""
    data = request.json
    user_message = data.get("message", "").strip()

    if not user_message:
        return Response("No message received", status=400)

    return Response(
        tarot_reader.process_query(user_message),
        content_type="text/plain"
    )

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
    return render_template("tarot_chat copy 2.html", chat_list=chat_list, username=username, chat_icon_list=chat_icon_list)

@chat_bp.route("/chat_page/", methods=['GET'])
def chat_page():
    return render_template("tarot_chat.html")

@chat_bp.route('/get_initial_message/', methods=['GET'])
def get_initial_message():
    response_messages = chat_service.get_initial_message()
    return jsonify(response_messages)
