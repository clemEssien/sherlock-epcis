from flask import Flask
import pytest
import json

import os , sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from app import (
    EventView,
    JSONView,
    XMLView
)

# FIXTURES
@pytest.fixture(scope="module")
def client():
    app = Flask(__name__)

    EventView.register(app)
    JSONView.register(app)
    XMLView.register(app)

    client = app.test_client()
    return client

BASE = "http://127.0.0.1:5000"

# TESTS
def test_json_post(client):
    body = {
        "isA": "ObjectEvent",
        "eventTime": "2005-04-02T20:33:31.116-06:00",
        "eventTimeZoneOffset": "-06:00",
        "epcList": [
            "urn:epc:id:sgtin:0614141.107346.2017",
            "urn:epc:id:sgtin:0614141.107346.2018",
        ],
        "action": "OBSERVE",
        "bizStep": "urn:epcglobal:cbv:bizstep:shipping",
        "disposition": "urn:epcglobal:cbv:disp:in_transit",
        "readPoint": {"id": "urn:epc:id:sgln:0614141.07346.1234"},
        "bizTransactionList": [
            {
                "type": "urn:epcglobal:cbv:btt:po",
                "bizTransaction": "http://transaction.acme.com/po/12345678",
            }
        ],
    }

    response = client.post(BASE + "/api/json/", data=json.dumps(body))

    assert response.status_code == 200
    assert response.json["success"] == True



