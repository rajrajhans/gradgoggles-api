import pytest
from models import User
from app import app as flask_app
import json


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def new_user():
    yield User.create_user('testing@gradgoggles.com', 'testpassword', 'Automated Test')
    # teardown
    User.delete_user('testing@gradgoggles.com')


@pytest.fixture
def register_endpoint():
    res = flask_app.test_client().post(
        '/register',
        data=json.dumps({'email': 'testing@gradgoggles.com',
                         'password': 'testpassword',
                         'fullName': 'Automated Test'}),
        content_type='application/json'
    )
    yield res
    User.delete_user('testing@gradgoggles.com')
