from FlaskAPI.routes.graph import Tree
from pymongo.uri_parser import parse_ipv6_literal_host
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
from pymongo.common import EVENTS_QUEUE_FREQUENCY

from FlaskAPI.models.user import User

from FlaskAPI.services import user_services, mongodb_connector
from FlaskAPI.init_app import create_app
from neo4j import GraphDatabase
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from tools.serializer import map_to_json
from FlaskAPI.routes.user import UserView
from FlaskAPI.routes.transformation import TransformationView

from dotenv import load_dotenv
import xml.etree.ElementTree as ET
import json


load_dotenv()
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from flask_cors import CORS

# Temporary sandbox database, probably expired
USER = os.getenv("DB_USER")
PASS = os.getenv("DB_PASS")
URI = os.getenv("DB_URI")
driver = GraphDatabase.driver(uri=URI, auth=(USER, PASS))

app = create_app()


CORS(
    app,
    allow_headers=["Content-Type", "Authorization"],
    origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "https://traceability.sapfonte.net",
        "https://traceability-dev.sapfonte.net",
        "http://traceability.sapfonte.net",
        "http://traceability-dev.sapfonte.net",
    ],
)

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


EventView.register(app)
TransformationView.register(app)
Tree.register(app)
Ocr.register(app)
UserView.register(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
