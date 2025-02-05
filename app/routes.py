from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify, session
from flask_login import login_user, login_required
from app.services.chat_service import ChatService
from app.services.user_service import authenticate_user, register_user, id_available
from app.forms import UserLoginForm, UserCreateForm
from flask_login import login_user, current_user

bp = Blueprint('main', __name__)
chat_service = ChatService()

@bp.route('/', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    
    if request.method == 'POST' and form.validate_on_submit():

        id = form.id.data
        pw = form.pw.data

        result = authenticate_user(id, pw)

        if result['success']:
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




@bp.route("/chat/", methods=['GET'])
@login_required
def tarot_chat():
    return render_template("tarot_chat.html")

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


# 사용자 메시지 전송, 저장된 전체 메시지 반환
@bp.route('/send_message/', methods=['POST'])
def send_message():
    data = request.get_json()
    user_message = data.get('text', '')

    if user_message:
        chat_service.add_user_message(user_message)

    # 업데이트된 메시지 반환
    # response_messages = chat_service.get_initial_message()
    response_messages = chat_service.messages
    return jsonify(response_messages)

#-----타로 리딩-----
# 사용자 메시지 전송 시, 리스트에 저장된 메시지를 전달
# @bp.route("/tarot_reading/", methods=['POST'])