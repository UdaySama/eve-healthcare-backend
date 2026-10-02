# EVE Healthcare Backend

Backend service for diagnostic test bookings and simulated payments.

This project was developed as part of the **EVE Healthcare SDE Intern — Backend Engineering Assignment**.

---

## Tech Stack

* Python 3.8+
* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic
* JWT Authentication
* Passlib / bcrypt
* Pytest
* HTTPX
* Docker
* Docker Compose

---

# Features

## Authentication

* User signup
* User login
* Password hashing using bcrypt
* JWT-based authentication
* Authenticated user profile
* Duplicate username validation
* Duplicate email validation

## Diagnostic Centres

* Create diagnostic centres
* List diagnostic centres
* Get diagnostic centre by ID

## Diagnostic Tests

* Create diagnostic tests
* List diagnostic tests
* Get diagnostic test by ID

## Centre Test Pricing

* Associate diagnostic tests with diagnostic centres
* Configure test price for each centre/test combination
* Prevent duplicate centre/test combinations
* Validate centre and test IDs
* Prevent negative prices

## Bookings

* Create authenticated bookings
* Automatically use the configured test price
* List bookings belonging to the authenticated user
* Get detailed booking information
* Prevent access to another user's bookings
* Track booking status

## Payments

* Simulated successful payments
* Simulated failed payments
* Prevent duplicate payments
* Verify booking ownership
* Prevent payments for non-pending bookings

## Payment Webhooks

* Process simulated payment webhook events
* Support `SUCCESS` and `FAILED` payment states
* Update payment and booking status
* Handle duplicate webhook events using unique event IDs
* Validate webhook status
* Handle invalid booking IDs
* Prevent processing webhooks for non-pending bookings

---

# Project Structure

```text
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
├── docs/
│   ├── db/
│   │   └── database-schema.png
│   │
│   └── Swagger/
│       ├── default_swagger_.png
│       ├── Authentication_swagger_.png
│       ├── Bookings_swagger_.png
│       ├── Centre-Tests_and_Pricing_swagger_.png
│       ├── Diagnostic_Centres_swagger_.png
│       ├── Diagnostic_Tests_swagger_.png
│       ├── Payments_swagger_.png
│       └── redoc_overview.png
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── README.md
└── requirements.txt
```

> Environment files such as `.env` and `.env.docker` are intentionally excluded from the repository.

---

# Database Design

The application uses **PostgreSQL**.

## Database Relationships

```text
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
```

## `users`

Stores registered application users.

Fields:

* `id`
* `username`
* `email`
* `hashed_password`

## `diagnostic_centres`

Stores diagnostic centre information.

Fields:

* `id`
* `name`
* `location`

## `diagnostic_tests`

Stores available diagnostic tests.

Fields:

* `id`
* `name`

## `centre_tests`

Connects diagnostic centres with diagnostic tests and stores the price.

Fields:

* `id`
* `centre_id`
* `test_id`
* `price`

A unique constraint prevents the same test from being added multiple times to the same diagnostic centre.

## `bookings`

Stores diagnostic test bookings.

Fields:

* `id`
* `user_id`
* `centre_test_id`
* `appointment_at`
* `amount`
* `status`

Possible booking statuses:

* `PENDING`
* `CONFIRMED`
* `FAILED`

## `payments`

Stores simulated payment information.

Fields:

* `id`
* `booking_id`
* `amount`
* `status`

Each booking can have at most one payment.

## `payment_webhook_events`

Stores processed webhook event information.

Fields:

* `id`
* `event_id`
* `payment_id`
* `status`

The `event_id` is unique and is used to prevent duplicate webhook processing.

## Database Schema

![Database Schema](docs/db/database-schema.png)

---

# Prerequisites

For local development, make sure the following are installed:

* Python 3.8+
* PostgreSQL
* pip
* Git

For Docker execution:

* Docker
* Docker Compose

---

# Clone the Repository

```bash
git clone https://github.com/UdaySama/eve-healthcare-backend.git
cd eve-healthcare-backend
```


---

# Local Setup

## Create a Virtual Environment

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# PostgreSQL Setup

Create a PostgreSQL database for the application.

Example:

```sql
CREATE DATABASE eve_healthcare_db;
```

Create a PostgreSQL user if required:

```sql
CREATE USER eve_app WITH PASSWORD 'your_password';
```

Grant database access:

```sql
GRANT ALL PRIVILEGES ON DATABASE eve_healthcare_db TO eve_app;
```

The exact PostgreSQL commands may vary depending on the local PostgreSQL configuration.

---

# Environment Variables

Create a `.env` file in the **project root**:

```text
.env
```

Add:

```env
DATABASE_URL=postgresql://eve_app:your_password@localhost:5432/eve_healthcare_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=5
```

## Environment Variable Description

| Variable                      | Description                        |
| ----------------------------- | ---------------------------------- |
| `DATABASE_URL`                | PostgreSQL connection string       |
| `SECRET_KEY`                  | Secret used for signing JWT tokens |
| `ALGORITHM`                   | JWT signing algorithm              |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT access token expiration time   |

> Do not commit `.env` files, passwords, JWT secrets, or database credentials to Git.

---

# Run the Application Locally

From the project root:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

# Docker Setup

The project also includes Docker support for running the FastAPI application and PostgreSQL together.

## Docker Files

```text
Dockerfile
docker-compose.yml
.dockerignore
```

The Docker Compose setup contains:

* FastAPI application container
* PostgreSQL database container
* Docker network between the API and database
* Persistent PostgreSQL volume

## Docker Environment Variables

Create a `.env.docker` file in the project root.

Example:

```env
DATABASE_URL=postgresql://eve_app:your_password@db:5432/eve_healthcare_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=5

POSTGRES_USER=eve_app
POSTGRES_PASSWORD=your_password
POSTGRES_DB=eve_healthcare_db
```

The database host is `db` because it is the PostgreSQL service name defined in `docker-compose.yml`.

Do not commit `.env.docker`.

## Build and Start the Docker Environment

```bash
docker compose up --build
```

The API is exposed on:

```text
http://127.0.0.1:8001
```

Swagger:

```text
http://127.0.0.1:8001/docs
```

ReDoc:

```text
http://127.0.0.1:8001/redoc
```

Health check:

```text
http://127.0.0.1:8001/health
```

Example:

```bash
curl http://127.0.0.1:8001/health
```

Response:

```json
{
  "status": "ok"
}
```

## Stop Docker Services

```bash
docker compose down
```

To remove the Docker PostgreSQL volume as well:

```bash
docker compose down -v
```

> Removing the volume deletes the PostgreSQL data stored in that Docker volume.

---

# API Documentation

FastAPI automatically provides interactive OpenAPI documentation.

## Swagger UI

Local:

```text
http://127.0.0.1:8000/docs
```

Docker:

```text
http://127.0.0.1:8001/docs
```

Swagger UI allows the API endpoints to be explored and tested interactively.

![Swagger API Documentation](docs/Swagger/default_swagger_.png)

## ReDoc

Local:

```text
http://127.0.0.1:8000/redoc
```

Docker:

```text
http://127.0.0.1:8001/redoc
```

![ReDoc](docs/Swagger/redoc_overview.png)

## OpenAPI Specification

Local:

```text
http://127.0.0.1:8000/openapi.json
```

Docker:

```text
http://127.0.0.1:8001/openapi.json
```

---

# Swagger Screenshots

## Authentication

![Authentication Swagger](docs/Swagger/Authentication_swagger_.png)

## Bookings

![Bookings Swagger](docs/Swagger/Bookings_swagger_.png)

## Centre Tests & Pricing

![Centre Tests and Pricing Swagger](docs/Swagger/Centre-Tests_and_Pricing_swagger_.png)

## Diagnostic Centres

![Diagnostic Centres Swagger](docs/Swagger/Diagnostic_Centres_swagger_.png)

## Diagnostic Tests

![Diagnostic Tests Swagger](docs/Swagger/Diagnostic_Tests_swagger_.png)

## Payments

![Payments Swagger](docs/Swagger/Payments_swagger_.png)

---

# API Endpoints

## Health Check

### `GET /health`

Checks whether the API is running.

Example response:

```json
{
  "status": "ok"
}
```

---

# Authentication

## `POST /auth/signup`

Creates a new user.

### Request

```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "TestPassword123"
}
```

### Response

```json
{
  "message": "User created successfully",
  "user_id": 1,
  "username": "john",
  "email": "john@example.com"
}
```

## `POST /auth/login`

Authenticates a user and returns a JWT access token.

### Request

```json
{
  "username": "john",
  "password": "TestPassword123"
}
```

### Response

```json
{
  "access_token": "<jwt-token>",
  "token_type": "bearer"
}
```

Use the returned token for protected endpoints:

```text
Authorization: Bearer <jwt-token>
```

## `GET /auth/me`

Returns information about the currently authenticated user.

### Response

```json
{
  "id": 1,
  "username": "john",
  "email": "john@example.com"
}
```

---

# Diagnostic Centres

## `POST /centres/`

Creates a diagnostic centre.

### Request

```json
{
  "name": "ABC Diagnostics",
  "location": "Pune"
}
```

### Response

```json
{
  "id": 1,
  "name": "ABC Diagnostics",
  "location": "Pune"
}
```

## `GET /centres/`

Returns all diagnostic centres.

## `GET /centres/{centre_id}`

Returns a diagnostic centre by ID.

Example:

```text
GET /centres/1
```

---

# Diagnostic Tests

## `POST /tests/`

Creates a diagnostic test.

### Request

```json
{
  "name": "Complete Blood Count"
}
```

### Response

```json
{
  "id": 1,
  "name": "Complete Blood Count"
}
```

## `GET /tests/`

Returns all diagnostic tests.

## `GET /tests/{test_id}`

Returns a diagnostic test by ID.

Example:

```text
GET /tests/1
```

---

# Centre Test Pricing

## `POST /centre-tests/`

Associates a diagnostic test with a diagnostic centre and sets its price.

### Request

```json
{
  "centre_id": 1,
  "test_id": 1,
  "price": 50000
}
```

### Response

```json
{
  "id": 1,
  "centre_id": 1,
  "test_id": 1,
  "price": 50000
}
```

The API prevents:

* Invalid centre IDs
* Invalid test IDs
* Negative prices
* Duplicate centre/test combinations

## `GET /centre-tests/`

Returns all centre-test pricing records.

## `GET /centre-tests/{centre_test_id}`

Returns a specific centre-test pricing record.

---

# Bookings

Bookings require JWT authentication.

## `POST /bookings/`

Creates a booking for the authenticated user.

### Request

```json
{
  "centre_test_id": 1,
  "appointment_at": "2026-10-15T10:00:00"
}
```

The booking amount is automatically taken from the configured price of the selected centre/test combination.

### Response

```json
{
  "id": 1,
  "centre_test_id": 1,
  "appointment_at": "2026-10-15T10:00:00",
  "amount": 50000,
  "status": "PENDING"
}
```

## `GET /bookings/`

Returns bookings belonging only to the authenticated user.

## `GET /bookings/{booking_id}`

Returns detailed information about a user's booking.

### Response

```json
{
  "id": 1,
  "centre_test_id": 1,
  "centre_name": "ABC Diagnostics",
  "test_name": "Complete Blood Count",
  "appointment_at": "2026-10-15T10:00:00",
  "amount": 50000,
  "status": "PENDING"
}
```

A user cannot access another user's booking.

---

# Payments

Payments are simulated for this assignment.

## `POST /payments/`

Creates a simulated payment for an authenticated user's pending booking.

### Successful Payment

Request:

```json
{
  "booking_id": 1,
  "success": true
}
```

Response:

```json
{
  "id": 1,
  "booking_id": 1,
  "amount": 50000,
  "status": "SUCCESS"
}
```

The booking status becomes `CONFIRMED`.

### Failed Payment

Request:

```json
{
  "booking_id": 1,
  "success": false
}
```

Response:

```json
{
  "id": 1,
  "booking_id": 1,
  "amount": 50000,
  "status": "FAILED"
}
```

The booking status becomes `FAILED`.

A payment cannot be created again for a booking that is no longer pending.

---

# Payment Webhook

## `POST /payments/webhook`

Simulates a payment provider webhook.

This endpoint does not require user authentication because it represents a callback from an external payment system.

### Successful Webhook

Request:

```json
{
  "event_id": "evt_success_001",
  "booking_id": 1,
  "status": "SUCCESS"
}
```

Response:

```json
{
  "message": "Webhook processed successfully",
  "event_id": "evt_success_001",
  "booking_id": 1,
  "status": "SUCCESS"
}
```

### Failed Webhook

Request:

```json
{
  "event_id": "evt_failed_001",
  "booking_id": 1,
  "status": "FAILED"
}
```

The associated booking becomes `FAILED`.

---

# Webhook Idempotency

Each webhook must contain a unique `event_id`.

If the same event is received again, it is not processed a second time.

Example:

```json
{
  "event_id": "evt_success_001",
  "booking_id": 1,
  "status": "SUCCESS"
}
```

Sending the same event again returns:

```json
{
  "message": "Webhook already processed",
  "event_id": "evt_success_001"
}
```

This prevents duplicate processing of the same payment event.

---

# Authentication Flow

The typical application flow is:

```text
User Signup
    ↓
User Login
    ↓
Receive JWT
    ↓
Access authenticated endpoints
    ↓
Create/List Diagnostic Centres
    ↓
Create/List Diagnostic Tests
    ↓
Configure Centre + Test + Price
    ↓
Create Booking
    ↓
Booking starts as PENDING
    ↓
Simulated Payment / Payment Webhook
    ↓
Booking becomes CONFIRMED or FAILED
```

---

# Error Handling

The API handles common invalid requests and resource errors.

Examples include:

* `400 Bad Request`
* `401 Unauthorized`
* `404 Not Found`
* `409 Conflict`
* `422 Unprocessable Entity`

Handled cases include:

* Invalid login credentials
* Duplicate username
* Duplicate email
* Missing authentication
* Invalid JWT
* Invalid centre ID
* Invalid test ID
* Invalid centre-test ID
* Negative price
* Duplicate centre/test combination
* Invalid booking ID
* Accessing another user's booking
* Paying another user's booking
* Duplicate payment
* Payment for a non-pending booking
* Invalid webhook status
* Invalid webhook booking
* Duplicate webhook event
* Webhook processing for a non-pending booking

---

# Testing

The project uses **pytest** for automated API testing.

A separate PostgreSQL database is used for tests so that test data does not affect the development database.

Test database:

```text
eve_healthcare_test_db
```

The test setup automatically cleans the test database before each test.

## Run Tests

From the project root:

```bash
pytest
```

Current automated test result:

```text
33 passed
```

---

# Test Coverage

## Authentication

* Health check
* User signup
* Duplicate username
* Duplicate email
* Invalid password
* Successful login
* Authenticated user profile
* Authentication failure handling

## Centre/Test Pricing

* Create pricing
* Duplicate centre/test
* List pricing
* Get pricing
* Invalid centre
* Invalid test
* Negative price
* Invalid pricing ID

## Bookings

* Create booking
* Correct booking amount
* List user bookings
* Booking details
* Invalid centre-test ID
* Authentication requirement
* User isolation
* Unauthorized booking access

## Payments

* Successful payment
* Failed payment
* Authentication requirement
* Invalid booking
* Unauthorized payment
* Duplicate payment prevention
* Successful webhook
* Failed webhook
* Invalid webhook status
* Invalid webhook booking
* Duplicate webhook event
* Webhook rejection for non-pending booking

---

# Security Considerations

The project includes the following security measures:

* Passwords are stored as bcrypt hashes rather than plain text.
* JWT authentication protects user-specific endpoints.
* Booking queries are restricted to the authenticated user.
* Payment creation verifies booking ownership.
* Sensitive environment variables are stored outside source code.
* Duplicate webhook events are tracked using unique event IDs.
* Database constraints are used for unique usernames, emails, centre/test combinations, payment bookings, and webhook event IDs.

---

# Assumptions

The following assumptions were made for this assignment:

1. A registered user is considered the patient making the booking.
2. Payment processing is simulated and does not connect to a real payment provider.
3. Diagnostic centre and test management endpoints are available without a separate admin role because the assignment does not define an admin authentication flow.
4. Prices are represented as integer values for simplicity.
5. Appointment scheduling does not integrate with an external calendar or scheduling provider.
6. The API focuses on the required booking and payment workflow rather than production-scale infrastructure.
7. JWT access tokens are used for authenticated API requests.

---

# Design Decisions

## SQLAlchemy

SQLAlchemy is used as the ORM to interact with PostgreSQL and keep database operations organized within the application layer.

## JWT

JWT provides stateless authentication for protected endpoints.

## Separate Centre-Test Table

A separate `centre_tests` table is used because the same diagnostic test can be offered by multiple diagnostic centres at different prices.

Example:

```text
Centre A + Blood Test = 500
Centre B + Blood Test = 650
```

This allows pricing to be associated with the centre/test combination instead of the diagnostic test itself.

## Webhook Event Tracking

Webhook events are stored separately using a unique `event_id`.

This allows the API to recognize duplicate events and avoid processing the same payment event multiple times.

## Payment State Handling

Bookings start in the `PENDING` state.

A successful payment or successful webhook changes the booking to `CONFIRMED`.

A failed payment or failed webhook changes the booking to `FAILED`.

Payment and webhook operations are prevented from processing a booking that is no longer pending.

---

# Future Improvements

If this service were developed further for a production environment, possible improvements would include:

* Admin authentication and role-based authorization
* Stronger password policies
* Appointment slot availability and conflict prevention
* Pagination for list endpoints
* Filtering and searching
* Database migrations using Alembic
* Redis for caching
* Celery/background jobs
* Rate limiting
* Structured application logging
* Improved payment state management
* Production payment provider integration
* Webhook signature verification
* More comprehensive integration tests
* CI/CD pipeline
* Production monitoring and error tracking
* API versioning
* Improved database indexing
* HTTPS and production security configuration

---

# Running the Project Locally

Quick start:

```bash
git clone https://github.com/UdaySama/eve-healthcare-backend.git
cd eve-healthcare-backend

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

Configure the PostgreSQL database and create the `.env` file in the project root.

Start the API:

```bash
uvicorn app.main:app --reload
```

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

Open ReDoc:

```text
http://127.0.0.1:8000/redoc
```

Run tests:

```bash
pytest
```

---

# Running with Docker

Build and start the complete application:

```bash
docker compose up --build
```

The Dockerized API is available at:

```text
http://127.0.0.1:8001
```

Swagger:

```text
http://127.0.0.1:8001/docs
```

ReDoc:

```text
http://127.0.0.1:8001/redoc
```

Health check:

```bash
curl http://127.0.0.1:8001/health
```

Expected response:

```json
{
  "status": "ok"
}
```

Stop the containers:

```bash
docker compose down
```

---

# Project Status

The core backend workflow is implemented, tested, documented, and Dockerized.

Current automated test result:

```text
33 passed
```

Implemented workflow:

```text
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
    ↓
Automated Tests
    ↓
Swagger / OpenAPI Documentation
    ↓
Docker / Docker Compose
```

---

# Author


## Note on Contributors

This repository shows two contributors on GitHub (**UdaySama** and **Udaykalse**).
Both accounts belong to the same person, **Uday Kalse**, the sole author of this project.

The duplicate happened because two GitHub accounts/emails were configured on my
laptop, so some commits were authored under a different Git identity. No one
else contributed to this assignment. All code, design decisions, and
implementation are my own work.

Developed for the **EVE Healthcare SDE Intern — Backend Engineering Assignment**.
