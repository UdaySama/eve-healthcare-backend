from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

# all test releted to booking
def create_user(username="bookinguser", email="booking@example.com"):
    response = client.post(
        "/auth/signup",
        json={
            "username": username,
            "email": email,
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 201


def login_user(username="bookinguser"):
    response = client.post(
        "/auth/login",
        json={
            "username": username,
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


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


def create_centre_test():
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

    return response.json()["id"]


def create_booking(token, centre_test_id):
    response = client.post(
        "/bookings/",
        json={
            "centre_test_id": centre_test_id,
            "appointment_at": "2026-10-10T10:00:00",
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    return response


def test_create_booking_success():
    create_user()
    token = login_user()
    centre_test_id = create_centre_test()

    response = create_booking(token, centre_test_id)

    assert response.status_code == 201

    data = response.json()

    assert data["centre_test_id"] == centre_test_id
    assert data["amount"] == 50000
    assert data["status"] == "PENDING"
    assert "id" in data


def test_booking_amount_uses_centre_test_price():
    create_user()
    token = login_user()

    centre_id = create_centre()
    test_id = create_test()

    response = client.post(
        "/centre-tests/",
        json={
            "centre_id": centre_id,
            "test_id": test_id,
            "price": 75000,
        },
    )

    assert response.status_code == 201

    centre_test_id = response.json()["id"]

    booking_response = create_booking(
        token,
        centre_test_id,
    )

    assert booking_response.status_code == 201
    assert booking_response.json()["amount"] == 75000


def test_get_user_bookings():
    create_user()
    token = login_user()
    centre_test_id = create_centre_test()

    create_booking(token, centre_test_id)

    response = client.get(
        "/bookings/",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["centre_test_id"] == centre_test_id
    assert data[0]["amount"] == 50000
    assert data[0]["status"] == "PENDING"


def test_get_booking_details():
    create_user()
    token = login_user()
    centre_test_id = create_centre_test()

    booking_response = create_booking(
        token,
        centre_test_id,
    )

    booking_id = booking_response.json()["id"]

    response = client.get(
        f"/bookings/{booking_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == booking_id
    assert data["centre_test_id"] == centre_test_id
    assert data["centre_name"] == "Test Diagnostics"
    assert data["test_name"] == "CBC Blood Test"
    assert data["amount"] == 50000
    assert data["status"] == "PENDING"


def test_booking_invalid_centre_test():
    create_user()
    token = login_user()

    response = create_booking(
        token,
        99999,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Centre test not found"


def test_booking_requires_authentication():
    centre_test_id = create_centre_test()

    response = client.post(
        "/bookings/",
        json={
            "centre_test_id": centre_test_id,
            "appointment_at": "2026-10-10T10:00:00",
        },
    )

    assert response.status_code == 401


def test_user_cannot_access_another_users_booking():
    create_user(
        username="userone",
        email="userone@example.com",
    )

    token_one = login_user("userone")

    centre_test_id = create_centre_test()

    booking_response = create_booking(
        token_one,
        centre_test_id,
    )

    booking_id = booking_response.json()["id"]

    create_user(
        username="usertwo",
        email="usertwo@example.com",
    )

    token_two = login_user("usertwo")

    response = client.get(
        f"/bookings/{booking_id}",
        headers={
            "Authorization": f"Bearer {token_two}"
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Booking not found"


def test_user_only_sees_own_bookings():
    create_user(
        username="userone",
        email="userone@example.com",
    )

    token_one = login_user("userone")

    centre_test_id = create_centre_test()

    create_booking(
        token_one,
        centre_test_id,
    )

    create_user(
        username="usertwo",
        email="usertwo@example.com",
    )

    token_two = login_user("usertwo")

    response = client.get(
        "/bookings/",
        headers={
            "Authorization": f"Bearer {token_two}"
        },
    )

    assert response.status_code == 200
    assert response.json() == []