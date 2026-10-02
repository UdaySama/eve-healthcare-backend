# import os

# os.environ["DATABASE_URL"] = (
#     "postgresql://eve_app:eve_dev_password@localhost:5432/eve_healthcare_test_db"
# )

# from fastapi.testclient import TestClient

# from app.main import app


# client = TestClient(app)


import os

import pytest
from sqlalchemy import text

os.environ["DATABASE_URL"] = (
    "postgresql://eve_app:eve_dev_password@localhost:5432/eve_healthcare_test_db"
)


@pytest.fixture(autouse=True)
def clean_test_database():
    from app.database import engine

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                TRUNCATE TABLE
                    payment_webhook_events,
                    payments,
                    bookings,
                    centre_tests,
                    diagnostic_centres,
                    diagnostic_tests,
                    users
                RESTART IDENTITY CASCADE;
                """
            )
        )
