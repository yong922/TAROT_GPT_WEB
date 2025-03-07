from flask import Blueprint, jsonify, render_template
from flask_login import login_required, current_user
from app.services.history_service import get_chat_list
from . import chat_history_bp

@chat_history_bp.route("/", methods=['GET'])
@login_required
def tarot_chat():
    """ ✅ 채팅 기록 목록을 가져오는 API """
    chat_icon_list = [
        {'topic': '애정운', 'icon': 'fa-heart'},
        {'topic': '재물운', 'icon': 'fa-coins'},
        {'topic': '학업운', 'icon': 'fa-briefcase'},
        {'topic': '건강운', 'icon': 'fa-medkit'},
        {'topic': '미래운', 'icon': 'fa-crystal-ball'},
    ]

    user_id = current_user.id
    username = current_user.nickname
    chat_list = get_chat_list(user_id)
    
    return render_template("sidebar.html", chat_list=chat_list, chat_icon_list=chat_icon_list, username=username)



