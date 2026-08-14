from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from dto.resena import (
    ResenaCreate,
    ResenaResponse
)
from services.resena import ResenaService


router = APIRouter(
    prefix="/resenas",
    tags=["Reseñas"]
)


@router.post(
    "",
    response_model=ResenaResponse,
    status_code=201
)
def crear_resena(
    resena: ResenaCreate,
    autor_id: int,
    db: Session = Depends(get_db)
):
    service = ResenaService(db)

    return service.crear_resena(
        resena,
        autor_id
    )