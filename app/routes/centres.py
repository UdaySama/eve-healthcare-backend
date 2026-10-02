from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import DiagnosticCentre
from app.schemas import (
    DiagnosticCentreCreate,
    DiagnosticCentreResponse,
)


router = APIRouter(
    prefix="/centres",
    tags=["Diagnostic Centres"],
)


@router.post(
    "/",
    response_model=DiagnosticCentreResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_centre(
    centre_data: DiagnosticCentreCreate,
    db: Session = Depends(get_db),
):
    new_centre = DiagnosticCentre(
        name=centre_data.name,
        location=centre_data.location,
    )

    db.add(new_centre)
    db.commit()
    db.refresh(new_centre)

    return new_centre


@router.get(
    "/",
    response_model=List[DiagnosticCentreResponse],
)
def get_centres(db: Session = Depends(get_db)):
    centres = db.query(DiagnosticCentre).all()

    return centres

@router.get(
    "/{centre_id}",
    response_model=DiagnosticCentreResponse,
)
def get_centre(
    centre_id: int,
    db: Session = Depends(get_db),
):
    centre = db.query(DiagnosticCentre).filter(
        DiagnosticCentre.id == centre_id
    ).first()

    if centre is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diagnostic centre not found",
        )

    return centre