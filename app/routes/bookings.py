from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import (
    Booking,
    CentreTest,
    DiagnosticCentre,
    DiagnosticTest,
    User,
)
from app.schemas import BookingCreate, BookingResponse, BookingDetailResponse


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.post(
    "/",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_booking(
    booking_data: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    centre_test = db.query(CentreTest).filter(
        CentreTest.id == booking_data.centre_test_id
    ).first()

    if centre_test is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Centre test not found",
        )

    new_booking = Booking(
        user_id=current_user.id,
        centre_test_id=booking_data.centre_test_id,
        appointment_at=booking_data.appointment_at,
        amount=centre_test.price,
        status="PENDING",
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return new_booking


@router.get(
    "/",
    response_model=List[BookingResponse],
)
def get_user_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    bookings = db.query(Booking).filter(
        Booking.user_id == current_user.id
    ).all()

    return bookings


@router.get(
    "/{booking_id}",
    response_model=BookingDetailResponse,
)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    booking = db.query(
        Booking,
        DiagnosticCentre.name,
        DiagnosticTest.name,
    ).join(
        CentreTest,
        Booking.centre_test_id == CentreTest.id,
    ).join(
        DiagnosticCentre,
        CentreTest.centre_id == DiagnosticCentre.id,
    ).join(
        DiagnosticTest,
        CentreTest.test_id == DiagnosticTest.id,
    ).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.id,
    ).first()

    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    booking_data, centre_name, test_name = booking

    return {
        "id": booking_data.id,
        "centre_test_id": booking_data.centre_test_id,
        "centre_name": centre_name,
        "test_name": test_name,
        "appointment_at": booking_data.appointment_at,
        "amount": booking_data.amount,
        "status": booking_data.status,
    }