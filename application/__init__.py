from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO
from config import config
from socketio import Server

db=SQLAlchemy()
migrate=Migrate()
login_manager=LoginManager()
socketio=SocketIO(max_http_buffer_size=5*1024*1024)

def create_app(config_name):
    app=Flask(__name__)

    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app=app, db=db)
    login_manager.init_app(app)
    socketio.init_app(app)
    login_manager.login_view='main.index'

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    # from .api import api as api_blueprint
    # app.register_blueprint(api_blueprint)
    return app