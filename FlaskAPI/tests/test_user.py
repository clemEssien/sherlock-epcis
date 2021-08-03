import os , sys

from werkzeug.security import generate_password_hash
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from flask import Flask
import pytest
import json
from models.user import User
from services import mongodb_connector, user_services

from flask_mongoengine import MongoEngine
import mongoengine as me
from dotenv import load_dotenv

from app import (
    UserView,
    EventView,
    JSONView,
    XMLView
)

# FIXTURES
@pytest.fixture(scope="module")
def client():
    app = Flask(__name__)
    app.config['MONGODB_SETTINGS'] = {
        "host": os.getenv('MONGODB_HOST')
    }
    db = MongoEngine(app)

    UserView.register(app)
    EventView.register(app)
    JSONView.register(app)
    XMLView.register(app)

    client = app.test_client()
    return client

@pytest.fixture
def clean():
    user_connector = mongodb_connector.MongoDBConnector(User)
    user_connector.delete_all()

    user_connector.create_one(
        user_id = "1",
        first_name = "first",
        last_name = "last",
        email = "email",
        role = "User",
        password_hash = "0B2CC2C0B8A1ACDD81DF59FBA71D255366254B6D1850E7BE9435959303D9D1EB", #hash for "123"
        company_id = "456"
    )

BASE = "http://127.0.0.1:5000"

# TESTS
@pytest.mark.usefixtures("clean")
def test_change_password_wrong_pass(client):
    body = {
        "user_id": "1",
        "old_password": "456",
        "new_password": "abc",
        "confirm_new_password": "abc"
    }

    response = client.post(BASE + "/api/users/change_password", data=json.dumps(body))

    assert response.status_code == 400
    assert response.json["error"] == "Incorrect password"

@pytest.mark.usefixtures("clean")
def test_change_password_not_found(client):
    body = {
        "user_id": "2",
        "old_password": "456",
        "new_password": "abc",
        "confirm_new_password": "abc"
    }

    response = client.post(BASE + "/api/users/change_password", data=json.dumps(body))

    assert response.status_code == 400
    assert response.json["error"] == "User not found"

@pytest.mark.usefixtures("clean")
def test_change_password_mismatch(client):
    body = {
        "user_id": "1",
        "old_password": "123",
        "new_password": "abc",
        "confirm_new_password": "def"
    }

    response = client.post(BASE + "/api/users/change_password", data=json.dumps(body))

    assert response.status_code == 400
    assert response.json["error"] == "New passwords do not match"

@pytest.mark.usefixtures("clean")
def test_change_password_success(client):
    body = {
        "user_id": "1",
        "old_password": "123",
        "new_password": "456",
        "confirm_new_password": "456"
    }

    response = client.post(BASE + "/api/users/change_password", data=json.dumps(body))

    assert response.status_code == 200
    assert response.json["success"] == True

@pytest.mark.usefixtures("clean")
def test_change_email(client):
    body = {
        "user_id": "1",
        "password": "123",
        "new_email": "new@gmail.com",
        "confirm_new_email": "new@gmail.com"
    }

    response = client.post(BASE + "/api/users/change_email", data=json.dumps(body))

    body_other = {
        "user_id": "1"
    }

    response_other = client.get(BASE + "/api/users/get_user", data=json.dumps(body_other))

    assert response.status_code == 200
    assert response.json["success"] == True
    assert response_other.json["email"] == "new@gmail.com"

@pytest.mark.usefixtures("clean")
def test_get_user(client):
    body = {
        "user_id": "1"
    }

    response = client.get(BASE + "/api/users/get_user", data=json.dumps(body))

    assert response.status_code == 200
    assert response.json["password_hash"] == generate_password_hash("123")
