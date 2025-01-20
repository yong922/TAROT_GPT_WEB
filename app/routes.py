from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, login_required
from app.services.user_service import authenticate_user_plain
from app.forms import UserLoginForm, UserCreateForm
from flask_login import login_user, current_user

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        # POST 요청에서 데이터 확인
        id = form.id.data
        pw = form.pw.data

        # result = authenticate_user(id, pw)
        result = authenticate_user_plain(id, pw)

        if result['success']:
            user = result['user']
            login_user(user)
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


@bp.route("/chat/", methods=['GET'])
@login_required
def tarot_chat():
    return render_template("tarot_chat.html")