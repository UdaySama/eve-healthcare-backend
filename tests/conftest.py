import os

import pytest
from dotenv import load_dotenv
from sqlalchemy import text

load_dotenv()

os.environ["DATABASE_URL"] = os.environ["TEST_DATABASE_URL"]


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
