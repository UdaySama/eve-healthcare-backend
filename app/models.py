from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, DateTime

from app.database import Base


# here all model's
# usermodel
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)

# DiagnosticCentre model
class DiagnosticCentre(Base):
    __tablename__ = "diagnostic_centres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)


class DiagnosticTest(Base):
    __tablename__ = "diagnostic_tests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)


class CentreTest(Base):
    __tablename__ = "centre_tests"

    id = Column(Integer, primary_key=True, index=True)
    centre_id = Column(
        Integer,
        ForeignKey("diagnostic_centres.id"),
        nullable=False,
    )
    test_id = Column(
        Integer,
        ForeignKey("diagnostic_tests.id"),
        nullable=False,
    )
    price = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "centre_id",
            "test_id",
            name="uq_centre_test",
        ),
    )


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )
    centre_test_id = Column(
        Integer,
        ForeignKey("centre_tests.id"),
        nullable=False,
    )
    appointment_at = Column(DateTime, nullable=False)
    amount = Column(Integer, nullable=False)
    status = Column(
        String,
        nullable=False,
        default="PENDING",
    )


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(
        Integer,
        ForeignKey("bookings.id"),
        nullable=False,
        unique=True,
    )
    amount = Column(Integer, nullable=False)
    status = Column(String, nullable=False)


class PaymentWebhookEvent(Base):
    __tablename__ = "payment_webhook_events"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )
    payment_id = Column(
        Integer,
        ForeignKey("payments.id"),
        nullable=False,
    )
    status = Column(String, nullable=False)