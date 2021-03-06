from flask import Flask, jsonify, request
import uuid
from flask_classful import FlaskView, route
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user, LoginManager

from dotenv import load_dotenv
import os, sys
import json
import secrets
from datetime import datetime

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
                password: str,
                confirmPassword: str,
                email: str,
            }
        """
        userId = str(uuid.uuid4())
        bodyJson=json.loads(request.get_data())

        for key in ["email", "password", "confirmPassword"]:
            if not (key in bodyJson):
                return {"error": "Bad Data"}, 401

        email = bodyJson["email"]
        password = bodyJson["password"]
        confirmPassword = bodyJson["confirmPassword"]

        if password != confirmPassword:
            return {"error": "Passwords do not match"}, 400 

        user_connector.create_one(
            userId=userId, 
            email=email,
            role="User",
            passwordHash=generate_password_hash(password)
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
        bodyJson = json.loads(request.get_data())

        for key in ["password", "email"]:
            if not (key in bodyJson):
                return {"error": "Bad Data"}, 401

        email = bodyJson["email"]
        password = bodyJson["password"]
        
        try:
            user = user_connector.get_one(email=email)
        except db.DoesNotExist:
            return {"error": "User not found"}, 400
        except:
            return {"error": "Server error"}, 400
        
        if not user or not check_password_hash(user.passwordHash, password):
            return {"error": "Invalid credentials"}, 400 

        token = secrets.token_urlsafe(2048)
        user_connector.update(user, authToken=token, lastSignIn=datetime.now())
        login_user(user)

        return {"success": True}

    @route("/signout", methods=["POST"])
    @login_required
    def signout(self):
        logout_user()
        return {"success": True}

    @route("/changePassword", methods=["POST"])
    def change_password(self):
        """
        Changes the password for a given user

        Request Body:
            {
                email: str,
                oldPassword: str,
                newPassword: str,
                confirmNewPassword: str,
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
        bodyJson = json.loads(request.get_data())

        # check the body for the minimum required variables for this call:
        for key in ["email", "newPassword", "confirmNewPassword", "oldPassword"]:
            if not (key in bodyJson):
                return {"error": "Bad Data"}, 401

        newPassword = bodyJson["newPassword"]
        confirmNewPassword = bodyJson["confirmNewPassword"]
        email = bodyJson["email"]
        oldPassword = bodyJson["oldPassword"]

        try:
            user = user_connector.get_one(email=email)
        except db.DoesNotExist:
            return {"error": "User not found"}, 400
        except:
            return {"error": "Server error"}, 400

        if (not check_password_hash(user.passwordHash, oldPassword)):
            return {"error": "Incorrect password"}, 400 
        if (newPassword != confirmNewPassword):
            return {"error": "New passwords do not match"}, 400 

        user_connector.update(user, passwordHash=generate_password_hash(newPassword))
        return {"success": True}

    @route("/changeEmail", methods=["POST"])
    @login_required
    def change_email(self):
        """
        Changes the email for a given user

        Request Body:
            {
                newEmail: str,
                confirmNewEmail: str,
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
        bodyJson = json.loads(request.get_data())

        for key in ["newEmail", "confirmNewEmail"]:
            if not (key in bodyJson):
                return {"error": "Bad Data"}, 401

        newEmail = bodyJson["newEmail"]
        confirmNewEmail = bodyJson["confirmNewEmail"]

        if (newEmail != confirmNewEmail):
            return {"error": "Emails do not match"}, 400 

        user_connector.update(current_user, email=newEmail)
        return {"success": True}

    @route("/getUser", methods=["GET"])
    def get_user(self):
        """
        Gets a single user based off of id

        Request Body:
            {
                userId: str,
            }

        Error Codes:
            400: User not found

        On Success (200):
            {
                ... (user object)
            }
        """
        bodyJson = json.loads(request.get_data())

        for key in ["userId"]:
            if not (key in bodyJson):
                return {"error": "Bad Data"}, 401

        userId = bodyJson["userId"]
        
        try:
            user = user_connector.get_one(userId=userId)
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
