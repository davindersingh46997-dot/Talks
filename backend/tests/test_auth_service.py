from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from backend.schemas.user import UserCreate
from backend.services import auth_service


@pytest.fixture
def user_data():
    return UserCreate(
        username="test-user",
        email="test@example.com",
        password="correct-horse-battery-staple",
    )


def test_register_user_hashes_password_and_creates_user(
    monkeypatch,
    user_data,
):
    db = object()
    created = SimpleNamespace(id=1)
    calls = []

    monkeypatch.setattr(auth_service, "get_user_by_email", lambda *_: None)
    monkeypatch.setattr(auth_service, "get_user_by_username", lambda *_: None)
    monkeypatch.setattr(
        auth_service,
        "hash_password",
        lambda password: f"hashed:{password}",
    )

    def create_user(**kwargs):
        calls.append(kwargs)
        return created

    monkeypatch.setattr(auth_service, "create_user", create_user)

    assert auth_service.register_user(db, user_data) is created
    assert calls == [
        {
            "db": db,
            "username": "test-user",
            "email": "test@example.com",
            "hashed_password": "hashed:correct-horse-battery-staple",
        }
    ]


def test_register_user_rejects_duplicate_email(monkeypatch, user_data):
    monkeypatch.setattr(
        auth_service,
        "get_user_by_email",
        lambda *_: object(),
    )
    monkeypatch.setattr(
        auth_service,
        "get_user_by_username",
        lambda *_: pytest.fail("username lookup should not run"),
    )
    monkeypatch.setattr(
        auth_service,
        "hash_password",
        lambda *_: pytest.fail("password should not be hashed"),
    )

    with pytest.raises(HTTPException) as exc_info:
        auth_service.register_user(object(), user_data)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Email already registered"


def test_register_user_rejects_duplicate_username(monkeypatch, user_data):
    monkeypatch.setattr(auth_service, "get_user_by_email", lambda *_: None)
    monkeypatch.setattr(
        auth_service,
        "get_user_by_username",
        lambda *_: object(),
    )
    monkeypatch.setattr(
        auth_service,
        "hash_password",
        lambda *_: pytest.fail("password should not be hashed"),
    )

    with pytest.raises(HTTPException) as exc_info:
        auth_service.register_user(object(), user_data)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Username already exists"


def test_authenticate_user_returns_user_for_valid_password(monkeypatch):
    db = object()
    user = SimpleNamespace(password_hash="stored-hash")
    monkeypatch.setattr(
        auth_service,
        "get_user_by_email",
        lambda actual_db, email: user
        if actual_db is db and email == "test@example.com"
        else None,
    )
    monkeypatch.setattr(
        auth_service,
        "verify_password",
        lambda plain, hashed: plain == "secret" and hashed == "stored-hash",
    )

    assert auth_service.authenticate_user(db, "test@example.com", "secret") is user


def test_authenticate_user_returns_none_for_unknown_email(monkeypatch):
    monkeypatch.setattr(auth_service, "get_user_by_email", lambda *_: None)
    monkeypatch.setattr(
        auth_service,
        "verify_password",
        lambda *_: pytest.fail("password verification should not run"),
    )

    assert auth_service.authenticate_user(
        object(),
        "missing@example.com",
        "secret",
    ) is None


def test_login_user_rejects_invalid_credentials(monkeypatch):
    monkeypatch.setattr(auth_service, "authenticate_user", lambda *_: None)

    with pytest.raises(HTTPException) as exc_info:
        auth_service.login_user(object(), "test@example.com", "wrong")

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid email or password"


def test_login_user_returns_bearer_token(monkeypatch):
    user = SimpleNamespace(id=42)
    captured = {}

    monkeypatch.setattr(auth_service, "authenticate_user", lambda *_: user)

    def create_access_token(*, data):
        captured.update(data)
        return "test-token"

    monkeypatch.setattr(auth_service, "create_access_token", create_access_token)

    assert auth_service.login_user(
        object(),
        "test@example.com",
        "secret",
    ) == {
        "access_token": "test-token",
        "token_type": "bearer",
    }
    assert captured == {"sub": "42"}
