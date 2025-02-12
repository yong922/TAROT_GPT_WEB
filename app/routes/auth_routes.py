from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user
from app.services.user_service import authenticate_user, register_user, id_available
from app.forms import UserLoginForm, UserCreateForm
from . import auth_bp


@auth_bp.route('/', methods=['GET', 'POST'])
def login():

    form = UserLoginForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        id = form.id.data
        pw = form.pw.data
        result = authenticate_user(id, pw)

        if result['success']:
            login_user(result['user'])
            return redirect(url_for('chat.tarot_chat'))
        else:
            return render_template('main.html', form=form, error=result['message'])

    return render_template('main.html', form=form)

@auth_bp.route('/signup/', methods=['GET', 'POST'])
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

@auth_bp.route('/check_id/', methods=['POST'])
def check_id():
    id = request.json.get('user_id')
    result = id_available(id=id)
    return jsonify(result)

@auth_bp.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("main.login"))
