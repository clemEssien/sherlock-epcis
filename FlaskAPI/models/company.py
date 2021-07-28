import mongoengine as me

class Company(me.Document):
    name = me.StringField()
    address = me.StringField()