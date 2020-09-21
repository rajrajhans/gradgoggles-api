import json


def test_unAuthorizedCreateScrap(client):
    """Tests the /createScrap endpoint without auth header"""

    res = client.post(
        '/createScrap',
        data=json.dumps({'posted_to_id': '21',
                         'content': 'yo its a test scrap'}),
        content_type='application/json'
    )

    data = json.loads(res.get_data(as_text=True))

    assert res.status_code == 401
    assert data["msg"] == "Missing Authorization Header"
