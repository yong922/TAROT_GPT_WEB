from flask import Blueprint

auth_bp = Blueprint('main', __name__)
chat_bp = Blueprint('chat', __name__)
history_bp = Blueprint('history', __name__)

from . import auth_routes, chat_routes, history_routes
