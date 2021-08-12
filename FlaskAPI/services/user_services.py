from FlaskAPI.services.mongodb_connector import MongoDBConnector
import hmac
import hashlib
from functools import wraps
from flask_login import current_user
from FlaskAPI.models.user import User

user_connector = MongoDBConnector(User)

def email_used(email: str) -> bool:
    try:
        user = user_connector.get_one(email=email)
    except: # none found
        return False
    return True

def role_required(*roles):
    """
    Decorator for role based authorization, takes in roles as args
    """

    def decorator(func):
        @wraps(func)
        def authorized(*args, **kargs):
            if current_user.role in roles:
                return func(*args, **kargs)
            return {"error": "Current user is not authorized"}

        return authorized
    return decorator