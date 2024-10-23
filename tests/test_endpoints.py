from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import pytest
from unittest.mock import patch

from models import BlacklistEmail

fake = Faker()
fake.seed_instance(0)


@pytest.fixture
def valid_body() -> dict:
    """Body for correct creation."""
    return {
        "email": fake.email(),
        "app_uuid": str(fake.uuid4()),
        "blocked_reason": fake.pystr(max_chars=255, min_chars=100),
    }


@pytest.fixture
def create_blacklisted_email(valid_body: dict, client: TestClient) -> dict:
    with patch(
        "main.Request.client",
        new_callable=lambda: type("obj", (object,), {"host": "9.4.6.3"}),
    ):
        response = client.post("/blacklists", json=valid_body)
        assert response.status_code == 201, response.text
        return response.json()


def test_add_blacklisted_email(
    db_session: Session,
    create_blacklisted_email: dict,
    valid_body: dict,
):
    assert create_blacklisted_email["is_blacklisted"] is True
    assert create_blacklisted_email["result"] == valid_body["blocked_reason"]

    db_email = (
        db_session.query(BlacklistEmail).filter_by(email=valid_body["email"]).first()
    )
    assert db_email is not None
    assert db_email.email == valid_body["email"]
    assert str(db_email.app_uuid) == valid_body["app_uuid"]
    assert db_email.blocked_reason == valid_body["blocked_reason"]
    assert db_email.ip == "9.4.6.3"


@pytest.mark.usefixtures("create_blacklisted_email")
def test_add_repeated_blacklisted_email(client: TestClient, valid_body: dict):
    response = client.post("/blacklists", json=valid_body)
    assert response.status_code == 400, response.text
    assert response.json() == {
        "is_blacklisted": False,
        "reason": "Email already blacklisted",
    }


def test_add_blacklisted_email_incomplete_body(client: TestClient):
    response = client.post("/blacklists", json={})
    assert response.status_code == 400, response.text
    assert response.json() == [
        {
            "type": "missing",
            "loc": ["email"],
            "msg": "Field required",
            "input": {},
            "url": "https://errors.pydantic.dev/2.9/v/missing",
        },
        {
            "type": "missing",
            "loc": ["app_uuid"],
            "msg": "Field required",
            "input": {},
            "url": "https://errors.pydantic.dev/2.9/v/missing",
        },
        {
            "type": "missing",
            "loc": ["blocked_reason"],
            "msg": "Field required",
            "input": {},
            "url": "https://errors.pydantic.dev/2.9/v/missing",
        },
    ]


@pytest.mark.usefixtures("create_blacklisted_email")
def test_get_blackliste_email(client: TestClient, valid_body: dict):
    response = client.get(f"/blacklists/{valid_body['email']}")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "is_blacklisted": True,
        "blocked_reason": valid_body["blocked_reason"],
    }


def test_get_non_blacklisted_email(client: TestClient):
    response = client.get(f"/blacklists/{fake.email()}")
    assert response.status_code == 200, response.text
    assert response.json() == {"is_blacklisted": False, "blocked_reason": None}


def test_get_non_blacklisted_email_invalid_auth(client: TestClient):
    response = client.get(
        f"/blacklists/{fake.email()}", headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401, response.text


def test_create_blacklisted_email_invalid_auth(client: TestClient, valid_body: dict):
    response = client.post(
        "/blacklists",
        headers={"Authorization": "Bearer invalid_token"},
        json=valid_body,
    )
    assert response.status_code == 401, response.text
