from fastapi import FastAPI
from app.routes.tests import router as tests_router
from app.routes.auth import router as auth_router
from app.routes.centres import router as centres_router
from app.routes.bookings import router as bookings_router
from app.routes.payments import router as payments_router
from app.routes.centre_tests import router as centre_tests_router

from app.models import (
    User,
    DiagnosticCentre,
    DiagnosticTest,
    CentreTest,
    Booking,
    Payment,
    PaymentWebhookEvent,
)

from app.database import Base, engine


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="EVE Healthcare API",
    version="1.0.0",
)


app.include_router(auth_router)
app.include_router(centres_router)
app.include_router(tests_router)
app.include_router(bookings_router)
app.include_router(payments_router)
app.include_router(centre_tests_router)




@app.get("/health")
def health_check():
    return {"status": "ok"}