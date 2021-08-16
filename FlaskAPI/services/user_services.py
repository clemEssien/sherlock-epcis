from FlaskAPI.services.mongodb_connector import MongoDBConnector
import hmac
import hashlib
from functools import wraps
from flask_login import current_user
from FlaskAPI.models.user import User
from datetime import datetime
import secrets

user_connector = MongoDBConnector(User)

def authorize_user(header) -> bool: # checks header for Authorization
    if not "Authorization" in header:
        return {"success": False}, 401
    token = clean_token(header["Authorization"])
    if not current_user.authToken == token:
        return {"error": "User authorized with incorrect token"}, 401

def email_used(email: str) -> bool:
    try:
        user = user_connector.get_one(email=email)
    except: # none found
        return False
    return True

def validate_body(body, *args):
    for key in args:
        if not key in body:
            return {"error": "Bad Data"}, 401

def role_required(*roles):
    """
    Decorator for role based authorization, takes in roles as args
    """

    def decorator(func):
        @wraps(func)
        def authorized(*args, **kargs):
            if current_user.role in roles:
                return func(*args, **kargs)
            return {"error": "Current user is not authorized"}, 401

        return authorized
    return decorator

# TOKENS

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