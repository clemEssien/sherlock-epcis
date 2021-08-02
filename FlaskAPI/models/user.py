import mongoengine as me

class User(me.Document):
    user_id = me.StringField()
    first_name = me.StringField()
    last_name = me.StringField()
    email = me.StringField()
    role = me.StringField() #User, Admin, Superuser
    password_hash = me.StringField()
    company_id = me.StringField()
