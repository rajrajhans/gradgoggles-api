import json


def test_incorrectlogin(client, register_endpoint):
    """Tests the /login endpoint with incorrect inputs"""

    res = client.post(
        '/login',
        data=json.dumps({'email': 'testing@gradgoggles.com',
                         'password': 'testpassword1234123'}),
        content_type='application/json'
    )

    data = json.loads(res.get_data(as_text=True))

    assert register_endpoint.status_code == 200
    assert data["error"] == "Email or password does not match"


def test_correctlogin(client, register_endpoint):
    """Tests the /login endpoint"""

    res = client.post(
        '/login',
        data=json.dumps({'email': 'testing@gradgoggles.com',
                         'password': 'testpassword'}),
        content_type='application/json'
    )

    data = json.loads(res.get_data(as_text=True))

    assert register_endpoint.status_code == 200
    assert data["id"]
    assert data["name"] == "Automated Test"
    assert data["access_token"]
    assert data["photo"] is None
    assert data["isVerified"] is False
    assert data["is2020"] is False
    assert data["error"] == "none"
