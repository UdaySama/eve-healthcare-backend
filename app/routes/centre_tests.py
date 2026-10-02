from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import CentreTest, DiagnosticCentre, DiagnosticTest
from app.schemas import CentreTestCreate, CentreTestResponse


router = APIRouter(
    prefix="/centre-tests",
    tags=["Centre Tests & Pricing"],
)


@router.post(
    "/",
    response_model=CentreTestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_centre_test(
    data: CentreTestCreate,
    db: Session = Depends(get_db),
):
    centre = db.query(DiagnosticCentre).filter(
        DiagnosticCentre.id == data.centre_id
    ).first()

    if centre is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diagnostic centre not found",
        )

    test = db.query(DiagnosticTest).filter(
        DiagnosticTest.id == data.test_id
    ).first()

    if test is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diagnostic test not found",
        )

    if data.price < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Price cannot be negative",
        )

    existing = db.query(CentreTest).filter(
        CentreTest.centre_id == data.centre_id,
        CentreTest.test_id == data.test_id,
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Test is already available at this centre",
        )

    centre_test = CentreTest(
        centre_id=data.centre_id,
        test_id=data.test_id,
        price=data.price,
    )

    db.add(centre_test)
    db.commit()
    db.refresh(centre_test)

    return centre_test


@router.get(
    "/",
    response_model=List[CentreTestResponse],
)
def get_centre_tests(
    db: Session = Depends(get_db),
):
    return db.query(CentreTest).all()


@router.get(
    "/{centre_test_id}",
    response_model=CentreTestResponse,
)
def get_centre_test(
    centre_test_id: int,
    db: Session = Depends(get_db),
):
    centre_test = db.query(CentreTest).filter(
        CentreTest.id == centre_test_id
    ).first()

    if centre_test is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Centre test not found",
        )

    return centre_test