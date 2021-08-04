import mongoengine as me
from flask_login import UserMixin

class User(UserMixin, me.Document):
    user_id = me.StringField()
    first_name = me.StringField()
    last_name = me.StringField()
    email = me.StringField()
    role = me.StringField() #User, Admin, Superuser
    password_hash = me.StringField()
    company_id = me.StringField()
    last_sign_in = me.DateTimeField()
    first_sign_in = me.DateTimeField()
    last_password_change = me.DateTimeField()
    password_reset = me.BooleanField()
    account_locked = me.BooleanField()
    auth_token = me.StringField()
    refresh_token = me.StringField()
    address1 = me.StringField()
    address2 = me.StringField(required=False)
    city = me.StringField()
    state = me.StringField()
    zip = me.StringField()
    country = me.StringField()
    phone = me.IntField()
    email = me.StringField()
