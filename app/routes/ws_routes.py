from flask import request
from flask_socketio import emit
from app.services.chat_service import ChatService
from app import socketio
from . import ws_bp

chat_service = ChatService()

@socketio.on("connect")
def handle_connect():
    print(f"사용자 연결됨: {request.sid}")
    
    # 초기 메시지 가져오기
    initial_messages = chat_service.get_initial_message()
    
    # 기존 메시지를 클라이언트에게 전송
    for msg in initial_messages:
        emit("new_message", {"sender": msg["sender"], "message": msg["text"]})

@socketio.on("send_message")
def handle_message(data):
    user_message = data.get("text", "")
    
    # 사용자 메시지 추가
    chat_service.add_user_message(user_message)

    # 메시지 처리 및 봇 응답 생성
    bot_response = chat_service.process_message(user_message)
    
    # 챗봇 응답 저장
    chat_service.add_bot_message(bot_response)

    # 사용자 메시지 및 봇 응답 전송
    emit("new_message", {"sender": "user", "message": user_message}, broadcast=True)
    emit("new_message", {"sender": "bot", "message": bot_response}, broadcast=True)
