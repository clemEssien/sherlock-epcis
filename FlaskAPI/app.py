from flask import Flask, jsonify, request, make_response
from flask_classful import FlaskView, route
from neo4j import GraphDatabase
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

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

UPLOAD_FOLDER = "./FlaskAPI/uploads"
ALLOWED_EXTENSIONS = {"json", "xml"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

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


class TransformationView(FlaskView):
    route_base = "/api/transformation"

    @route("/", methods=["POST"])
    def post(self):
        """
        POST an EPCIS event file to add events to graph database
        and return the appropriate FDA CTE

        """
        # Validate User

        # Get Uploaded File
        if "file" not in request.files:
            return make_response(
                {
                    "result": "fail",
                    "message": "Request does not contain a file",
                    "code": 0,
                    "data": {},
                },
                400,
            )
        file = request.files["file"]
        if file.filename == "":
            return make_response(
                {
                    "result": "fail",
                    "message": "No file selected",
                    "code": 0,
                    "data": {},
                },
                400,
            )
        file_ext = file.filename.rsplit(".", 1)[1].lower()
        if file and file_ext in ALLOWED_EXTENSIONS:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        # Create event object and populate it
        if file_ext == "json":
            return make_response(
                {
                    "result": "fail",
                    "message": "JSON Files not currently supported",
                    "code": 0,
                    "data": {},
                },
                501,
            )
            event = epcis_from_json_file(file)
        elif file_ext == "xml":
            try:
                event_list = epcis_from_xml_file(file)
            except:
                return make_response(
                    {
                        "result": "fail",
                        "message": "XML file is not an EPCIS Document",
                        "code": 0,
                        "data": {},
                    },
                    400,
                )
        else:
            return make_response(
                {
                    "result": "fail",
                    "message": "Invalid file type",
                    "code": 0,
                    "data": {},
                },
                400,
            )

        # temporarily just handle first event
        event = event_list[0]

        # Detect CTE from EPCIS event
        cd = CTEDetector()
        try:
            cd.import_yaml_file("epcis_cte_transformation/cte_detect_config.yaml")
        except Exception as e:
            return make_response(
                {
                    "result": "fail",
                    "message": "Invalid CTE detetion configuration file",
                    "code": 0,
                    "data": {},
                },
                500,
            )
        try:
            cte_type = cd.detect_cte(event)
        except Exception as e:
            return make_response(
                {
                    "result": "fail",
                    "message": "Could not detect CTE from EPCIS event",
                    "code": 0,
                    "data": {},
                },
                500,
            )

        # Transform EPCIS event to FDA CTE

        # Store data in Neo4j database

        # Return CTE to user
        return make_response(
            {
                "result": "ok",
                "message": "CTE detected",
                "code": 0,
                "data": {"cte_type": cte_type},
            },
            200,
        )

    @route("/cte", methods=["POST"])
    def finish_cte(self):
        # Edit CTE in database

        # Format CTE as desired document type

        # Return CTE document
        pass


def epcis_from_json_file(file: FileStorage) -> epc.EPCISEvent:
    # verify that file is an epcis document

    # isolate epcis events from file
    pass


def epcis_from_xml_file(file: FileStorage) -> epc.EPCISEvent:
    """Function to return list of EPCISEvent objects from an xml file"""
    epcis_xml = file.read()
    root = ET.fromstring(epcis_xml)
    if "epcis" not in root.tag.lower():
        raise ValueError("XML File is not an EPCIS document")
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
                events.append(event)
    return events


EventView.register(app)
TransformationView.register(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
