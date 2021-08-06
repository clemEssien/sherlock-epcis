from flask import Flask, jsonify, request
import uuid
from flask_classful import FlaskView, route
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user, LoginManager

from dotenv import load_dotenv
import os, sys
import json

load_dotenv()
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from models.user import User
from services import mongodb_connector
from init_db import db

user_connector = mongodb_connector.MongoDBConnector(User)

class UserView(FlaskView):
    route_base = "/api/users"

    @route("/create", methods=["POST"])
    def create_user(self):
        """
        Allows a new user to sign up and creates id info

        Request Body:
            {
                first_name: str,
                last_name: str,
                password: str,
                email: str,
            }
        """
        user_id = str(uuid.uuid4())

        body_json=json.loads(request.get_data())
        email = body_json["email"]
        password = body_json["password"]
        last_name=body_json["last_name"]
        first_name=body_json["first_name"]

        user_connector.create_one(
            user_id=user_id, 
            email=email,
            last_name=last_name, 
            first_name=first_name,
            role="User",
            password_hash=generate_password_hash(password)
        )

        return {"success": True}

    @route("/signin", methods=["POST"])
    def signin(self):
        """
        Allows a user to sign in to their session

        Request Body:
            {
                password: str,
                email: str,
            }
        """
        body_json = json.loads(request.get_data())

        for key in ["password", "email"]:
            if not (key in body_json):
                return {"error": "Bad Data"}, 401

        email = body_json["email"]
        password = body_json["password"]
        
        try:
            user = user_connector.get_one(email=email)
        except db.DoesNotExist:
            return {"error": "User not found"}, 400
        except:
            return {"error": "Server error"}, 400
        
        if not user or not check_password_hash(user.password_hash, password):
            return {"error": "Invalid credentials"}, 400 

        login_user(user)

        return {"success": True}

    @route("/signout", methods=["POST"])
    @login_required
    def signout(self):
        logout_user()
        return {"success": True}

    @route("/change_password", methods=["POST"])
    def change_password(self):
        """
        Changes the password for a given user

        Request Body:
            {
                email: str,
                old_password: str,
                new_password: str,
                confirm_new_password: str,
            }

        Error Codes:
            400: User not found
            400: Incorrect password
            400: New passwords do not match
            400: Server error

        On Success (200):
            {
                success: true
            }
        """
        body_json = json.loads(request.get_data())

        # check the body for the minimum required variables for this call:
        for key in ["email", "new_password", "confirm_new_password", "old_password"]:
            if not (key in body_json):
                return {"error": "Bad Data"}, 401

        new_password = body_json["new_password"]
        confirm_new_passwords = body_json["confirm_new_password"]
        email = body_json["email"]
        old_password = body_json["old_password"]

        try:
            user = user_connector.get_one(email=email)
        except db.DoesNotExist:
            return {"error": "User not found"}, 400
        except:
            return {"error": "Server error"}, 400

        if (not check_password_hash(user.password_hash, old_password)):
            return {"error": "Incorrect password"}, 400 
        if (new_password != confirm_new_passwords):
            return {"error": "New passwords do not match"}, 400 

        user_connector.update(user, password_hash=generate_password_hash(new_password))
        return {"success": True}

    @route("/change_email", methods=["POST"])
    @login_required
    def change_email(self):
        """
        Changes the email for a given user

        Request Body:
            {
                new_email: str,
                confirm_new_email: str,
            }

        Error Codes:
            400: User not found
            400: Server error
            400: Incorrect password
            400: New emails do not match

        On Success (200):
            {
                success: true
            }
        """
        body_json = json.loads(request.get_data())

        for key in ["new_email", "confirm_new_email"]:
            if not (key in body_json):
                return {"error": "Bad Data"}, 401

        new_email = body_json["new_email"]
        confirm_new_email = body_json["confirm_new_email"]

        if (new_email != confirm_new_email):
            return {"error": "Emails do not match"}, 400 

        user_connector.update(current_user, email=new_email)
        return {"success": True}

    @route("/get_user", methods=["GET"])
    def get_user(self):
        """
        Gets a single user based off of id

        Request Body:
            {
                user_id: str,
            }

        Error Codes:
            400: User not found

        On Success (200):
            {
                ... (user object)
            }
        """
        body_json = json.loads(request.get_data())
        user_id = body_json["user_id"]
        
        try:
            user = user_connector.get_one(user_id=user_id)
        except:
            return {"error": "User not found"}, 400

        return jsonify(user)

    @route("/profile", methods=["GET"])
    @login_required
    def profile(self):
        """
        Returns the user that is currently logged in
        """
        return jsonify(current_user)
