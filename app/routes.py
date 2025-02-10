from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify, session
from flask_login import login_user, login_required
from app.services.chat_service import ChatService
from app.services.user_service import authenticate_user, register_user
from app.services.tarot_reading_service import TarotReader
from app.forms import UserLoginForm, UserCreateForm
from flask_login import login_user, current_user
from flask_socketio import emit
from app import socketio
import asyncio  # 비동기 처리

bp = Blueprint('main', __name__)
chat_service = ChatService()
tarot_reader = TarotReader()



@bp.route('/', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        # POST 요청에서 데이터 확인
        id = form.id.data
        pw = form.pw.data

        result = authenticate_user(id, pw)

        if result['success']:
            # print(result['user']) # 출력형식 : <User kay>
            login_user(result['user'])
            return redirect(url_for('main.tarot_chat'))
        else:
            return render_template('main.html', form=form, error=result['message'])
    return render_template('main.html', form=form)  


@bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        result = register_user(
            id=form.id.data,
            pw=form.pw.data,
            nickname=form.nickname.data
        ) 
        if result['success']:
            return redirect(url_for('main.login'))
        else:
            flash(result['message'])
    return render_template('sign_up.html', form=form)

@bp.route('/check_id/', methods=['POST'])
def check_id():
    id = request.json.get('user_id')

    result = id_available(id=id)

    return jsonify(result)

# @bp.route("/chat/", methods=['GET'])
# @login_required
# def tarot_chat():
#     return render_template("tarot_chat.html")

#------
# 채팅 페이지
@bp.route("/chat_page/", methods=['GET'])
def chat_page():
    return render_template("tarot_chat.html")


# 초기 메시지(봇 인사말) 반환
@bp.route('/get_initial_message/', methods=['GET'])
def get_initial_message():
    response_messages = chat_service.get_initial_message()
    return jsonify(response_messages)


# # 사용자 메시지 전송, 저장된 전체 메시지 반환
# @bp.route('/send_message/', methods=['POST'])
# def send_message():
#     data = request.get_json()
#     user_message = data.get('text', '')

#     if user_message:
#         chat_service.add_user_message(user_message)

#     # 업데이트된 메시지 반환
#     # response_messages = chat_service.get_initial_message()
#     response_messages = chat_service.messages
#     return jsonify(response_messages)



# ==============WebSocket================
# login_required 빼놓음

# WebSocket 연결 핸들러
@socketio.on("connect")
def handle_connect():
    print(f"사용자 연결됨: {request.sid}")
    
    # 초기 메시지 가져오기
    if chat_service.initialized:
        initial_messages = chat_service.get_initial_message()

    # 기존 메시지를 클라이언트에게 전송
    for msg in initial_messages:
        emit("new_message", {"sender": msg["sender"], "message": msg["text"]})

# WebSocket 메시지 핸들러
# '웹소켓 메시지'를 처리하는 부분(HTTP 요청 처리가 아님XXXX)
@socketio.on("send_message")
async def handle_message(data):
    user_message = data.get("text", "")

    # 사용자 메시지 추가
    chat_service.add_user_message(user_message)

    # 사용자 메시지를 클라이언트에 즉시 표시(전송)
    emit("new_message", {"sender": "user", "message": user_message}, broadcast=True)
    
    async def stream_callback(chunk):
        # 실시간 전송
        emit("stream_message", {"chunk": chunk}, broadcast=True)
        await asyncio.sleep(0)
    
    # TarotReader의 process_query 실행 -> 스트리밍 전송
    bot_response = tarot_reader.process_query(user_message, stream_callback=stream_callback)
    
    # 최종 챗봇 응답 저장
    chat_service.add_bot_message(bot_response)
    #===============수정전=================
    # 사용자 메시지 추가
    # chat_service.add_user_message(user_message)

    # # 메시지 처리 및 봇 응답 생성
    # bot_response = chat_service.process_message(user_message)
    
    # # 챗봇 응답 저장
    # chat_service.add_bot_message(bot_response)

    # # 사용자 메시지 및 봇 응답 전송
    # emit("new_message", {"sender": "user", "message": user_message}, broadcast=True)  # 사용자가 보낸 메시지를 모든 클라이언트에게 전송 (사용자의 메시지 표시)
    # emit("new_message", {"sender": "bot", "message": bot_response}, broadcast=True)  # 봇의 응답 메시지를 모든 클라이언트에게 전송 (봇의 리딩 결과 표시