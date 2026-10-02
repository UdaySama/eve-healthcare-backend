from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import DiagnosticTest
from app.schemas import (
    DiagnosticTestCreate,
    DiagnosticTestResponse,
)


router = APIRouter(
    prefix="/tests",
    tags=["Diagnostic Tests"],
)


@router.post(
    "/",
    response_model=DiagnosticTestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_test(
    test_data: DiagnosticTestCreate,
    db: Session = Depends(get_db),
):
    new_test = DiagnosticTest(
        name=test_data.name,
    )

    db.add(new_test)
    db.commit()
    db.refresh(new_test)

    return new_test


@router.get(
    "/",
    response_model=List[DiagnosticTestResponse],
)
def get_tests(db: Session = Depends(get_db)):
    tests = db.query(DiagnosticTest).all()

    return tests


@router.get(
    "/{test_id}",
    response_model=DiagnosticTestResponse,
)
def get_test(
    test_id: int,
    db: Session = Depends(get_db),
):
    test = db.query(DiagnosticTest).filter(
        DiagnosticTest.id == test_id
    ).first()

    if test is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diagnostic test not found",
        )

    return test