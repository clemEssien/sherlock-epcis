import mongoengine as me

class Company(me.Document):
    company_id = me.StringField()
    name = me.StringField()
    address = me.StringField()