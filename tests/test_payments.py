from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def create_user(
    username="paymentuser",
    email="payment@example.com",
):
    response = client.post(
        "/auth/signup",
        json={
            "username": username,
            "email": email,
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 201


def login_user(username="paymentuser"):
    response = client.post(
        "/auth/login",
        json={
            "username": username,
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def create_centre_test():
    centre_response = client.post(
        "/centres/",
        json={
            "name": "Payment Diagnostics",
            "location": "Pune",
        },
    )

    assert centre_response.status_code == 201

    centre_id = centre_response.json()["id"]

    test_response = client.post(
        "/tests/",
        json={
            "name": "Payment Blood Test",
        },
    )

    assert test_response.status_code == 201

    test_id = test_response.json()["id"]

    centre_test_response = client.post(
        "/centre-tests/",
        json={
            "centre_id": centre_id,
            "test_id": test_id,
            "price": 50000,
        },
    )

    assert centre_test_response.status_code == 201

    return centre_test_response.json()["id"]


def create_booking(token, centre_test_id):
    response = client.post(
        "/bookings/",
        json={
            "centre_test_id": centre_test_id,
            "appointment_at": "2026-10-15T10:00:00",
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 201

    return response.json()["id"]


def test_successful_payment():
    create_user()
    token = login_user()

    centre_test_id = create_centre_test()
    booking_id = create_booking(
        token,
        centre_test_id,
    )

    response = client.post(
        "/payments/",
        json={
            "booking_id": booking_id,
            "success": True,
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["booking_id"] == booking_id
    assert data["amount"] == 50000
    assert data["status"] == "SUCCESS"


def test_failed_payment():
    create_user()
    token = login_user()

    centre_test_id = create_centre_test()
    booking_id = create_booking(
        token,
        centre_test_id,
    )

    response = client.post(
        "/payments/",
        json={
            "booking_id": booking_id,
            "success": False,
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["booking_id"] == booking_id
    assert data["amount"] == 50000
    assert data["status"] == "FAILED"


def test_payment_requires_authentication():
    response = client.post(
        "/payments/",
        json={
            "booking_id": 99999,
            "success": True,
        },
    )

    assert response.status_code == 401


def test_payment_booking_not_found():
    create_user()
    token = login_user()

    response = client.post(
        "/payments/",
        json={
            "booking_id": 99999,
            "success": True,
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Booking not found"


def test_user_cannot_pay_another_users_booking():
    create_user(
        username="userone",
        email="userone@example.com",
    )

    token_one = login_user("userone")

    centre_test_id = create_centre_test()

    booking_id = create_booking(
        token_one,
        centre_test_id,
    )

    create_user(
        username="usertwo",
        email="usertwo@example.com",
    )

    token_two = login_user("usertwo")

    response = client.post(
        "/payments/",
        json={
            "booking_id": booking_id,
            "success": True,
        },
        headers={
            "Authorization": f"Bearer {token_two}"
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Booking not found"


def test_payment_cannot_be_created_twice():
    create_user()
    token = login_user()

    centre_test_id = create_centre_test()
    booking_id = create_booking(
        token,
        centre_test_id,
    )

    first_response = client.post(
        "/payments/",
        json={
            "booking_id": booking_id,
            "success": True,
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/payments/",
        json={
            "booking_id": booking_id,
            "success": True,
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Booking is not pending"


def test_webhook_success():
    create_user()
    token = login_user()

    centre_test_id = create_centre_test()
    booking_id = create_booking(
        token,
        centre_test_id,
    )

    response = client.post(
        "/payments/webhook",
        json={
            "event_id": "evt_success_001",
            "booking_id": booking_id,
            "status": "SUCCESS",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["event_id"] == "evt_success_001"
    assert data["booking_id"] == booking_id
    assert data["status"] == "SUCCESS"


def test_webhook_failed_payment():
    create_user()
    token = login_user()

    centre_test_id = create_centre_test()
    booking_id = create_booking(
        token,
        centre_test_id,
    )

    response = client.post(
        "/payments/webhook",
        json={
            "event_id": "evt_failed_001",
            "booking_id": booking_id,
            "status": "FAILED",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["event_id"] == "evt_failed_001"
    assert data["booking_id"] == booking_id
    assert data["status"] == "FAILED"


def test_webhook_invalid_status():
    create_user()
    token = login_user()

    centre_test_id = create_centre_test()
    booking_id = create_booking(
        token,
        centre_test_id,
    )

    response = client.post(
        "/payments/webhook",
        json={
            "event_id": "evt_invalid_001",
            "booking_id": booking_id,
            "status": "PENDING",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid payment status"


def test_webhook_booking_not_found():
    response = client.post(
        "/payments/webhook",
        json={
            "event_id": "evt_missing_001",
            "booking_id": 99999,
            "status": "SUCCESS",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Booking not found"


def test_webhook_duplicate_event():
    create_user()
    token = login_user()

    centre_test_id = create_centre_test()
    booking_id = create_booking(
        token,
        centre_test_id,
    )

    first_response = client.post(
        "/payments/webhook",
        json={
            "event_id": "evt_duplicate_001",
            "booking_id": booking_id,
            "status": "SUCCESS",
        },
    )

    assert first_response.status_code == 200

    second_response = client.post(
        "/payments/webhook",
        json={
            "event_id": "evt_duplicate_001",
            "booking_id": booking_id,
            "status": "SUCCESS",
        },
    )

    assert second_response.status_code == 200

    assert second_response.json()["message"] == (
        "Webhook already processed"
    )
