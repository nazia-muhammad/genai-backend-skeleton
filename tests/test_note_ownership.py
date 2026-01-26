from tests.helpers import api

def test_user_cannot_see_other_users_notes(client):
    # --- user A signup + login ---
    r = client.post(api("/users"), json={"email": "a@test.com", "password": "pass1234"})
    assert r.status_code in (200, 201)

    r = client.post(api("/auth/login"), json={"email": "a@test.com", "password": "pass1234"})
    assert r.status_code == 200
    token_a = r.json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # --- user B signup + login ---
    r = client.post(api("/users"), json={"email": "b@test.com", "password": "pass1234"})
    assert r.status_code in (200, 201)

    r = client.post(api("/auth/login"), json={"email": "b@test.com", "password": "pass1234"})
    assert r.status_code == 200
    token_b = r.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # --- user A creates a note ---
    r = client.post(api("/notes"), json={"title": "A note", "content": "secret"}, headers=headers_a
    )
    assert r.status_code == 200
    note_id = r.json()["id"]

    # --- user B should NOT see it in list ---
    r = client.get(api("/notes"), headers=headers_b)
    assert r.status_code == 200
    ids = [n["id"] for n in r.json()]
    assert note_id not in ids

    # --- user B should NOT get it by id ---
    r = client.get(f"/notes/{note_id}", headers=headers_b)
    assert r.status_code == 404

    # --- user B should NOT update it ---
    r = client.put(
        f"/notes/{note_id}",
        json={"title": "hacked", "content": "hacked"},
        headers=headers_b,
    )
    assert r.status_code == 404

    # --- user B should NOT delete it ---
    r = client.delete(f"/notes/{note_id}", headers=headers_b)
    assert r.status_code == 404
