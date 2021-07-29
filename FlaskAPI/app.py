from flask import Flask, jsonify, request, make_response
from flask_classful import FlaskView, route
from neo4j import GraphDatabase

from dotenv import load_dotenv
import os, sys
import xml.etree.ElementTree as ET
import json

load_dotenv()
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import JSONDeserialization.epcis_event as epc
import JSONDeserialization.extract_gis_from_json as ex_json
import XMLDeserialization.extract_gis_from_xml as ex_xml
from epcis_cte_transformation.cte_detector import CTEDetector

# Temporary sandbox database, probably expired
USER = os.getenv("DB_USER")
PASS = os.getenv("DB_PASS")
URI = os.getenv("DB_URI")
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
    route_base = "/api/events"

    @route("/", methods=["GET"])
    def get_all(self):
        """
        Gets all EPCIS event data

        Error Codes:
            400: Bad request

        On Success (200):
            {
                events: EPCISEvent[]
            }
        """
        try:
            with driver.session() as session:
                q = "match (n:Event) return n"
                results = session.run(q).data()
            return {"events": results}, 200
        except Exception as e:
            return {"error": "Error getting events"}, 400

    @route("/delete", methods=["DELETE"])  # TEMPORARY
    def delete(self):
        """
        Deletes all EPCIS event data

        Error Codes:
            400: Bad request

        On Success (200):
            {
                success: true
            }
        """
        try:
            with driver.session() as session:
                q = "match (n:Event) delete n"
                session.run(q).data()
            return {"success": True}
        except Exception as e:
            return {"error": "Error deleting events"}, 400


class JSONView(FlaskView):
    route_base = "/api/json"

    @route("/", methods=["POST"])
    def post(self):
        """
        POST an JSON EPCIS event to add to db

        Content Type: application/json

        Request Body:
            {
                isA: str, *event type
                eventTime: str,
                eventTimeZoneOffset: str,
                epcList: str[],
                action: str,
                bizStep: str,
                disposition: str,
                readPoint: {id: str},
                bizTransactionList: [
                    {
                        type: str,
                        bizTransaction: str,
                    }
                ],
            }

        Error Codes:
            400: Bad request

        On Success (200):
            {
                success: true
            }

        """
        # Validate User

        # Validate request body is EPCIS Event

        # Create event object and populate it
        epcis_json = json.loads(request.get_data())
        event = event_types[epcis_json["isA"]]()
        ex_json.map_from_epcis(event, epcis_json)

        # Detect CTE from EPCIS event
        cd = CTEDetector()
        cd.import_yaml_file("epcis_cte_transformation/cte_detect_config.yaml")
        cte_type = cd.detect_cte(event)

        # Transform EPCIS event to FDA CTE

        # Store data in Neo4j database
        q = "create (:Event{eventTime: $eventTime, eventTimeZoneOffset: $eventTimeZoneOffset})"
        qmap = {
            "eventTime": str(event.event_time),
            "eventTimeZoneOffset": str(event.event_timezone_offset),
        }
        try:
            with driver.session() as session:
                session.run(q, qmap)
        except Exception as e:
            return make_response({"error": "Error adding events"}, 400)
        # Return CTE to user

    @route("/cte", methods=["POST"])
    def finish_cte(self):
        # Edit CTE in database

        # Format CTE as desired document type

        # Return CTE document
        pass


class XMLView(FlaskView):
    route_base = "/api/xml"

    @route("/", methods=["POST"])
    def post(self):
        """
        Posts XML EPCIS events to add to db

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
                        event = event_types[event.tag]()
                    except Exception:
                        event_from_xml = ex_xml.find_event_from_xml(event, event_types)
                        event = event_types[event_from_xml]
                    xml_dict = ex_xml.map_to_epcis_dict(xml_doc)
                    ex_xml.map_from_epcis(event, xml_dict)
                    q = "create (:Event{eventTime: $eventTime, eventTimeZoneOffset: $eventTimeZoneOffset})"
                    qmap = {
                        "eventTime": str(event.event_time),
                        "eventTimeZoneOffset": str(event.event_timezone_offset),
                    }
                    try:
                        with driver.session() as session:
                            session.run(q, qmap)
                    except Exception as e:
                        return {"error": "Error adding events"}, 400
                    events.append(
                        {  # Event object not json serializable
                            "eventTime": str(event._event_time),
                            "eventTimeZoneOffset": str(event._event_timezone_offset),
                        }
                    )

        return {"success": True, "events": events}, 200


EventView.register(app)
JSONView.register(app)
XMLView.register(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
