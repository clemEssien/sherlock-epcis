import hmac
import hashlib

def authenticate_user():    #TODO
    pass

def create_hash(key: str, message: str) -> str:
    key_bytes = key.encode()
    message_bytes = message.encode()
    return hmac.new(key_bytes, msg=message_bytes, digestmod=hashlib.sha256).hexdigest().upper()