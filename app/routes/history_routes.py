# from flask import render_template, jsonify, Response, request
# from flask_login import login_required, current_user
# from app.services.history_service import get_chat_list
# from . import history_bp

# @history_bp.route("/chats", methods=["GET"])
# def get_chats():
#     user_id = user_id = current_user.id
#     if not user_id:
#         return jsonify({"error": "user_id is required"}), 400
    
#     chats = get_chat_list(user_id)
#     chat_list = [{"chat_id": chat.chat_id, "topic": chat.topic} for chat in chats]

#     return jsonify(chat_list)