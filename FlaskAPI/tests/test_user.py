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
from models.company import Company
from services import mongodb_connector, user_services

from flask_mongoengine import MongoEngine
import mongoengine as me
from dotenv import load_dotenv

from app import (
    UserView,
    EventView,
    TransformationView
)

# FIXTURES
@pytest.fixture(scope="module")
def client():
    app = create_app()

    UserView.register(app)
    EventView.register(app)
    TransformationView.register(app)

    client = app.test_client()
    return client

@pytest.fixture(scope="module")
def user_connector():
    return mongodb_connector.MongoDBConnector(User)

@pytest.fixture(scope="module")
def company_connector():
    return mongodb_connector.MongoDBConnector(Company)

@pytest.fixture
def clean(user_connector, company_connector):
    if current_user and current_user.is_authenticated:
        logout_user(current_user)

    user_connector.delete_all()
    company_connector.delete_all()

    user_connector.create_one(
        userId = "1",
        firstName = "first",
        lastName = "last",
        email = "email",
        role = "User",
        passwordHash = generate_password_hash("123"),
        companyId = "456"
    )

@pytest.fixture
def create_admin(user_connector, company_connector):
    user_connector.create_one(
        userId = "2",
        firstName = "ad",
        lastName = "min",
        email = "admin@gmail.com",
        role = "Admin",
        passwordHash = generate_password_hash("456"),
        companyId = "abc123"
    )

    company_connector.create_one(
        companyId = "abc123",
        name = "TestCompany",
        address = "test address"
    )


BASE = "http://127.0.0.1:5000"

# TESTS

@pytest.mark.usefixtures("clean")
def test_create_user_fail(client):
    body = {
        "password": "123",
        "confirmPassword": "123",
        "email": "email",
    }

    response = client.post(BASE + "/api/users/create", data=json.dumps(body))

    assert response.status_code == 400
    assert response.json["error"] == "Email already used"

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
        "password": "nathan123",
        "confirmPassword": "nathan123",
        "email": "nathaniel.moschkin@precise-soft.com",
    }

    response = client.post(BASE + "/api/users/create", data=json.dumps(body))

    user = user_connector.get_one(email="nathaniel.moschkin@precise-soft.com")

    assert response.status_code == 200
    assert response.json["success"] == True
    assert user.email == "nathaniel.moschkin@precise-soft.com"

@pytest.mark.usefixtures("clean")
def test_change_password_wrong_pass(client):
    body_signin = {
        "password": "123",
        "email": "email",
    }

    client.post(BASE + "/api/users/signin", data=json.dumps(body_signin))

    body = {
        "email": "email",
        "oldPassword": "456",
        "newPassword": "abc",
        "confirmNewPassword": "abc"
    }

    response = client.post(BASE + "/api/users/changePassword", data=json.dumps(body))

    assert response.status_code == 400
    assert response.json["error"] == "Incorrect password"

@pytest.mark.usefixtures("clean")
def test_change_password_not_found(client):
    body_signin = {
        "password": "123",
        "email": "email",
    }

    client.post(BASE + "/api/users/signin", data=json.dumps(body_signin))

    body = {
        "email": "bademail",
        "oldPassword": "456",
        "newPassword": "abc",
        "confirmNewPassword": "abc"
    }

    response = client.post(BASE + "/api/users/changePassword", data=json.dumps(body))

    assert response.status_code == 400
    assert response.json["error"] == "User not found"

@pytest.mark.usefixtures("clean")
def test_change_password_mismatch(client):
    body_signin = {
        "password": "123",
        "email": "email",
    }

    client.post(BASE + "/api/users/signin", data=json.dumps(body_signin))

    body = {
        "email": "email",
        "oldPassword": "123",
        "newPassword": "abc",
        "confirmNewPassword": "def"
    }

    response = client.post(BASE + "/api/users/changePassword", data=json.dumps(body))

    assert response.status_code == 400
    assert response.json["error"] == "New passwords do not match"

@pytest.mark.usefixtures("clean")
def test_change_password_success(client, user_connector):
    body_signin = {
        "password": "123",
        "email": "email",
    }

    client.post(BASE + "/api/users/signin", data=json.dumps(body_signin))

    body = {
        "email": "email",
        "oldPassword": "123",
        "newPassword": "456",
        "confirmNewPassword": "456"
    }

    response = client.post(BASE + "/api/users/changePassword", data=json.dumps(body))

    user = user_connector.get_one(email="email")

    assert response.status_code == 200
    assert response.json["success"] == True
    assert check_password_hash(user.passwordHash, "456")

@pytest.mark.usefixtures("clean")
def test_change_email(client, user_connector):
    body_signin = {
        "password": "123",
        "email": "email",
    }

    client.post(BASE + "/api/users/signin", data=json.dumps(body_signin))

    body = {
        "newEmail": "new@gmail.com",
        "confirmNewEmail": "new@gmail.com"
    }

    response = client.post(BASE + "/api/users/changeEmail", data=json.dumps(body))

    user = user_connector.get_one(userId="1")

    assert response.status_code == 200
    assert response.json["success"] == True
    assert user.email == "new@gmail.com"

@pytest.mark.usefixtures("clean")
def test_get_user(client):
    body = {
        "userId": "1"
    }

    response = client.get(BASE + "/api/users/getUser", data=json.dumps(body))

    assert response.status_code == 200
    assert check_password_hash(response.json["passwordHash"], "123")


@pytest.mark.usefixtures("clean", "create_admin")
def test_update_roles_fail(client):
    body_signin = {
        "password": "123",
        "email": "email",
    }

    client.post(BASE + "/api/users/signin", data=json.dumps(body_signin))

    body = {
        "email": "email",
        "roles": ["Originator", "Consumer"]
    }

    response = client.post(BASE + "/api/users/updateRoles", data=json.dumps(body))

    assert response.status_code == 401
    assert response.json["error"] == "Current user is not authorized"

@pytest.mark.usefixtures("clean", "create_admin")
def test_update_roles(client, user_connector):
    body_signin = {
        "password": "456",
        "email": "admin@gmail.com",
    }

    client.post(BASE + "/api/users/signin", data=json.dumps(body_signin))

    body = {
        "email": "email",
        "roles": ["Originator", "Consumer"]
    }

    response = client.post(BASE + "/api/users/updateRoles", data=json.dumps(body))

    user = user_connector.get_one(email="email")

    assert "Originator" in user.supplyChainRoles and "Consumer" in user.supplyChainRoles
    assert response.status_code == 200
    assert response.json["success"] == True

@pytest.mark.usefixtures("clean", "create_admin")
def test_update_company(client, company_connector):
    body_signin = {
        "password": "456",
        "email": "admin@gmail.com",
    }

    client.post(BASE + "/api/users/signin", data=json.dumps(body_signin))

    body = {
        "name": "TestCompany2",
        "address": "other address"
    }

    response = client.post(BASE + "/api/users/updateCompany", data=json.dumps(body))

    company = company_connector.get_one(companyId="abc123")

    assert company.name == "TestCompany2" and company.address == "other address"
    assert response.status_code == 200
    assert response.json["success"] == True

@pytest.mark.usefixtures("clean", "create_admin")
def test_remove_user(client, user_connector):
    body_signin = {
        "password": "456",
        "email": "admin@gmail.com",
    }

    client.post(BASE + "/api/users/signin", data=json.dumps(body_signin))

    body = {
        "email": "email"
    }

    response = client.post(BASE + "/api/users/removeUser", data=json.dumps(body))

    user = user_connector.get_one(email="email")

    assert user.companyId == "" #user is removed from company 456
    assert response.status_code == 200
    assert response.json["success"] == True