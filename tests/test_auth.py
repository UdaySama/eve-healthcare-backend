from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_signup_success():
    response = client.post(
        "/auth/signup",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"
    assert "user_id" in data


def test_signup_duplicate_username():
    client.post(
        "/auth/signup",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "TestPassword123",
        },
    )

    response = client.post(
        "/auth/signup",
        json={
            "username": "testuser",
            "email": "another@example.com",
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Username already exists"


def test_login_invalid_password():
    client.post(
        "/auth/signup",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "TestPassword123",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "username": "testuser",
            "password": "WrongPassword123",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"


def test_login_success_and_get_me():
    signup_response = client.post(
        "/auth/signup",
        json={
            "username": "loginuser",
            "email": "loginuser@example.com",
            "password": "TestPassword123",
        },
    )

    assert signup_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "username": "loginuser",
            "password": "TestPassword123",
        },
    )

    assert login_response.status_code == 200

    login_data = login_response.json()

    assert "access_token" in login_data
    assert login_data["token_type"] == "bearer"

    token = login_data["access_token"]

    me_response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert me_response.status_code == 200

    me_data = me_response.json()

    assert me_data["username"] == "loginuser"
    assert me_data["email"] == "loginuser@example.com"