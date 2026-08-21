from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.db.connection import get_db
from src.dtos.amenidad_dto import CreateAmenidadDTO, ResponseAmenidadDTO
from src.services.amenidad_service import AmenidadService

router = APIRouter(prefix="/amenidades", tags=["Amenidades"])


@router.get(
    "",
    response_model=list[ResponseAmenidadDTO],
    summary="Obtener todas las amenidades"
)
def listar_amenidades(db: Session = Depends(get_db)):
    """HU8: Obtiene el catálogo completo de amenidades para mostrar en los filtros o al crear propiedades."""
    amenidad_service = AmenidadService(db)
    return amenidad_service.obtener_todas()


@router.post(
    "",
    response_model=ResponseAmenidadDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva amenidad"
)
def crear_amenidad(
    amenidad_data: CreateAmenidadDTO,
    db: Session = Depends(get_db)
):
    """Permite agregar una nueva amenidad al catálogo (ej: 'Pileta', 'WiFi', 'Aire Acondicionado')."""
    amenidad_service = AmenidadService(db)
    return amenidad_service.crear_amenidad(amenidad_data)