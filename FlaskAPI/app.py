from flask import Flask, jsonify, request
from flask_classful import FlaskView, route
from flask_mongoengine import MongoEngine
import mongoengine as me
from models.user import User
from services import user_services
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

# Temporary sandbox database, probably expired
USER = os.getenv('DB_USER')
PASS = os.getenv('DB_PASS')
URI = os.getenv('DB_URI')
driver = GraphDatabase.driver(uri=URI, auth=(USER, PASS))

app = Flask(__name__)
db = MongoEngine(app)
""" app.config['MONGODB_SETTINGS'] = {
    'db': 'project1',
    'username':'webapp',
    'password':'pwd123'
} """


event_types = {
    "ObjectEvent": epc.ObjectEvent,
    "AggregationEvent": epc.AggregationEvent,
    "QuantityEvent": epc.QuantityEvent,
    "TransactionEvent": epc.TransactionEvent,
    "TransformationEvent": epc.TransformationEvent,
}

class UserView(FlaskView):
    route_base = "/api/users"

    @route("/create", methods=["POST"])
    def create_user(self):
        pass

    @route("/signin", methods=["POST"])
    def signin(self):
        pass

    @route("/refresh", methods=["GET"])
    def refresh(self):
        pass

    @route("/change_password", methods=["POST"])
    def change_password(self):
        """
        Changes the password for a given user

        Request Body:
            {
                user_id: str,
                old_password: str,
                new_password: str,
                confirm_new_password: str,
            }

        Error Codes:
            400: Bad request
            404: User not found

        On Success (200):
            {
                success: true
            }
        """
        body_json = json.loads(request.get_data())
        new_password = body_json["new_password"]
        confirm_new_passwords = body_json["confirm_new_passwords"]
        user_id = body_json["user_id"]
        old_password = body_json["old_password"]

        user = User.objects.get_or_404(_id=user_id, message="User not found")
        if (user.password_hash != user_services("something", old_password)):
            return {"error": "Incorrect password"}, 400 
        if (new_password != confirm_new_passwords):
            return {"error": "New passwords do not match"}, 400 

        user.update(password_hash=user_services("something", new_password))
        return {"success": True}


    @route("/get_user", methods=["GET"])
    def get_user(self):
        """
        Gets a single user based off of id

        Request Body:
            {
                user_id: str,
            }

        Error Codes:
            404: User not found

        On Success (200):
            {
                user: User
            }
        """
        body_json = json.loads(request.get_data())
        user_id = body_json["user_id"]
        user = User.objects.get_or_404(_id=user_id)

        return {"user": jsonify(user)}

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

    @route("/delete", methods=["DELETE"]) # TEMPORARY 
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
        epcis_json = json.loads(request.get_data())
        event = event_types[epcis_json["isA"]]()
        ex_json.map_from_epcis(event, epcis_json)
        q = "create (:Event{eventTime: $eventTime, eventTimeZoneOffset: $eventTimeZoneOffset})"
        qmap = {
            "eventTime": str(event.event_time),
            "eventTimeZoneOffset": str(event.event_timezone_offset),
        }
        try:
            with driver.session() as session:
                session.run(q, qmap)
            return {"success": True}
        except Exception as e:
            return {"error": "Error adding events"}, 400

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
                    events.append({     #Event object not json serializable
                        "eventTime": str(event._event_time),
                        "eventTimeZoneOffset": str(event._event_timezone_offset),
                    })

        return {"success": True, "events": events}, 200
        
EventView.register(app)
JSONView.register(app)
XMLView.register(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0")