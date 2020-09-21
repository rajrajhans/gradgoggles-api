# Tests for /register endpoint
import pytest
from flask import json
from models import User


def test_noemail(app, client):
    """
    WHEN no email is included in POST data
    THEN check for status code 400 and error message
    """
    response = client.post(
        '/register',
        data=json.dumps({}),
        content_type='application/json'
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert data["message"]["email"] == "Email cannot be blank"


def test_nofullName(app, client):
    """Checks for appropriate response when no full name is provided"""

    res = client.post(
        '/register',
        data=json.dumps({'email': 'me@rajrajhans.com',
                         'password': 'testuser'}),
        content_type='application/json'
    )

    data = json.loads(res.get_data(as_text=True))

    assert res.status_code == 400
    assert data["message"]["fullName"] == "Full Name cannot be blank"


def test_userAlreadyExists(app, client):
    """Checks for appropriate response when email is of a existing user in database"""

    res = client.post(
        '/register',
        data=json.dumps({'email': 'me@rajrajhans.com',
                         'password': 'testuser',
                         'fullName': 'Test User'}),
        content_type='application/json'
    )

    data = json.loads(res.get_data(as_text=True))

    assert res.status_code == 200
    assert data["error"] == "User already exists"


def test_newuser(new_user):
    """Tests the create_user() function"""

    assert new_user.email == "testing@gradgoggles.com"
    assert new_user.password != "testpassword"  # makes sure password not stored in plaintext
    assert new_user.name == "Automated Test"
    assert new_user.isVerified is False
    assert new_user.dob is None
    assert new_user.isfeatured == 0


def test_register(register_endpoint):
    """Tests the /register endpoint"""

    data = json.loads(register_endpoint.get_data(as_text=True))

    assert register_endpoint.status_code == 200
    assert data["id"]
    assert data["name"] == "Automated Test"
    assert data["access_token"]
    assert data["photo"] is None
    assert data["is2020"] == False
    assert data["error"] == "none"

    with pytest.raises(KeyError):
        data["password"]
