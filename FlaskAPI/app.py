from flask import Flask
from flask_classful import FlaskView
import JSONDeserialization.epcis_event

app = Flask(__name__)


class EventView(FlaskView):
    def index(self):
        return "Event Index"
