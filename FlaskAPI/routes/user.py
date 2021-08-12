from FlaskAPI.services.user_services import validate_body
from FlaskAPI.models import company
from FlaskAPI.services.mongodb_connector import MongoDBConnector
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
from models.company import Company
from services import mongodb_connector, user_services
from init_db import db

user_connector: MongoDBConnector = mongodb_connector.MongoDBConnector(User)
company_connector = mongodb_connector.MongoDBConnector(Company)
auth_expiration = 8

def clean_token(string: str):
    return string.replace("Bearer ", "").replace("Bearer: ", "").replace("Bearer:", "")

def get_token_by_email(email: str):
    """
    Retrieves a valid sign-in token by email address.

    If the current session is no longer valid, the tokens are cleared and None is returned.
    """
    user: User = user_connector.get_one(email=email)
    if user:
        d1: datetime = user.lastSignIn
        d2 = datetime.now()
        dd = d2 - d1
        if (dd.total_seconds > (auth_expiration * 60 * 60)):
            user_connector.update(user, authToken="", refreshToken="")
            return None
        else:
            return user.authToken
    else:
        return None

def get_token_by_userid(user_id: str):
    """
    Retrieves a valid sign-in token by userid.

    If the current session is no longer valid, the tokens are cleared and None is returned.
    """
    user: User = user_connector.get_one(userId=user_id)
    if user:
        d1: datetime = user.lastSignIn
        d2 = datetime.now()
        dd = d2 - d1
        if (dd.total_seconds > (auth_expiration * 60 * 60)):
            user_connector.update(user, authToken="", refreshToken="")
            return None
        else:
            return user.authToken
    else:
        return None

def exchange_token(refresh_token: str):
    """
    Use the refresh token to exchange the current auth token for a new one and update the sign-in time stamp.
    
    If the current session is no longer valid, the tokens are cleared and None is returned.
    """
    user: User = user_connector.get_one(refreskToken=refresh_token)

    if user:
        d1: datetime = user.lastSignIn
        d2 = datetime.now()
        dd = d2 - d1
        
        if (dd.total_seconds > (auth_expiration * 60 * 60)):
            user_connector.update(user, authToken="", refreshToken="")
            return None
        else:
            token = secrets.token_urlsafe(2048)
            refreshtoken = secrets.token_urlsafe(2048)
            user_connector.update(user, authToken=token, refreshToken=refreshtoken, lastSignIn = datetime.now())
            
            return (token, refreshtoken)
    else:
        return None

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

        user_services.validate_body(bodyJson, "password", "confirmPassword")

        email = bodyJson["email"]
        password = bodyJson["password"]
        confirmPassword = bodyJson["confirmPassword"]

        if user_services.email_used(email):
            return {"error": "Email already used"}, 400 
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

        user_services.validate_body(bodyJson, "password", "email")

        email = bodyJson["email"]
        password = bodyJson["password"]
        
        try:
            user = user_connector.get_one(email=email)
        except db.DoesNotExist:
            return {"error": "User not found"}, 400
        except Exception as e:
            return {"error": "Server error", "exception": str(e)}, 400
        
        if not user or not check_password_hash(user.passwordHash, password):
            return {"error": "Invalid credentials"}, 400 

        token = secrets.token_urlsafe(2048)
        refreshtoken = secrets.token_urlsafe(2048)

        user_connector.update(user, authToken=token, refreshToken=refreshtoken, lastSignIn=datetime.now())
        login_user(user)

        return {"success": True, "user": user, "authToken": token }

    @route("/fromauth", methods=["POST"])
    @login_required
    def fromauth(self):
        tok = request.headers["Authorization"]
        tok = tok.replace("Bearer ", "").replace("Bearer: ", "").replace("Bearer:", "")
        
        user = user_connector.get_one(authToken=tok)
        
        return {"result": "ok", "success": True, "user": user}, 200
        
        
    @route("/signout", methods=["POST"])
    @login_required
    def signout(self):
        logout_user()
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

        user_services.validate_body(bodyJson, "newEmail", "confirmNewEmail")

        newEmail = bodyJson["newEmail"]
        confirmNewEmail = bodyJson["confirmNewEmail"]

        if (newEmail != confirmNewEmail):
            return {"error": "Emails do not match"}, 400 
        if user_services.email_used(newEmail):
            return {"error": "Email already used"}, 400 

        user_connector.update(current_user, email=newEmail)
        return {"success": True}

    @route("/getUser", methods=["POST"])
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
        
        if not "Authorization" in request.headers:
            return {"success": False}, 401
        
        token = clean_token(request.headers["Authorization"])
        bodyJson = json.loads(request.get_data())

        if "userId" in bodyJson:
            userId = bodyJson["userId"]
        
            try:
                user = user_connector.get_one(userId=userId)
            except:
                return {"error": "User not found"}, 400
        else:
            try:
                user = user_connector.get_one(authToken=token)
            except:
                return {"error": "User not found"}, 400
            
        
        return { "success": True, "user": user }

    @route("/setUser", methods=["POST"])
    def set_user(self):
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
        
        if not "Authorization" in request["headers"]:
            return {"success": False}, 401
        
        token = clean_token(request.headers["Authorization"])
        bodyJson = json.loads(request.get_data())
        details = bodyJson["details"]                
        user = None
        
        if "userId" in bodyJson:
            userId = bodyJson["userId"]            

            try:
                user = user_connector.get_one(userId=userId)
                user_connector.update(user, details)

            except:
                return {"error": "User not found"}, 400
        else:
            try:
                user = user_connector.get_one(authToken=token)
                if "firstName" in details:
                    user_connector.update(user, firstName=details["firstName"])
                if "lastName" in details:
                    user_connector.update(user, lastName=details["lastName"])
                    
            except Exception as e:
                return {"error": "Database Error", "message": str(e), "success": False}, 400
            
        
        return { "success": True }

    @route("/profile", methods=["GET"])
    @login_required
    def profile(self):
        """
        Returns the user that is currently logged in
        """
        return jsonify(current_user)

    # ADMIN (required role)
    
    @route("/invite", methods=["POST"])
    @login_required
    @user_services.role_required("Admin")
    def send_invite(self):
        """
        Sends an invitation to a new user

        Request Body:
            {
                email: str
            }
        """
        pass

    @route("/updateRoles", methods=["POST"])
    @login_required
    @user_services.role_required("Admin")
    def update_roles(self):
        """
        Updates the role of a user

        Request Body:
            {
                email: str
                roles: str[]
            }
        """
        bodyJson = json.loads(request.get_data())

        user_services.validate_body(bodyJson, "email", "roles")

        email = bodyJson["email"]
        roles = bodyJson["roles"]

        try:
            user = user_connector.get_one(email=email)
        except db.DoesNotExist:
            return {"error": "User not found"}, 400
        except Exception as e:
            return {"error": "Server error", "exception": str(e)}, 400 # very bad

        user_connector.update(user, supplyChainRoles=roles)

        return {"success": True}, 200


    @route("/updateCompany", methods=["POST"])
    @login_required
    @user_services.role_required("Admin")
    def update_company(self):
        """
        Updates the information of a company 

        Request Body:
            {
                name: str
                address: str
            }
        """
        bodyJson = json.loads(request.get_data())

        user_services.validate_body(bodyJson, "name", "address")

        name = bodyJson["name"]
        address = bodyJson["address"]

        try:
            company = company_connector.get_one(companyId=current_user.companyId)
        except db.DoesNotExist:
            return {"error": "Company not found"}, 400
        except Exception as e:
            return {"error": "Server error", "exception": str(e)}, 400

        company_connector.update(company, name=name, address=address)

        return {"success": True}

    @route("/removeUser", methods=["POST"])
    @login_required
    @user_services.role_required("Admin")
    def remove_user(self):
        """
        Removes user from company

        Request Body:
            {
                email: str
            }
        """
        bodyJson = json.loads(request.get_data())

        user_services.validate_body(bodyJson, "email")

        email = bodyJson["email"]

        try:
            user = user_connector.get_one(email=email)
        except db.DoesNotExist:
            return {"error": "User not found"}, 400
        except Exception as e:
            return {"error": "Server error", "exception": str(e)}, 400

        user_connector.update(user, companyId="")

        return {"success": True}, 200

    @route("/reportHistory", methods=["GET"])
    @login_required
    @user_services.role_required("Admin")
    def get_report_history(self):
        """
        Gets report history of company(?)
        """
        pass

    @route("/changePassword", methods=["POST"])
    @login_required
    @user_services.role_required("User", "Admin") #user should be able to change their own pass(?)
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

        user_services.validate_body(bodyJson, "email", "newPassword", "confirmNewPassword", "oldPassword")

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

