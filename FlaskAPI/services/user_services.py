import hmac
import hashlib
from functools import wraps
from flask_login import current_user

def authenticate_user():    #TODO
    pass


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