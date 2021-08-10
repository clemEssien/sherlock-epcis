from flask import Flask
import pytest
import json

import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from app import (
    EventView,
    TransformationView,
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
