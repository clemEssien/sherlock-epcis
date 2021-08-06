from flask_login import UserMixin
import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from init_db import db

class User(UserMixin, db.Document):
    user_id = db.StringField()
    first_name = db.StringField()
    last_name = db.StringField()
    email = db.StringField()
    role = db.StringField() #User, Admin, Superuser
    password_hash = db.StringField()
    company_id = db.StringField()
    last_sign_in = db.DateTimeField()
    first_sign_in = db.DateTimeField()
    last_password_change = db.DateTimeField()
    password_reset = db.BooleanField()
    account_locked = db.BooleanField()
    auth_token = db.StringField()
    refresh_token = db.StringField()
    address1 = db.StringField()
    address2 = db.StringField(required=False)
    city = db.StringField()
    state = db.StringField()
    zip = db.StringField()
    country = db.StringField()
    phone = db.IntField()
    email = db.StringField()
