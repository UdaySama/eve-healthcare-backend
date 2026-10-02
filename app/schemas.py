from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserSignup(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class DiagnosticCentreCreate(BaseModel):
    name: str
    location: str


class DiagnosticCentreResponse(BaseModel):
    id: int
    name: str
    location: str


class DiagnosticTestCreate(BaseModel):
    name: str


class DiagnosticTestResponse(BaseModel):
    id: int
    name: str



class BookingCreate(BaseModel):
    centre_test_id: int
    appointment_at: datetime


class BookingResponse(BaseModel):
    id: int
    centre_test_id: int
    appointment_at: datetime
    amount: int
    status: str


class BookingDetailResponse(BaseModel):
    id: int
    centre_test_id: int
    centre_name: str
    test_name: str
    appointment_at: datetime
    amount: int
    status: str


class PaymentCreate(BaseModel):
    booking_id: int
    success: bool


class PaymentResponse(BaseModel):
    id: int
    booking_id: int
    amount: int
    status: str

class PaymentWebhookRequest(BaseModel):
    event_id: str
    booking_id: int
    status: str

class CentreTestCreate(BaseModel):
    centre_id: int
    test_id: int
    price: int


class CentreTestResponse(BaseModel):
    id: int
    centre_id: int
    test_id: int
    price: int