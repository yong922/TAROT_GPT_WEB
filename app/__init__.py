from flask import Flask
from flask_login import LoginManager
from app.models import get_db_connection, User

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.secret_key = '1234'  # 세션용 secret key

    # Flask-Login 초기화
    login_manager.init_app(app)
    login_manager.login_view = "login"

    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, password, nickname FROM user_tb WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return User(user["id"], user["password"], user["nickname"])
    return None
