from flask import Flask, jsonify, request
from flask_classful import FlaskView, route
from flask_mongoengine import MongoEngine
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
from init_db import db
from init_mail import mail
from models.user import User
import base64 

from dotenv import load_dotenv
import os, sys

load_dotenv()
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


def create_app():
    app = Flask(__name__)
    app.config['MONGODB_SETTINGS'] = {
        "host": os.getenv('MONGODB_HOST')
    }
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

    app.secret_key = 'some key'
    db.init_app(app)
    mail.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.objects.get(id=user_id)
        except:
            return None

    @login_manager.unauthorized_handler
    def unauthorized():
        return {"error": "Not logged in"}, 401

    @login_manager.needs_refresh_handler
    def refresh():
        login_user(current_user)
        return {"success": True}, 200
    
    @login_manager.request_loader
    def load_user_from_request(request):

        api_key = request.args.get('api_key')
        if api_key:
            user = User.objects.get(authToken=api_key)
            if user:
                return user

        api_key = request.headers.get('Authorization')
        if api_key:
            api_key = api_key.replace('Basic ', '', 1)
            try:
                api_key = base64.b64decode(api_key)
            except TypeError:
                pass
            user = User.objects.get(authToken=api_key)
            if user:
                return user

        return None

    return app