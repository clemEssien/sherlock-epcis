from flask import Flask, jsonify, request
from flask_classful import FlaskView, route
from neo4j import GraphDatabase

import os, sys
import xml.etree.ElementTree as ET

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
    "ObjectEvent": epc.ObjectEvent,
    "AggregationEvent": epc.AggregationEvent,
    "QuantityEvent": epc.QuantityEvent,
    "TransactionEvent": epc.TransactionEvent,
    "TransformationEvent": epc.TransformationEvent,
}

class EventView(FlaskView):
    route_base = "/event"

    @route("/", methods=["GET"])
    def index(self):
        """
        IN PROGRESS
        Gets EPCIS event data

        Error Codes:

        On Success (200):

        """
        with driver.session() as session:
            q = "match (n:Event) return n"
            results = session.run(q).data()
        return jsonify(results), 200

class JSONView(FlaskView):
    route_base = "/json"

    @route("/", methods=["POST"])
    def post(self):
        """POST an JSON EPCIS event to add to db"""
        epcis_json = request.get_json()
        event = event_types[epcis_json["isA"]]()
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

    @route("/", methods=["POST"])
    def post(self):
        """
        IN PROGRESS
        Posts XML EPCIS event to add to db

        Content Type: application/xml

        Request Body: 
            xml data of epcis

        Error Codes:
            400: Bad request

        On Success (200):
            {
                success: true
                events: EPCISEvent[]
            }
        """
        epcis_xml = str(request.get_data(), "utf-8") 
        
        root = ET.fromstring(epcis_xml)

        if root.tag != "{urn:epcglobal:epcis:xsd:1}EPCISDocument":
            return {"error": "Not EPCISDocument"}, 400

        events = []
        for child in root:
            for event_list in child:
                for event in event_list:
                    d = ex_xml.map_xml_to_dict(event)
                    try:
                        xml_doc = d[event.tag]
                        epcis_event_obj = event_types[event.tag]()
                    except Exception:
                        event_from_xml = ex_xml.find_event_from_xml(event, event_types)
                        epcis_event_obj = event_types[event_from_xml]
                        pass

                    xml_dict = ex_xml.map_to_epcis_dict(xml_doc)
                    ex_xml.map_from_epcis(epcis_event_obj, xml_dict)
                    events.append({     #Event object not json serializable
                        "_event_time": str(epcis_event_obj._event_time),
                        "_event_timezone_offset": str(epcis_event_obj._event_timezone_offset),
                        "_extensions": str(epcis_event_obj._extensions),
                        "_action": str(epcis_event_obj._action),
                        "_business_step": str(epcis_event_obj._business_step),
                    })

        return {"success": True, "events": events}, 200
        

EventView.register(app)
JSONView.register(app)
XMLView.register(app)

if __name__ == "__main__":
    app.run()
