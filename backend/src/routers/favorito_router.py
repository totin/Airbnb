from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.connection import get_db
from src.dtos.favorito_dto import FavoritoCreateDTO, FavoritoResponseDTO
from src.services.favorito_service import FavoritoService

router = APIRouter(prefix="/favoritos", tags=["Favoritos"])


@router.post("", response_model=FavoritoResponseDTO, status_code=status.HTTP_201_CREATED)
def agregar_favorito(dto: FavoritoCreateDTO, db: Session = Depends(get_db)):
    service = FavoritoService(db)
    try:
        return service.agregar_favorito(
            usuario_id=dto.usuario_id,
            propiedad_id=dto.propiedad_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("", status_code=status.HTTP_200_OK)
def eliminar_favorito(usuario_id: int, propiedad_id: int, db: Session = Depends(get_db)):
    service = FavoritoService(db)
    try:
        service.eliminar_favorito(usuario_id=usuario_id, propiedad_id=propiedad_id)
        return {"message": "Favorito eliminado correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/usuario/{usuario_id}", response_model=list[FavoritoResponseDTO])
def listar_favoritos(usuario_id: int, db: Session = Depends(get_db)):
    service = FavoritoService(db)
    try:
        return service.listar_favoritos_por_usuario(usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))