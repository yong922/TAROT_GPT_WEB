from flask_socketio import SocketIO, emit
from flask import request

socketio = SocketIO(cors_allowed_origins="*")  # CORS 설정

class WebSocketService:
    def __init__(self, app):
        socketio.init_app(app)

    @staticmethod
    @socketio.on("connect")
    def handle_connect():
        print("Client connected")
        emit("response", {"message": "웹소켓 연결 성공!"})

    @staticmethod
    @socketio.on("disconnect")
    def handle_disconnect():
        print("Client disconnected")

    @staticmethod
    @socketio.on("chat_message")
    def handle_chat_message(data):
        print(f"Received message: {data}")
        response_text = f"'{data['message']}'에 대한 타로 리딩 결과를 준비 중입니다."
        emit("response", {"message": response_text})
