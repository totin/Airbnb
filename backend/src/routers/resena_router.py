from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.connection import get_db
from src.dtos.resena_dto import ResenaCreateDTO, ResenaResponseDTO
from src.services.resena_service import ResenaService

router = APIRouter(prefix="/resenas", tags=["Reseñas"])


@router.post("", response_model=ResenaResponseDTO, status_code=status.HTTP_201_CREATED)
def crear_resena(dto: ResenaCreateDTO, db: Session = Depends(get_db)):
    service = ResenaService(db)
    try:
        return service.crear_resena(
            reserva_id=dto.reserva_id,
            autor_id=dto.autor_id,
            puntaje=dto.puntaje,
            comentario=dto.comentario
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{resena_id}", response_model=ResenaResponseDTO)
def obtener_resena(resena_id: int, db: Session = Depends(get_db)):
    service = ResenaService(db)
    try:
        return service.obtener_por_id(resena_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/propiedad/{propiedad_id}", response_model=list[ResenaResponseDTO])
def listar_por_propiedad(propiedad_id: int, db: Session = Depends(get_db)):
    service = ResenaService(db)
    return service.listar_por_propiedad(propiedad_id)