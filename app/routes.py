from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, login_required

bp = Blueprint('main', __name__)

@bp.route("/login", methods=["GET", "POST"])
def login():
    # if request.method == "POST":
    #     user_id = request.form.get("id")
    #     password = request.form.get("password")

    #     user = authenticate_user(user_id, password)
    #     if user:
    #         login_user(user)
    #         print(f"{user.nickname}님 환영합니다")  # 콘솔 출력
    #         return redirect(url_for("main.main"))
    #     else:
    #         flash("Invalid ID or Password", "error")
    #         return redirect(url_for("main.login"))

    return render_template("main.html")


@bp.route("/chat", methods=['GET'])
# @login_required
def tarot_chat():
    return render_template("tarot_chat.html")