def test_signup_login_and_access_notes(client):
    # 1) signup
    email = "flow@example.com"
    password = "test1234"

    res = client.post("/users", json={"email": email, "password": password})
    assert res.status_code == 200
    body = res.json()
    assert "id" in body
    assert body["email"] == email

    # 2) login -> get token
    res = client.post("/auth/login", json={"email": email, "password": password})
    assert res.status_code == 200
    token = res.json().get("access_token")
    assert token

    headers = {"Authorization": f"Bearer {token}"}

    # 3) notes: should work with token
    res = client.get("/notes?limit=10&offset=0", headers=headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)

    # 4) create note (protected) + verify it shows up
    res = client.post("/notes", json={"title": "t", "content": "c"}, headers=headers)
    assert res.status_code == 200
    created = res.json()
    assert created["title"] == "t"

    res = client.get("/notes?limit=10&offset=0", headers=headers)
    assert res.status_code == 200
    notes = res.json()
    assert any(n["id"] == created["id"] for n in notes)

