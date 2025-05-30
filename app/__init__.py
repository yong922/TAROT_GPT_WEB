from flask import Flask
from app.models import db, User
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from app.config import Config

login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    app.config.from_object(Config)
    csrf.init_app(app)
    
    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"  
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    
    from app.routes import auth_bp, chat_bp
    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(chat_bp, url_prefix='/chat')

    return app
