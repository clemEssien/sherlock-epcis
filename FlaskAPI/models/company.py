import mongoengine as me

class Company(me.Document):
    company_id = me.IntField()
    name = me.StringField()
    address = me.StringField()