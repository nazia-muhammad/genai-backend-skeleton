from fastapi.testclient import TestClient


def signup_and_login(client: TestClient, db_session, email: str, password: str):
    # signup
    r = client.post("/api/v1/users", json={"email": email, "password": password})
    assert r.status_code == 200, r.text

    # login (correct route)
    r = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200, r.text
    token = r.json()["access_token"]

    # find org_id for this user
    from app.models import User
    from app.tenancy_models.membership import Membership

    user = db_session.query(User).filter(User.email == email).first()
    assert user is not None

    m = db_session.query(Membership).filter(Membership.user_id == user.id).first()
    assert m is not None

    # return headers for future requests
    return {
        "Authorization": f"Bearer {token}",
        "X-Org-Id": str(m.org_id),
    }


def get_org_id(db_session, user_id: int) -> str:
    from app.tenancy_models.membership import Membership
    m = db_session.query(Membership).filter(Membership.user_id == user_id).first()
    assert m is not None
    return str(m.org_id)


def test_tenant_isolation_notes(client, db_session):
    headers_a = signup_and_login(client, db_session, "a@example.com", "pass1234")
    headers_b = signup_and_login(client, db_session, "b@example.com", "pass1234")

    # Fetch orgs (optional extra safety check)
    from app.models import User

    user_a = db_session.query(User).filter(User.email == "a@example.com").first()
    user_b = db_session.query(User).filter(User.email == "b@example.com").first()
    assert user_a and user_b

    org_a = get_org_id(db_session, user_a.id)
    org_b = get_org_id(db_session, user_b.id)
    assert org_a != org_b

    # user A creates a note in org A (headers include X-Org-Id)
    r = client.post(
        "/api/v1/notes",
        headers=headers_a,
        json={"title": "A1", "content": "hello"},
    )
    assert r.status_code == 200, r.text
    note_id = r.json()["id"]

    # user B tries to read A's note from org B => should be 404 or 403
    r = client.get(
        f"/api/v1/notes/{note_id}",
        headers=headers_b,
    )
    assert r.status_code in (403, 404), r.text


def test_rbac_member_cannot_create_workspace(client, db_session):
    headers_owner = signup_and_login(client, db_session, "owner@example.com", "pass1234")

    from app.models import User
    from app.tenancy_models.membership import Membership

    owner = db_session.query(User).filter(User.email == "owner@example.com").first()
    assert owner is not None

    org_id = get_org_id(db_session, owner.id)

    # create another user
    headers_member = signup_and_login(client, db_session, "member@example.com", "pass1234")
    member = db_session.query(User).filter(User.email == "member@example.com").first()
    assert member is not None

    # add member into OWNER's org as MEMBER (DB shortcut)
    db_session.add(Membership(org_id=org_id, user_id=member.id, role="MEMBER"))
    db_session.commit()

    # MEMBER tries to create workspace => 403
    # must use the org_id of OWNER's org to test RBAC properly:
    headers_member_in_org = {
        "Authorization": headers_member["Authorization"],
        "X-Org-Id": str(org_id),
    }

    r = client.post(
        "/api/v1/workspaces",
        headers=headers_member_in_org,
        params={"name": "ws1"},
    )
    assert r.status_code == 403, r.text
