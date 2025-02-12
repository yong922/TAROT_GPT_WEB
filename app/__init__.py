from flask import Flask, session, redirect
from app.models import db, User
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
# from flask_socketio import SocketIO

# socketio = SocketIO()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    # socketio.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    
    from app.routes import bp
    app.register_blueprint(bp)

    return app