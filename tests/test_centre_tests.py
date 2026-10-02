from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def create_centre():
    response = client.post(
        "/centres/",
        json={
            "name": "Test Diagnostics",
            "location": "Pune",
        },
    )

    assert response.status_code == 201

    return response.json()["id"]


def create_test():
    response = client.post(
        "/tests/",
        json={
            "name": "CBC Blood Test",
        },
    )

    assert response.status_code == 201

    return response.json()["id"]


def test_create_centre_test():
    centre_id = create_centre()
    test_id = create_test()

    response = client.post(
        "/centre-tests/",
        json={
            "centre_id": centre_id,
            "test_id": test_id,
            "price": 50000,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["centre_id"] == centre_id
    assert data["test_id"] == test_id
    assert data["price"] == 50000
    assert "id" in data


def test_duplicate_centre_test():
    centre_id = create_centre()
    test_id = create_test()

    client.post(
        "/centre-tests/",
        json={
            "centre_id": centre_id,
            "test_id": test_id,
            "price": 50000,
        },
    )

    response = client.post(
        "/centre-tests/",
        json={
            "centre_id": centre_id,
            "test_id": test_id,
            "price": 60000,
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "Test is already available at this centre"
    )


def test_get_centre_tests():
    centre_id = create_centre()
    test_id = create_test()

    client.post(
        "/centre-tests/",
        json={
            "centre_id": centre_id,
            "test_id": test_id,
            "price": 50000,
        },
    )

    response = client.get("/centre-tests/")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["centre_id"] == centre_id
    assert data[0]["test_id"] == test_id
    assert data[0]["price"] == 50000


def test_get_centre_test():
    centre_id = create_centre()
    test_id = create_test()

    create_response = client.post(
        "/centre-tests/",
        json={
            "centre_id": centre_id,
            "test_id": test_id,
            "price": 50000,
        },
    )

    centre_test_id = create_response.json()["id"]

    response = client.get(
        f"/centre-tests/{centre_test_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == centre_test_id
    assert data["centre_id"] == centre_id
    assert data["test_id"] == test_id
    assert data["price"] == 50000


def test_centre_not_found():
    test_id = create_test()

    response = client.post(
        "/centre-tests/",
        json={
            "centre_id": 99999,
            "test_id": test_id,
            "price": 50000,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Diagnostic centre not found"


def test_test_not_found():
    centre_id = create_centre()

    response = client.post(
        "/centre-tests/",
        json={
            "centre_id": centre_id,
            "test_id": 99999,
            "price": 50000,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Diagnostic test not found"


def test_negative_price():
    centre_id = create_centre()
    test_id = create_test()

    response = client.post(
        "/centre-tests/",
        json={
            "centre_id": centre_id,
            "test_id": test_id,
            "price": -500,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Price cannot be negative"


def test_centre_test_not_found():
    response = client.get("/centre-tests/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Centre test not found"