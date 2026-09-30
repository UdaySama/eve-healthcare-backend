from fastapi import FastAPI

from app.routes.auth import router as auth_router

from app.models import (
    User,
    DiagnosticCentre,
    DiagnosticTest,
    CentreTest,
    Booking,
)

from app.database import Base, engine


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="EVE Healthcare API",
    version="1.0.0",
)


app.include_router(auth_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}