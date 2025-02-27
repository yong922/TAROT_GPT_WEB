from flask import render_template, jsonify, Response, request
from flask_login import login_required
from app.services.tarot_service_test import TarotReader
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
    """ ✅ Chunk 단위로 응답을 스트리밍하는 API"""
    data = request.json
    user_message = data.get("message", "").strip()
    # topic = data.get("topic","").strip()
    # cards = data.get("cards", [])  # 클라이언트에서 카드 3장 정보를 가져오도록 함

    if not user_message:
        return Response("No message received", status=400)
    
    return Response(
        tarot_reader.process_query(user_message),
        content_type="text/plain"
    )


@chat_bp.route("/", methods=['GET'])
@login_required
def tarot_chat():
    """채팅 기록을 가져오는 API"""
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
