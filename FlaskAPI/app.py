import os, sys

import json
from flask import (
    Flask,
    jsonify,
    request,
    make_response,
    flash,
    redirect,
    url_for,
    send_from_directory,
)
import uuid
from flask_classful import FlaskView, route
from flask_mongoengine import MongoEngine
import mongoengine as me

from .models.user import User

from services import user_services, mongodb_connector
from init_app import create_app
from neo4j import GraphDatabase
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from routes.user import UserView

from dotenv import load_dotenv
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

app = create_app()

event_types = {
    "ObjectEvent": epc.ObjectEvent,
    "AggregationEvent": epc.AggregationEvent,
    "QuantityEvent": epc.QuantityEvent,
    "TransactionEvent": epc.TransactionEvent,
    "TransformationEvent": epc.TransformationEvent,
}

UPLOAD_FOLDER = "/var/src/uploads"
ALLOWED_EXTENSIONS = {
    "txt",
    "pdf",
    "png",
    "jpg",
    "jpeg",
    "gif",
    "json",
    "csv",
    "xlsx",
    "xml",
}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


class Ocr(FlaskView):
    route_base = "/api/ocr"

    def allowed_file(self, filename):
        return (
            "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
        )

    @route("/download_file/<name>", methods=["GET"])
    def download_file(self, name: str):
        if os.path.exists(os.path.join(app.config["UPLOAD_FOLDER"], name)):
            return send_from_directory(
                app.config["UPLOAD_FOLDER"], name, as_attachment=True
            )
        else:
            return make_response(
                json.dumps({"result": "fail", "message": "File Not Found"}), 404
            )

    @route("/upload_file", methods=["GET", "POST"])
    def upload_file(self):

        DOWNLOAD_URL = request.host_url + "api/ocr/download_file/"

        if request.method == "POST":
            # check if the post request has the file part
            if "file" not in request.files:
                return make_response(
                    json.dumps({"result": "fail", "message": "No file included"}), 400
                )
            file = request.files["file"]
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == "":
                return make_response(
                    json.dumps({"result": "fail", "message": "No selected file"}), 400
                )
            if file and self.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

                return make_response(
                    json.dumps(
                        {
                            "result": "ok",
                            "message": "File uploaded successfully.",
                            "url": DOWNLOAD_URL + filename,
                        }
                    ),
                    200,
                )

        return make_response(
            json.dumps({"result": "fail", "message": "Invalid method"}), 400
        )


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
        # Create event objects and populate them
        if file_ext == "json":
            try:
                event_list = epcis_from_json_file(file)
            except:
                return make_response(
                    {
                        "result": "fail",
                        "message": "Couldn't extract EPCIS events from JSON File",
                        "code": 0,
                        "data": {},
                    },
                    400,
                )
        elif file_ext == "xml":
            try:
                event_list = epcis_from_xml_file(file)
            except:
                return make_response(
                    {
                        "result": "fail",
                        "message": "Couldn't extract EPCIS events from XML File",
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
        cte_list = []
        for event in event_list:

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
            if cte_type == "creation":
                from epcis_cte_transformation.creation_cte import CreationCTE

                cte = CreationCTE.new_from_epcis(CreationCTE, event)
            elif cte_type == "growing":
                # from epcis_cte_transformation.growing_cte import GrowingCTE
                # cte = GrowingCTE.new_from_epcis(GrowingCTE, event)
                pass
            elif cte_type == "transformation":
                from epcis_cte_transformation.transformation_cte import (
                    TransformationCTE,
                )

                cte = TransformationCTE.new_from_epcis(TransformationCTE, event)
            elif cte_type == "shipping":
                from epcis_cte_transformation.shipping_cte import ShippingCTE

                cte = ShippingCTE.new_from_epcis(ShippingCTE, event)
            elif cte_type == "receiving":
                from epcis_cte_transformation.receiving_cte import ReceivingCTE

                cte = ShippingCTE.new_from_epcis(ShippingCTE, event)
            else:
                # invalid cte type
                raise ValueError("CTE is an invalid type")

            # Store data in Neo4j database

            cte_list.append(cte)
        # Return CTEs to user
        return make_response(
            {
                "result": "ok",
                "message": "CTE detected",
                "code": 0,
                "CTEs": cte_list,
            },
            200,
        )

    @route("/cte", methods=["POST"])
    def finish_cte(self):
        # Edit CTE in database

        # Format CTE as desired document type

        # Return CTE document
        pass


def epcis_from_json_file(file: FileStorage) -> "list[epc.EPCISEvent]":
    """Function to return a list of EPCISEvent objects from a JSON file"""
    with open(
        os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(file.filename))
    ) as f:
        json_dict = json.load(f)
    # document follows proposed EPCIS2.0 JSON bindings
    if json_dict["isA"].lower() == "epcisdocument":
        json_event_list = json_dict["epcisBody"]["eventList"]
    # document does not follow proposed EPCIS2.0 JSON bindings
    else:
        pass
    # populate EPCISEvent object from JSON events
    for e in json_event_list:
        print("event:", e)
    event_list = []
    for json_event in json_event_list:
        print("for json_Event in json_event_list")
        event = event_types[json_event["isA"]]()
        print("event object created from event_types")
        try:
            ex_json.map_from_epcis(event, json_event)
        except Exception as e:
            print(e)
        print("event mapped to object")
        event_list.append(event)
        print("event appended")

    return event_list


def epcis_from_xml_file(file: FileStorage) -> "list[epc.EPCISEvent]":
    """Function to return list of EPCISEvent objects from an XML file"""
    try:
        tree = ET.parse(
            os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(file.filename))
        )

    except:
        raise ValueError("Couldn't parse XML file")
    root = tree.getroot()
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
Ocr.register(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
