from flask import Flask, jsonify, request
from flask_classful import FlaskView, route
from neo4j import GraphDatabase

import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import JSONDeserialization.epcis_event as epc
import JSONDeserialization.extract_gis_from_json as ex_json
import XMLDeserialization.extract_gis_from_xml as ex_xml

# Temporary sandbox database, expires June 21 at 3:20pm
USER = "neo4j"
PASS = "emitter-juries-tunes"
URI = "bolt://35.172.233.63:7687"
driver = GraphDatabase.driver(uri=URI, auth=(USER, PASS))

app = Flask(__name__)

event_types = {
    "ObjectEvent": epc.ObjectEvent(),
    "AggregationEvent": epc.AggregationEvent(),
    "QuantityEvent": epc.QuantityEvent(),
    "TransactionEvent": epc.TransactionEvent(),
    "TransformationEvent": epc.TransformationEvent(),
}


class JSONView(FlaskView):
    route_base = "/json"

    @route("/", methods=["GET"])
    def index(self):
        with driver.session() as session:
            q = "match (n:Event) return n"
            results = session.run(q).data()
        return jsonify(results)

    @route("/", methds=["POST"])
    def post(self):
        """POST an JSON EPCIS event to add to db"""
        epcis_json = request.get_json()
        event = event_types[epcis_json["isA"]]
        ex_json.map_from_epcis(event, epcis_json)
        q = "create (:Event{eventTime: datetime($eventTime), eventTimeZoneOffset: $eventTimeZoneOffset})"
        qmap = {
            "eventTime": str(event.event_time),
            "eventTimeZoneOffset": str(event.event_timezone_offset),
        }
        try:
            with driver.session() as session:
                session.run(q, qmap)
            return "Event added"
        except Exception as e:
            return str(e)

class XMLView(FlaskView):
    route_base = "/xml"


JSONView.register(app)
