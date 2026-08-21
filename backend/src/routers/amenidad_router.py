from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.connection import get_db
from src.dtos.amenidad_dto import AmenidadCreateDTO, AmenidadResponseDTO
from src.services.amenidad_service import AmenidadService

router = APIRouter(prefix="/amenidades", tags=["Amenidades"])


@router.post("", response_model=AmenidadResponseDTO, status_code=status.HTTP_201_CREATED)
def crear_amenidad(dto: AmenidadCreateDTO, db: Session = Depends(get_db)):
    service = AmenidadService(db)
    try:
        return service.crear_amenidad(nombre=dto.nombre)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[AmenidadResponseDTO])
def listar_amenidades(db: Session = Depends(get_db)):
    service = AmenidadService(db)
    return service.listar_todas()


@router.get("/{amenidad_id}", response_model=AmenidadResponseDTO)
def obtener_amenidad(amenidad_id: int, db: Session = Depends(get_db)):
    service = AmenidadService(db)
    try:
        return service.obtener_por_id(amenidad_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))