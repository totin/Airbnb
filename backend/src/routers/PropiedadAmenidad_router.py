from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.connection import get_db
from src.dtos.propiedad_amenidad_dto import (
    PropiedadAmenidadCreateDTO,
    PropiedadAmenidadesBulkDTO,
    PropiedadAmenidadResponseDTO,
)
from src.services.prop_amen_service import PropiedadAmenidadService

router = APIRouter(prefix="/propiedades-amenidades", tags=["Propiedades - Amenidades"])


@router.post("", response_model=PropiedadAmenidadResponseDTO, status_code=status.HTTP_201_CREATED)
def asociar_amenidad(dto: PropiedadAmenidadCreateDTO, db: Session = Depends(get_db)):
    service = PropiedadAmenidadService(db)
    try:
        return service.asociar_amenidad(
            propiedad_id=dto.propiedad_id,
            amenidad_id=dto.amenidad_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/masivo", status_code=status.HTTP_201_CREATED)
def asociar_multiples_amenidades(dto: PropiedadAmenidadesBulkDTO, db: Session = Depends(get_db)):
    service = PropiedadAmenidadService(db)
    try:
        service.asociar_multiples_amenidades(
            propiedad_id=dto.propiedad_id,
            amenidades_ids=dto.amenidades_ids
        )
        return {"message": "Amenidades asociadas correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/propiedad/{propiedad_id}/amenidad/{amenidad_id}", status_code=status.HTTP_200_OK)
def desasociar_amenidad(propiedad_id: int, amenidad_id: int, db: Session = Depends(get_db)):
    service = PropiedadAmenidadService(db)
    try:
        service.desasociar_amenidad(propiedad_id=propiedad_id, amenidad_id=amenidad_id)
        return {"message": "Amenidad removida de la propiedad correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))