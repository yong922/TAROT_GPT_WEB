from flask import Flask
from app.models import db  
from app.routes import bp 
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from flask_login import LoginManager
login_manager = LoginManager()

migrate = Migrate()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    print(f"SECRET_KEY: {app.config['SECRET_KEY']}")
    
    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(bp)

    return app