from resources import email_verification as ev
import json


def test_emailverification():
    """Tests the generate_confirmation_token and confirm_token with correct values"""
    token = ev.generate_confirmation_token('testing@gradgoggles.com')
    isTokenCorrect = ev.confirm_token(token)

    assert isTokenCorrect == 'testing@gradgoggles.com'


def test_incorrect_emailverification():
    """Tests the generate_confirmation_token and confirm_token with incorrect values"""
    token = ev.generate_confirmation_token('testing@gradgoggles.com')
    isTokenCorrect = ev.confirm_token(token + "dummy haha")

    assert isTokenCorrect is False


def test_forgetpassError(client):
    """Tests the /forgotPasswordSendMail endpoint with invalid input"""

    res = client.post(
        '/forgotPasswordSendMail',
        data=json.dumps({'email': 'testing@gradgoggles.com'}),
        content_type='application/json'
    )

    data = json.loads(res.get_data(as_text=True))

    assert res.status_code == 200
    assert data["msg"] == "email does not exist, please sign up"


def test_forgetpass(client, register_endpoint):
    """Tests the /forgotPasswordSendMail endpoint"""

    res = client.post(
        '/forgotPasswordSendMail',
        data=json.dumps({'email': 'testing@gradgoggles.com'}),
        content_type='application/json'
    )

    data = json.loads(res.get_data(as_text=True))

    assert register_endpoint.status_code == 200
    assert res.status_code == 200
    assert data["msg"] == "email sent"
