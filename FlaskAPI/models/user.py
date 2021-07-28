import mongoengine as me

class User(me.Document):
    first_name = me.StringField()
    last_name = me.StringField()
    email = me.StringField()
    role = me.StringField() #User, Admin, Superuser
    password_hash = me.StringField()
    companyId = me.StringField()
