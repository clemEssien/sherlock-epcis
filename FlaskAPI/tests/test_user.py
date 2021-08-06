import os , sys

from werkzeug.security import check_password_hash, generate_password_hash
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from flask import Flask
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
import pytest
import json
from init_app import create_app
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
    app = create_app()

    UserView.register(app)
    EventView.register(app)
    JSONView.register(app)
    XMLView.register(app)

    client = app.test_client()
    return client

@pytest.fixture(scope="module")
def user_connector():
    return mongodb_connector.MongoDBConnector(User)

@pytest.fixture
def clean(user_connector):
    if current_user and current_user.is_authenticated:
        logout_user(current_user)

    user_connector.delete_all()

    user_connector.create_one(
        user_id = "1",
        first_name = "first",
        last_name = "last",
        email = "email",
        role = "User",
        password_hash = generate_password_hash("123"), #hash for "123"
        company_id = "456"
    )

BASE = "http://127.0.0.1:5000"

# TESTS

@pytest.mark.usefixtures("clean")
def test_signin(client):
    body = {
        "password": "123",
        "email": "email",
    }

    response = client.post(BASE + "/api/users/signin", data=json.dumps(body))

    assert response.status_code == 200
    assert response.json["success"] == True

@pytest.mark.usefixtures("clean")
def test_signout_fail(client):

    response = client.post(BASE + "/api/users/signout")

    assert response.status_code == 401
    assert response.json["error"] == "Not logged in"

@pytest.mark.usefixtures("clean")
def test_profile_fail(client):

    response = client.get(BASE + "/api/users/profile")

    assert response.status_code == 401
    assert response.json["error"] == "Not logged in"

@pytest.mark.usefixtures("clean")
def test_profile(client):
    body = {
        "password": "123",
        "email": "email",
    }

    response = client.post(BASE + "/api/users/signin", data=json.dumps(body))

    response_profile = client.get(BASE + "/api/users/profile")

    assert response.status_code == 200
    assert response_profile.json["email"] == "email"

@pytest.mark.usefixtures("clean")
def test_create(client, user_connector):
    body = {
        "first_name": "Nathaniel",
        "last_name": "Moschkin",
        "password": "nathan123",
        "email": "nathaniel.moschkin@precise-soft.com",
    }

    response = client.post(BASE + "/api/users/create", data=json.dumps(body))

    user = user_connector.get_one(email="nathaniel.moschkin@precise-soft.com")

    assert response.status_code == 200
    assert response.json["success"] == True
    assert user.first_name == "Nathaniel"

@pytest.mark.usefixtures("clean")
def test_change_password_wrong_pass(client):
    body = {
        "email": "email",
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
        "email": "bademail",
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
        "email": "email",
        "old_password": "123",
        "new_password": "abc",
        "confirm_new_password": "def"
    }

    response = client.post(BASE + "/api/users/change_password", data=json.dumps(body))

    assert response.status_code == 400
    assert response.json["error"] == "New passwords do not match"

@pytest.mark.usefixtures("clean")
def test_change_password_success(client, user_connector):
    body = {
        "email": "email",
        "old_password": "123",
        "new_password": "456",
        "confirm_new_password": "456"
    }

    response = client.post(BASE + "/api/users/change_password", data=json.dumps(body))

    user = user_connector.get_one(email="email")

    assert response.status_code == 200
    assert response.json["success"] == True
    assert check_password_hash(user.password_hash, "456")

@pytest.mark.usefixtures("clean")
def test_change_email(client, user_connector):
    body = {
        "user_id": "1",
        "password": "123",
        "new_email": "new@gmail.com",
        "confirm_new_email": "new@gmail.com"
    }

    response = client.post(BASE + "/api/users/change_email", data=json.dumps(body))

    user = user_connector.get_one(user_id="1")

    assert response.status_code == 200
    assert response.json["success"] == True
    assert user.email == "new@gmail.com"

@pytest.mark.usefixtures("clean")
def test_get_user(client):
    body = {
        "user_id": "1"
    }

    response = client.get(BASE + "/api/users/get_user", data=json.dumps(body))

    assert response.status_code == 200
    assert check_password_hash(response.json["password_hash"], "123")
