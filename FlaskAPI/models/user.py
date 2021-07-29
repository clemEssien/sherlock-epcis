import mongoengine as me

class User(me.Document):
    user_id = me.IntField()
    first_name = me.StringField()
    last_name = me.StringField()
    email = me.StringField()
    role = me.StringField() #User, Admin, Superuser
    password_hash = me.StringField()
    companyId = me.StringField()
