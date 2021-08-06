import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from init_app import db

class Company(db.Document):
    company_id = db.StringField()
    name = db.StringField()
    address = db.StringField()