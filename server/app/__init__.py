from flask import Flask
from flask_cors import CORS
from app.auth.routes import auth_bp
from app.config import SECRET_KEY
from app.travels.routes import travels_bp
from app.db import create_users_table_if_not_exists
from app.db import create_travels_table_if_not_exists

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = SECRET_KEY
    create_users_table_if_not_exists()
    create_travels_table_if_not_exists()
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(travels_bp, url_prefix='/travels')
    return app
