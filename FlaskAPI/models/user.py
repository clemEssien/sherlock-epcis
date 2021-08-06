from flask_login import UserMixin
import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from init_db import db

class User(UserMixin, db.Document):
    userId = db.StringField()
    firstName = db.StringField()
    lastName = db.StringField()
    email = db.StringField()
    role = db.StringField() #User, Admin, Superuser
    passwordHash = db.StringField()
    companyId = db.StringField()
    lastSignIn = db.DateTimeField()
    firstSignIn = db.DateTimeField()
    lastPasswordChange = db.DateTimeField()
    passwordReset = db.BooleanField()
    accountLocked = db.BooleanField()
    authToken = db.StringField()
    refreshToken = db.StringField()
    address1 = db.StringField()
    address2 = db.StringField(required=False)
    city = db.StringField()
    state = db.StringField()
    zip = db.StringField()
    country = db.StringField()
    phone = db.IntField()
    email = db.StringField()
