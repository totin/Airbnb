from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from dto.favorito import FavoritoResponse
from services.favorito import FavoritoService


router = APIRouter(
    prefix="/favoritos",
    tags=["Favoritos"]
)


@router.post(
    "/{usuario_id}/{propiedad_id}",
    response_model=FavoritoResponse,
    status_code=201
)
def agregar_favorito(
    usuario_id: int,
    propiedad_id: int,
    db: Session = Depends(get_db)
):
    service = FavoritoService(db)

    return service.agregar_favorito(
        usuario_id,
        propiedad_id
    )