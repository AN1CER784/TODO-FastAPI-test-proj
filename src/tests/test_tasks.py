import asyncio
import uuid
from typing import Dict

import pytest
from fastapi.testclient import TestClient
from tortoise import Tortoise

from src.main import app
from src.models import Task


@pytest.fixture(scope="session", autouse=True)
def init_db():
    db_url = "sqlite://:memory:"
    loop = asyncio.get_event_loop()

    loop.run_until_complete(
        Tortoise.init(
            db_url=db_url,
            modules={"models": ["src.models"]},
        )
    )
    loop.run_until_complete(Tortoise.generate_schemas())

    yield
    loop.run_until_complete(Tortoise.close_connections())


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


def create_payload(title: str = "Task", description: str | None = None, status: str | None = None) -> Dict:
    d = {"title": title}
    if description is not None:
        d["description"] = description
    if status is not None:
        d["status"] = status
    return d


def parse_uuid_like(s: str) -> uuid.UUID:
    return uuid.UUID(s)


def test_create_task_success(client):
    payload = create_payload("My first task", "desc", None)
    r = client.post("/tasks/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "My first task"
    assert data["description"] == "desc"
    assert "id" in data
    parse_uuid_like(data["id"])


def test_create_task_invalid_status_api(client):
    payload = create_payload("Bad status task", "x", "not_a_status")
    r = client.post("/tasks/", json=payload)
    assert r.status_code == 422


def test_model_level_validation_rejects_invalid_status():
    bad_status = "i_am_wrong_status_value"
    loop = asyncio.get_event_loop()
    with pytest.raises(ValueError):
        loop.run_until_complete(Task.create(title="m", status=bad_status))


def test_get_nonexistent_task_returns_404(client):
    random_uuid = str(uuid.uuid4())
    r = client.get(f"/tasks/{random_uuid}")
    assert r.status_code == 404


def test_list_pagination(client):
    ids = []
    for i in range(5):
        r = client.post("/tasks/", json=create_payload(f"T{i}", f"d{i}"))
        assert r.status_code == 201
        ids.append(r.json()["id"])

    r = client.get("/tasks/?skip=2&limit=2")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) == 2
    for item in data:
        assert item["id"] in ids


def test_update_task_success(client):
    r = client.post("/tasks/", json=create_payload("To update", "desc"))
    tid = r.json()["id"]

    update_body = {"title": "Updated", "status": "in_progress"}
    r2 = client.put(f"/tasks/{tid}", json=update_body)
    assert r2.status_code == 200
    data = r2.json()
    assert data["title"] == "Updated"
    assert data["status"] == "in_progress"


def test_update_task_invalid_status_api(client):
    r = client.post("/tasks/", json=create_payload("To bad update"))
    tid = r.json()["id"]

    r2 = client.put(f"/tasks/{tid}", json={"status": "lol_no"})
    assert r2.status_code == 422


def test_delete_task(client):
    r = client.post("/tasks/", json=create_payload("To delete"))
    tid = r.json()["id"]

    r2 = client.delete(f"/tasks/{tid}")
    assert r2.status_code == 204

    r3 = client.get(f"/tasks/{tid}")
    assert r3.status_code == 404


def test_multiple_creates_and_uniqueness(client):
    ids = set()
    for i in range(10):
        r = client.post("/tasks/", json=create_payload(f"bulk{i}"))
        ids.add(r.json()["id"])
    assert len(ids) == 10


def test_list_returns_taskread_shape(client):
    r = client.post("/tasks/", json=create_payload("schema-check", "dd"))
    r2 = client.get("/tasks/")
    data = r2.json()
    assert isinstance(data, list)
    if data:
        item = data[0]
        assert "id" in item and isinstance(item["id"], str)
        assert "title" in item and isinstance(item["title"], str)
        assert "status" in item and isinstance(item["status"], str)
