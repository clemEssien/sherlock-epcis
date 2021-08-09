from flask import Flask, jsonify, request
import uuid
from flask_classful import FlaskView, route
from flask_mongoengine import MongoEngine
import mongoengine as me
from models.user import User
from services import user_services, mongodb_connector
from init_app import create_app
from neo4j import GraphDatabase

from routes.user import UserView

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

app = create_app()

event_types = {
    "ObjectEvent": epc.ObjectEvent,
    "AggregationEvent": epc.AggregationEvent,
    "QuantityEvent": epc.QuantityEvent,
    "TransactionEvent": epc.TransactionEvent,
    "TransformationEvent": epc.TransformationEvent,
}

import os
from flask import  flash, redirect, url_for, send_from_directory, make_response
from werkzeug.utils import secure_filename
import json

UPLOAD_FOLDER = '/var/src/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'json', 'csv', 'xlsx', 'xml'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

class Ocr(FlaskView):
    route_base = "/api/ocr"

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
               
    @route("/download_file/<name>", methods=["GET"])
    def download_file(self, name: str):
        if (os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], name))):
            return send_from_directory(
                app.config['UPLOAD_FOLDER'], name, as_attachment=True
            )        
        else:
            return make_response(json.dumps({ "result": "fail", "message": "File Not Found" }), 404)
        
    @route("/upload_file", methods=["GET", "POST"])
    def upload_file(self):

        DOWNLOAD_URL = request.host_url + "api/ocr/download_file/"

        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                return make_response(json.dumps({ "result": "fail", "message": "No file included" }), 400)
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                return make_response(json.dumps({ "result": "fail", "message": "No selected file" }), 400)
            if file and self.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
                return make_response(json.dumps({ "result": "ok", "message": "File uploaded successfully.", "url": DOWNLOAD_URL + filename}), 200)
        
        return make_response(json.dumps({ "result": "fail", "message": "Invalid method" }), 400)
    
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

UserView.register(app)   
EventView.register(app)
JSONView.register(app)
XMLView.register(app)
Ocr.register(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0")