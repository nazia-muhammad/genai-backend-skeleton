from tests.helpers import api

def test_notes_requires_token(client):
    r = client.get(api("/notes?limit=10&offset=0"))
    assert r.status_code == 401
    assert r.json()["detail"] in ["Missing bearer token", "Unauthorized"]
