from epcis_cte_transformation.cte import split_results
from epcis_cte_transformation.location_master import LocationMaster
from epcis_cte_transformation.ftl_food import FTLFood
import os, sys

import json
from flask import make_response, request
import uuid
from flask_classful import FlaskView, route

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from tools.serializer import map_to_json

from dotenv import load_dotenv
import json


load_dotenv()
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from JSONDeserialization.epcis_event import (
    EPCISEvent,
    ObjectEvent,
    AggregationEvent,
    QuantityEvent,
    TransactionEvent,
    TransformationEvent,
)

from JSONDeserialization.extract_gis_from_json import map_from_epcis
from XMLDeserialization.DeserializeXMLRecursive import parse_xml
from epcis_cte_transformation.cte_detector import CTEDetector

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

event_types = {
    "ObjectEvent": ObjectEvent,
    "AggregationEvent": AggregationEvent,
    "QuantityEvent": QuantityEvent,
    "TransactionEvent": TransactionEvent,
    "TransformationEvent": TransformationEvent,
}


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
            file.save(os.path.join(UPLOAD_FOLDER, filename))
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
        ftl_list = []
        loc_list = []

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

                cte = CreationCTE.new_from_epcis(event)
            elif cte_type == "growing":
                # from epcis_cte_transformation.growing_cte import GrowingCTE
                # cte = GrowingCTE.new_from_epcis(event)
                cte = None
                pass
            elif cte_type == "transformation":
                from epcis_cte_transformation.transformation_cte import (
                    TransformationCTE,
                )

                cte = TransformationCTE.new_from_epcis(event)
            elif cte_type == "shipping":
                from epcis_cte_transformation.shipping_cte import ShippingCTE

                cte = ShippingCTE.new_from_epcis(event)
            elif cte_type == "receiving":
                from epcis_cte_transformation.receiving_cte import ReceivingCTE

                cte = ReceivingCTE.new_from_epcis(event)

            else:
                # invalid cte type
                return "CTE is an invalid type", 400

            # Store data in Neo4j database
            try:
                store_event(event)
            except:
                return make_response(
                    {
                        "result": "fail",
                        "message": "Could not store event in database",
                        "code": 0,
                        "data": {},
                    },
                    500,
                )
            # Handle FTL and Location Master
            output_types = {}

            if cte:
                data = map_to_json(cte)
                data["cteType"] = cte_type

                ftl = FTLFood.new_from_cte(cte)
                location = LocationMaster.new_from_cte(cte)

                # data['funky'] = [ "item1", "item2", "item3" ]
                # data['alienation'] = [ "lambda", "delta" ]
                split = split_results(data)
                for item in split:
                    cte_list.append(item)

                split = split_results(map_to_json(ftl))
                for item in split:
                    ftl_list.append(item)

                split = split_results(map_to_json(location))
                for item in split:
                    loc_list.append(item)

                for cte in cte_list:
                    ctetype = cte["cteType"]

                    if not ctetype in output_types.keys():
                        output_types[ctetype] = [cte]
                    else:
                        output_types[ctetype].append(cte)

        # Return CTEs to user
        return make_response(
            {
                "result": "ok",
                "message": "CTE detected",
                "code": 0,
                "CTEs": output_types,
                "FTLs": ftl_list,
                "Locations": loc_list,
            },
            200,
        )

    @route("/cte", methods=["POST"])
    def finish_cte(self):
        # Edit CTE in database

        # Format CTE as desired document type

        # Return CTE document
        pass


def epcis_from_json_file(file: FileStorage) -> "list[EPCISEvent]":
    """Function to return a list of EPCISEvent objects from a JSON file"""
    with open(os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))) as f:
        json_dict = json.load(f)
    # document follows proposed EPCIS2.0 JSON bindings
    try:
        json_event_list = json_dict["epcisBody"]["eventList"]
    # document does not follow proposed EPCIS2.0 JSON bindings
    except:
        raise ValueError("File does not follow proposed EPCIS2.0 JSON bindings")
    # populate EPCISEvent object from JSON events
    event_list = []
    for json_event in json_event_list:
        event = event_types[json_event["isA"]]()
        try:
            map_from_epcis(event, json_event)
        except Exception as e:
            print("map_from_epcis error:", e)
        event_list.append(event)

    return event_list


def epcis_from_xml_file(file: FileStorage) -> "list[EPCISEvent]":
    """Function to return list of EPCISEvent objects from an XML file"""
    event_dicts = parse_xml(os.path.join(UPLOAD_FOLDER, secure_filename(file.filename)))
    event_list = []
    for event_dict in event_dicts:
        event = event_types[event_dict["isA"]]()
        try:
            map_from_epcis(event, event_dict)
        except Exception as e:
            print("map_from_epcis error:", e)
        event_list.append(event)
    return event_list


def store_event(event: EPCISEvent):
    """Stores a given EPCIS Event in the Neo4j database"""
    pass
