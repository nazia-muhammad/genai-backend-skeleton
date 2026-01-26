from tests.helpers import api

def test_create_note_requires_token(client):
    # POST /notes should be protected
    res = client.post(api("/notes"), json={"title": "t", "content": "c"})
    assert res.status_code == 401
    assert res.json()["detail"] == "Missing bearer token"


def test_create_note_with_token_works(client):
    # 1) signup (or ignore if already exists)
    email = "test@example.com"
    password = "test1234"

    signup = client.post(api("/users"), json={"email": email, "password": password})
    assert signup.status_code in (200, 409)

    # 2) login -> get token
    login = client.post(api("/auth/login"), json={"email": email, "password": password})
    assert login.status_code == 200
    token = login.json()["access_token"]
    assert token

    headers = {"Authorization": f"Bearer {token}"}

    # 3) create note with token
    res = client.post(api("/notes"), json={"title": "Hello", "content": "World"}, headers=headers
    )
    assert res.status_code == 200
    body = res.json()
    assert body["title"] == "Hello"
    assert body["content"] == "World"
    assert "id" in body


def test_update_note_requires_token(client):
    res = client.put(api("/notes/1"), json={"title": "t", "content": "c"})
    assert res.status_code == 401


def test_delete_note_requires_token(client):
    res = client.delete(api("/notes/1"))
    assert res.status_code == 401
