from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Booking, Payment, PaymentWebhookEvent, User
from app.schemas import PaymentCreate, PaymentResponse, PaymentWebhookRequest


router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


@router.post(
    "/",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_payment(
    payment_data: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    booking = db.query(Booking).filter(
        Booking.id == payment_data.booking_id,
        Booking.user_id == current_user.id,
    ).first()

    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    if booking.status != "PENDING":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking is not pending",
        )

    existing_payment = db.query(Payment).filter(
        Payment.booking_id == booking.id
    ).first()

    if existing_payment:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Payment already exists for this booking",
        )

    payment_status = "SUCCESS" if payment_data.success else "FAILED"

    payment = Payment(
        booking_id=booking.id,
        amount=booking.amount,
        status=payment_status,
    )

    booking.status = (
        "CONFIRMED"
        if payment_data.success
        else "FAILED"
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment


@router.post("/webhook")
def payment_webhook(
    webhook_data: PaymentWebhookRequest,
    db: Session = Depends(get_db),
):
    # Check duplicate webhook event first.
    existing_event = db.query(PaymentWebhookEvent).filter(
        PaymentWebhookEvent.event_id == webhook_data.event_id
    ).first()

    if existing_event:
        return {
            "message": "Webhook already processed",
            "event_id": webhook_data.event_id,
        }

    # Validate payment status.
    if webhook_data.status not in ["SUCCESS", "FAILED"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid payment status",
        )

    # Find the booking.
    booking = db.query(Booking).filter(
        Booking.id == webhook_data.booking_id
    ).first()

    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    # Only pending bookings can receive a new payment webhook.
    if booking.status != "PENDING":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking is not pending",
        )

    # Find an existing payment for the booking.
    payment = db.query(Payment).filter(
        Payment.booking_id == booking.id
    ).first()

    if payment is None:
        payment = Payment(
            booking_id=booking.id,
            amount=booking.amount,
            status=webhook_data.status,
        )

        db.add(payment)
        db.flush()

    else:
        payment.status = webhook_data.status

    # Update booking status based on payment result.
    booking.status = (
        "CONFIRMED"
        if webhook_data.status == "SUCCESS"
        else "FAILED"
    )

    # Store the webhook event for idempotency.
    webhook_event = PaymentWebhookEvent(
        event_id=webhook_data.event_id,
        payment_id=payment.id,
        status=webhook_data.status,
    )

    db.add(webhook_event)
    db.commit()

    return {
        "message": "Webhook processed successfully",
        "event_id": webhook_data.event_id,
        "booking_id": booking.id,
        "status": webhook_data.status,
    }