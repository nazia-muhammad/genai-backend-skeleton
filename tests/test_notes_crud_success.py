from tests.helpers import api

def test_notes_crud_success_flow(client):
    # signup
    r = client.post(api("/users"), json={"email": "crud@test.com", "password": "pass1234"})
    assert r.status_code in (200, 201)

    # login
    r = client.post(api("/auth/login"), json={"email": "crud@test.com", "password": "pass1234"}
    )
    assert r.status_code == 200
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # create note
    r = client.post(api("/notes"), json={"title": "t1", "content": "c1"}, headers=headers)
    assert r.status_code == 200
    note = r.json()
    note_id = note["id"]
    assert note["title"] == "t1"
    assert note["content"] == "c1"

    # list notes (should include created note)
    r = client.get(api("/notes?limit=10&offset=0"), headers=headers)
    assert r.status_code == 200
    ids = [n["id"] for n in r.json()]
    assert note_id in ids

    # get note by id
    r = client.get(api(f"/notes/{note_id}"), headers=headers)
    assert r.status_code == 200
    assert r.json()["id"] == note_id

    # update note
    r = client.put(
    api(f"/notes/{note_id}"),
    json={"title": "t2", "content": "c2"},
    headers=headers,
)
    assert r.status_code == 200
    assert r.json()["title"] == "t2"
    assert r.json()["content"] == "c2"

    # delete note
    r = client.delete(api(f"/notes/{note_id}"), headers=headers)
    assert r.json()["deleted"] is True

    # get after delete -> 404
    r = client.get(f"/notes/{note_id}", headers=headers)
    assert r.status_code == 404
