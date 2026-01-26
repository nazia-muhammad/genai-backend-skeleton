from tests.helpers import api

def _auth_headers(client, email="fail@test.com", password="pass1234"):
    # signup (ignore if already exists)
    client.post(api("/users"), json={"email": email, "password": password})
    # login
    r = client.post(api("/auth/login"), json={"email": email, "password": password})
    assert r.status_code == 200
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_notes_list_requires_auth(client):
    r = client.get(api("/notes"))
    assert r.status_code == 401


def test_notes_create_requires_auth(client):
    r = client.post(api("/notes"), json={"title": "t", "content": "c"})
    assert r.status_code == 401


def test_notes_update_requires_auth(client):
    r = client.put(api("/notes/1"), json={"title": "t", "content": "c"})
    assert r.status_code == 401


def test_notes_delete_requires_auth(client):
    r = client.delete(api("/notes/1"))
    assert r.status_code == 401


def test_get_missing_note_returns_404(client):
    headers = _auth_headers(client, email="missing@test.com")
    r = client.get(api("/notes/999999"), headers=headers)
    assert r.status_code == 404


def test_pagination_limit_validation(client):
    headers = _auth_headers(client, email="page@test.com")
    # limit must be <= 50 in your route
    r = client.get(api("/notes?limit=999&offset=0"), headers=headers)
    assert r.status_code == 422


def test_pagination_offset_validation(client):
    headers = _auth_headers(client, email="page2@test.com")
    # offset must be >= 0 in your route
    r = client.get(api("/notes?limit=10&offset=-1"), headers=headers)
    assert r.status_code == 422
