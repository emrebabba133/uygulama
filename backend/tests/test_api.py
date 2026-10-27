import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest
from fastapi.testclient import TestClient

from app.db import Base, SessionLocal, engine
from app.main import app
from app.models import User
from app.security import hash_password


@pytest.fixture()
def client():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        db.add_all([
            User(email="admin@test.local", full_name="Admin", role="admin",
                 password_hash=hash_password("pw-admin")),
            User(email="cons@test.local", full_name="Cons", role="consultant",
                 password_hash=hash_password("pw-cons")),
        ])
        db.commit()
    return TestClient(app)


def login(c, email, pw):
    r = c.post("/api/v1/auth/login", json={"email": email, "password": pw})
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def make_client_user(org_id, email):
    with SessionLocal() as db:
        db.add(User(email=email, full_name="Client", role="client", organization_id=org_id,
                    password_hash=hash_password("pw-client")))
        db.commit()


def test_unauthenticated_rejected(client):
    assert client.get("/api/v1/client-cases").status_code == 401


def test_bad_login_and_lockout(client):
    for _ in range(5):
        assert client.post("/api/v1/auth/login",
                           json={"email": "cons@test.local", "password": "x"}).status_code == 401
    r = client.post("/api/v1/auth/login", json={"email": "cons@test.local", "password": "pw-cons"})
    assert r.status_code == 429


def test_case_flow_validation_and_audit(client):
    h = login(client, "cons@test.local", "pw-cons")
    org = client.post("/api/v1/organizations", json={"name": "Acme", "country": "TR"}, headers=h).json()
    assert client.post("/api/v1/organizations", json={"name": ""}, headers=h).status_code == 422
    assert client.post("/api/v1/client-cases", json={"title": "T", "organization_id": 999},
                       headers=h).status_code == 422
    case = client.post("/api/v1/client-cases", json={"title": "AD case", "organization_id": org["id"]},
                       headers=h).json()
    assert case["reference"].startswith("CC-")
    r = client.patch(f"/api/v1/client-cases/{case['id']}", json={"status": "Active"}, headers=h)
    assert r.json()["status"] == "Active"
    assert client.patch(f"/api/v1/client-cases/{case['id']}", json={"status": "Bogus"},
                        headers=h).status_code == 422
    task = client.post("/api/v1/tasks", json={"client_case_id": case["id"], "title": "Do"}, headers=h).json()
    assert client.patch(f"/api/v1/tasks/{task['id']}", json={"status": "In Progress"},
                        headers=h).json()["status"] == "In Progress"
    ha = login(client, "admin@test.local", "pw-admin")
    actions = [(e["action"], e["object_type"]) for e in
               client.get("/api/v1/audit-events", headers=ha).json()["items"]]
    assert ("update", "client_case") in actions and ("create", "task") in actions
    assert client.get("/api/v1/audit-events", headers=h).status_code == 403


def test_client_isolation_idor(client):
    h = login(client, "cons@test.local", "pw-cons")
    a = client.post("/api/v1/organizations", json={"name": "A"}, headers=h).json()
    b = client.post("/api/v1/organizations", json={"name": "B"}, headers=h).json()
    ca = client.post("/api/v1/client-cases", json={"title": "A", "organization_id": a["id"]}, headers=h).json()
    cb = client.post("/api/v1/client-cases", json={"title": "B", "organization_id": b["id"]}, headers=h).json()
    make_client_user(a["id"], "ca@test.local")
    hc = login(client, "ca@test.local", "pw-client")
    ids = [c["id"] for c in client.get("/api/v1/client-cases", headers=hc).json()["items"]]
    assert ids == [ca["id"]]
    assert client.get(f"/api/v1/client-cases/{ca['id']}", headers=hc).status_code == 200
    assert client.get(f"/api/v1/client-cases/{cb['id']}", headers=hc).status_code == 404
    # clients cannot write, or see internal tasks / organizations
    assert client.patch(f"/api/v1/client-cases/{ca['id']}", json={"status": "Closed"},
                        headers=hc).status_code == 403
    assert client.get("/api/v1/tasks", headers=hc).status_code == 403
    assert client.get("/api/v1/organizations", headers=hc).status_code == 403


def test_pagination(client):
    h = login(client, "cons@test.local", "pw-cons")
    for i in range(5):
        client.post("/api/v1/organizations", json={"name": f"O{i}"}, headers=h)
    r = client.get("/api/v1/organizations?page=2&size=2", headers=h).json()
    assert r["total"] == 5 and len(r["items"]) == 2
    assert client.get("/api/v1/organizations?size=1000", headers=h).status_code == 422
