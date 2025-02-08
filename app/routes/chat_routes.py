from flask import render_template, jsonify
from flask_login import login_required
from app.services.chat_service import ChatService
from app.services.tarot_service import TarotReader
from . import chat_bp

chat_service = ChatService()
tarot_reader = TarotReader()

@chat_bp.route("/", methods=['GET'])
@login_required
def tarot_chat():
    return render_template("tarot_chat copy.html")

@chat_bp.route("/chat_page/", methods=['GET'])
def chat_page():
    return render_template("tarot_chat.html")

@chat_bp.route('/get_initial_message/', methods=['GET'])
def get_initial_message():
    response_messages = chat_service.get_initial_message()
    return jsonify(response_messages)
