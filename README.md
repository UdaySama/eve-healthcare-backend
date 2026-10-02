# EVE Healthcare Backend

Backend service for diagnostic test bookings and simulated payments.

This project was developed as part of the EVE Healthcare SDE Intern — Backend Engineering Assignment.

## Tech Stack

- Python 3.8+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- JWT Authentication
- Passlib / bcrypt
- Pytest
- HTTPX

## Features

### Authentication

- User signup
- User login
- Password hashing
- JWT-based authentication
- Authenticated user profile
- Duplicate username and email validation

### Diagnostic Centres

- Create diagnostic centres
- List diagnostic centres
- Get diagnostic centre by ID

### Diagnostic Tests

- Create diagnostic tests
- List diagnostic tests
- Get diagnostic test by ID

### Centre Test Pricing

- Associate tests with diagnostic centres
- Configure test price for each centre
- Prevent duplicate centre/test combinations
- Validate centre and test IDs
- Prevent negative prices

### Bookings

- Create authenticated bookings
- Automatically use configured test price
- List authenticated user's bookings
- Get booking details
- Prevent access to another user's bookings
- Track booking status

### Payments

- Simulated successful payments
- Simulated failed payments
- Prevent duplicate payments
- Verify booking ownership

### Payment Webhooks

- Process payment webhook events
- Support SUCCESS and FAILED payment states
- Update payment and booking status
- Handle duplicate webhook events using event IDs
- Validate webhook status
- Handle invalid booking IDs

## Project Structure

    eve-healthcare-backend/
    │
    ├── app/
    │   ├── __init__.py
    │   ├── main.py
    │   ├── auth.py
    │   ├── database.py
    │   ├── models.py
    │   ├── schemas.py
    │   │
    │   └── routes/
    │       ├── __init__.py
    │       ├── auth.py
    │       ├── centres.py
    │       ├── tests.py
    │       ├── centre_tests.py
    │       ├── bookings.py
    │       └── payments.py
    │
    ├── tests/
    │   ├── __init__.py
    │   ├── conftest.py
    │   ├── test_auth.py
    │   ├── test_centre_tests.py
    │   ├── test_bookings.py
    │   └── test_payments.py
    │
    ├── .gitignore
    ├── README.md
    └── requirements.txt

## Database Design

The application uses PostgreSQL.

### Tables

    users
      │
      └── bookings
              │
              ├── centre_tests
              │       ├── diagnostic_centres
              │       └── diagnostic_tests
              │
              └── payments
                      │
                      └── payment_webhook_events

### users

Stores registered application users.

Fields:

- id
- username
- email
- hashed_password

### diagnostic_centres

Stores diagnostic centre information.

Fields:

- id
- name
- location

### diagnostic_tests

Stores available diagnostic tests.

Fields:

- id
- name

### centre_tests

Connects diagnostic centres with diagnostic tests and stores the price.

Fields:

- id
- centre_id
- test_id
- price

A unique constraint prevents the same test from being added multiple times to the same centre.

### bookings

Stores diagnostic test bookings.

Fields:

- id
- user_id
- centre_test_id
- appointment_at
- amount
- status

Possible booking statuses:

- PENDING
- CONFIRMED
- FAILED

### payments

Stores simulated payment information.

Fields:

- id
- booking_id
- amount
- status

Each booking can have at most one payment.

### payment_webhook_events

Stores processed webhook event IDs.

Fields:

- id
- event_id
- payment_id
- status

The event_id is unique and is used to prevent duplicate webhook processing.

## Prerequisites

Make sure the following are installed:

- Python 3.8+
- PostgreSQL
- pip
- Git

## Clone the Repository

    git clone <repository-url>
    cd eve-healthcare-backend

Replace <repository-url> with the GitHub repository URL.

## Create a Virtual Environment

### Linux/macOS

    python3 -m venv venv
    source venv/bin/activate

### Windows

    python -m venv venv
    venv\Scripts\activate

## Install Dependencies

    pip install -r requirements.txt

## PostgreSQL Setup

Create a PostgreSQL database for the application.

Example:

    CREATE DATABASE eve_healthcare_db;

Create a PostgreSQL user if required:

    CREATE USER eve_app WITH PASSWORD 'your_password';

Grant database access:

    GRANT ALL PRIVILEGES ON DATABASE eve_healthcare_db TO eve_app;

The exact PostgreSQL commands may vary depending on the local PostgreSQL configuration.

## Environment Variables

Create:

    app/.env

Add:

    DATABASE_URL=postgresql://eve_app:your_password@localhost:5432/eve_healthcare_db
    SECRET_KEY=your-secret-key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30

### Environment Variable Description

| Variable | Description |
|---|---|
| DATABASE_URL | PostgreSQL connection string |
| SECRET_KEY | Secret used for signing JWT tokens |
| ALGORITHM | JWT signing algorithm |
| ACCESS_TOKEN_EXPIRE_MINUTES | JWT expiration time |

Do not commit .env or database credentials to Git.

## Run the Application

From the project root:

    uvicorn app.main:app --reload

The API will be available at:

    http://127.0.0.1:8000

## API Documentation

FastAPI automatically provides interactive API documentation.

Swagger UI:

    http://127.0.0.1:8000/docs

ReDoc:

    http://127.0.0.1:8000/redoc

# API Endpoints

## Health Check

### GET /health

Checks whether the API is running.

Example response:

    {
      "status": "ok"
    }

# Authentication

## POST /auth/signup

Creates a new user.

### Request

    {
      "username": "john",
      "email": "john@example.com",
      "password": "TestPassword123"
    }

### Response

    {
      "message": "User created successfully",
      "user_id": 1,
      "username": "john",
      "email": "john@example.com"
    }

## POST /auth/login

Authenticates a user and returns a JWT access token.

### Request

    {
      "username": "john",
      "password": "TestPassword123"
    }

### Response

    {
      "access_token": "<jwt-token>",
      "token_type": "bearer"
    }

Use the returned token for protected endpoints:

    Authorization: Bearer <jwt-token>

## GET /auth/me

Returns the currently authenticated user's information.

### Response

    {
      "id": 1,
      "username": "john",
      "email": "john@example.com"
    }

# Diagnostic Centres

## POST /centres/

Creates a diagnostic centre.

### Request

    {
      "name": "ABC Diagnostics",
      "location": "Pune"
    }

### Response

    {
      "id": 1,
      "name": "ABC Diagnostics",
      "location": "Pune"
    }

## GET /centres/

Returns all diagnostic centres.

## GET /centres/{centre_id}

Returns a diagnostic centre by ID.

Example:

    GET /centres/1

# Diagnostic Tests

## POST /tests/

Creates a diagnostic test.

### Request

    {
      "name": "Complete Blood Count"
    }

### Response

    {
      "id": 1,
      "name": "Complete Blood Count"
    }

## GET /tests/

Returns all diagnostic tests.

## GET /tests/{test_id}

Returns a diagnostic test by ID.

Example:

    GET /tests/1

# Centre Test Pricing

## POST /centre-tests/

Associates a diagnostic test with a diagnostic centre and sets its price.

### Request

    {
      "centre_id": 1,
      "test_id": 1,
      "price": 50000
    }

### Response

    {
      "id": 1,
      "centre_id": 1,
      "test_id": 1,
      "price": 50000
    }

The API prevents:

- Invalid centre IDs
- Invalid test IDs
- Negative prices
- Duplicate centre/test combinations

## GET /centre-tests/

Returns all centre-test pricing records.

## GET /centre-tests/{centre_test_id}

Returns a specific centre-test pricing record.

# Bookings

Bookings require JWT authentication.

## POST /bookings/

Creates a booking for the authenticated user.

### Request

    {
      "centre_test_id": 1,
      "appointment_at": "2026-10-15T10:00:00"
    }

The booking amount is automatically taken from the configured price of the selected centre/test combination.

### Response

    {
      "id": 1,
      "centre_test_id": 1,
      "appointment_at": "2026-10-15T10:00:00",
      "amount": 50000,
      "status": "PENDING"
    }

## GET /bookings/

Returns bookings belonging only to the authenticated user.

## GET /bookings/{booking_id}

Returns detailed information about a user's booking.

### Response

    {
      "id": 1,
      "centre_test_id": 1,
      "centre_name": "ABC Diagnostics",
      "test_name": "Complete Blood Count",
      "appointment_at": "2026-10-15T10:00:00",
      "amount": 50000,
      "status": "PENDING"
    }

A user cannot access another user's booking.

# Payments

Payments are simulated for this assignment.

## POST /payments/

Creates a simulated payment for an authenticated user's pending booking.

### Successful Payment

Request:

    {
      "booking_id": 1,
      "success": true
    }

Response:

    {
      "id": 1,
      "booking_id": 1,
      "amount": 50000,
      "status": "SUCCESS"
    }

The booking status becomes CONFIRMED.

### Failed Payment

Request:

    {
      "booking_id": 1,
      "success": false
    }

Response:

    {
      "id": 1,
      "booking_id": 1,
      "amount": 50000,
      "status": "FAILED"
    }

The booking status becomes FAILED.

A payment cannot be created again for a booking that is no longer pending.

# Payment Webhook

## POST /payments/webhook

Simulates a payment provider webhook.

This endpoint does not require user authentication because it represents a callback from an external payment system.

### Successful Webhook

Request:

    {
      "event_id": "evt_success_001",
      "booking_id": 1,
      "status": "SUCCESS"
    }

Response:

    {
      "message": "Webhook processed successfully",
      "event_id": "evt_success_001",
      "booking_id": 1,
      "status": "SUCCESS"
    }

### Failed Webhook

Request:

    {
      "event_id": "evt_failed_001",
      "booking_id": 1,
      "status": "FAILED"
    }

The associated booking becomes FAILED.

## Webhook Idempotency

Each webhook must contain a unique event_id.

If the same event is received again, it is not processed a second time.

Example:

    {
      "event_id": "evt_success_001",
      "booking_id": 1,
      "status": "SUCCESS"
    }

Sending the same event again returns:

    {
      "message": "Webhook already processed",
      "event_id": "evt_success_001"
    }

This prevents duplicate processing of the same payment event.

# Authentication Flow

The typical application flow is:

    1. User Signup
           ↓
    2. User Login
           ↓
    3. Receive JWT
           ↓
    4. Create/List Diagnostic Centres
           ↓
    5. Create/List Diagnostic Tests
           ↓
    6. Configure Centre + Test + Price
           ↓
    7. Create Booking
           ↓
    8. Booking starts as PENDING
           ↓
    9. Simulated Payment / Payment Webhook
           ↓
    10. Booking becomes CONFIRMED or FAILED

# Error Handling

The API handles common invalid requests and resource errors.

Examples include:

- 400 Bad Request
- 401 Unauthorized
- 404 Not Found
- 409 Conflict
- 422 Unprocessable Entity

Handled cases include:

- Invalid login credentials
- Duplicate username
- Duplicate email
- Missing authentication
- Invalid JWT
- Invalid centre ID
- Invalid test ID
- Invalid centre-test ID
- Negative price
- Duplicate centre/test combination
- Invalid booking ID
- Accessing another user's booking
- Paying another user's booking
- Duplicate payment
- Invalid webhook status
- Duplicate webhook event

# Testing

The project uses pytest for automated API testing.

A separate PostgreSQL database is used for tests so that test data does not affect the development database.

Test database:

    eve_healthcare_test_db

The test setup automatically cleans the database before each test.

## Run Tests

From the project root:

    pytest

Current test result:

    32 passed

The tests cover:

### Authentication

- Health check
- User signup
- Duplicate username
- Invalid password
- Successful login
- Authenticated user profile

### Centre/Test Pricing

- Create pricing
- Duplicate centre/test
- List pricing
- Get pricing
- Invalid centre
- Invalid test
- Negative price
- Invalid pricing ID

### Bookings

- Create booking
- Correct booking amount
- List user bookings
- Booking details
- Invalid centre-test ID
- Authentication requirement
- User isolation
- Unauthorized booking access

### Payments

- Successful payment
- Failed payment
- Authentication requirement
- Invalid booking
- Unauthorized payment
- Duplicate payment prevention
- Successful webhook
- Failed webhook
- Invalid webhook status
- Invalid webhook booking
- Duplicate webhook event

# Security Considerations

The project includes the following security measures:

- Passwords are stored as bcrypt hashes rather than plain text.
- JWT authentication protects user-specific endpoints.
- Booking queries are restricted to the authenticated user.
- Payment creation verifies booking ownership.
- Sensitive environment variables are stored outside source code.
- Duplicate webhook events are tracked using unique event IDs.
- Database constraints are used for unique usernames, emails, centre/test combinations, payment bookings, and webhook event IDs.

# Assumptions

The following assumptions were made for this assignment:

1. A registered user is considered the patient making the booking.
2. Payment processing is simulated and does not connect to a real payment provider.
3. Diagnostic centre and test management endpoints are available without a separate admin role because the assignment does not define an admin authentication flow.
4. Prices are represented as integer values for simplicity.
5. Appointment scheduling does not integrate with an external calendar or scheduling provider.
6. The API focuses on the required booking and payment workflow rather than production-scale infrastructure.
7. JWT access tokens are used for authenticated API requests.

# Design Decisions

## SQLAlchemy

SQLAlchemy is used as the ORM to interact with PostgreSQL and keep database operations organized within the application layer.

## JWT

JWT provides stateless authentication for protected endpoints.

## Separate Centre-Test Table

A separate centre_tests table is used because the same diagnostic test can be offered by multiple diagnostic centres at different prices.

Example:

    Centre A + Blood Test = 500
    Centre B + Blood Test = 650

This allows pricing to be associated with the centre/test combination instead of the test itself.

## Webhook Event Tracking

Webhook events are stored separately using a unique event_id.

This allows the API to recognize duplicate events and avoid processing the same event multiple times.

# Future Improvements

If this service were developed further for a production environment, possible improvements would include:

- Admin authentication and role-based authorization
- Stronger password policies
- Appointment slot availability and conflict prevention
- Pagination for list endpoints
- Filtering and searching
- Database migrations using Alembic
- Docker and Docker Compose
- Redis for caching
- Celery/background jobs
- Rate limiting
- Structured application logging
- Improved payment state management
- Production payment provider integration
- Webhook signature verification
- More comprehensive integration tests
- CI/CD pipeline
- Production monitoring and error tracking
- API versioning
- Improved database indexing
- HTTPS and production security configuration

# Running the Project Locally

Quick start:

    git clone <repository-url>
    cd eve-healthcare-backend

    python3 -m venv venv
    source venv/bin/activate

    pip install -r requirements.txt

Configure:

    app/.env

Then start the API:

    uvicorn app.main:app --reload

Open:

    http://127.0.0.1:8000/docs

Run tests:

    pytest

# Project Status

The core backend workflow is implemented and tested.

Current automated test result:

    32 passed

The project currently covers:

    Authentication
          ↓
    Diagnostic Centres
          ↓
    Diagnostic Tests
          ↓
    Centre/Test Pricing
          ↓
    Bookings
          ↓
    Simulated Payments
          ↓
    Payment Webhooks
          ↓
    Webhook Idempotency

## Database 
![Database](docs/db/database-schema.png)

## Swagger / OpenAPI Documentation

The API provides interactive Swagger/OpenAPI documentation through FastAPI.

Swagger UI:

`http://127.0.0.1:8000/docs`

The documentation includes authentication, diagnostic centres, diagnostic tests, centre-specific pricing, bookings, and simulated payments.

### Swagger Overview

![Swagger API Documentation](docs/Swagger/default_swagger_.png)

### Authentication

![Authentication Swagger](docs/Swagger/Authentication_swagger_.png)

### Bookings

![Bookings Swagger](docs/Swagger/Bookings_swagger_.png)

### Centre Tests & Pricing

![Centre Tests and Pricing Swagger](docs/Swagger/Centre-Tests_and_Pricing_swagger_.png)

### Diagnostic Centres

![Diagnostic Centres Swagger](docs/Swagger/Diagnostic_Centres_swagger_.png)

## API Documentation

The API provides interactive OpenAPI documentation using FastAPI.

### ReDoc

Available at:

`http://127.0.0.1:8000/redoc`

![ReDoc](docs/ReDoc/redoc_overview.png)

### Payments

![Payments Swagger](docs/Swagger/Payments_swagger_.png.png)

# Author

Developed for the EVE Healthcare SDE Intern — Backend Engineering Assignment.