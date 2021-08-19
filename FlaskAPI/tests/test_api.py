from flask import Flask
import pytest
import json
from io import BytesIO

import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from FlaskAPI.routes.transformation import TransformationView

from app import (
    EventView,
)

# FIXTURES
@pytest.fixture(scope="module")
def client():
    app = Flask(__name__)

    EventView.register(app)
    TransformationView.register(app)

    client = app.test_client()
    return client


BASE = "http://127.0.0.1:5000"

# TESTS
def test_delete(client):
    response = client.delete(BASE + "/api/events/delete")

    assert response.status_code == 200
    assert response.json["success"] == True


def test_transformation_valid_json(client):
    with open("./data/GS1StandardExample1.json", "rb") as f:
        data = {
            "file": (f, "test.json"),
        }
        res = client.post(BASE + "/api/transformation/", data=data)
    assert res.status_code == 200


def test_transformation_valid_xml(client):
    with open("./data/FetaFactory.xml", "rb") as f:
        data = {
            "file": (f, "test.xml"),
        }
        res = client.post(BASE + "/api/transformation/", data=data)
    assert res.status_code == 200


def test_transformation_invalid_json(client):
    with open("./data/test_invalid.json", "rb") as f:
        data = {
            "file": (f, "test.json"),
        }
        res = client.post(BASE + "/api/transformation/", data=data)
    assert res.status_code == 400


def test_transformation_valid_xml(client):
    with open("./data/test_invalid.xml", "rb") as f:
        data = {
            "file": (f, "test.xml"),
        }
        res = client.post(BASE + "/api/transformation/", data=data)
    assert res.status_code == 400


def test_transformation_invalid_file_type(client):
    with open("./data/invalid_file_type.txt", "rb") as f:
        data = {
            "file": (f, "invalid_file_Type.txt"),
        }
        res = client.post(BASE + "/api/transformation/", data=data)
    assert res.status_code == 400


def test_transformation_no_file(client):
    res = client.post(BASE + "/api/transformation/")
    assert res.status_code == 400
