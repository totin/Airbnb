from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.connection import get_db
from src.dtos.reserva_dto import ReservaCreateDTO, ReservaResponseDTO
from src.services.reserva_service import ReservaService

router = APIRouter(prefix="/reservas", tags=["Reservas"])


@router.post("", response_model=ReservaResponseDTO, status_code=status.HTTP_201_CREATED)
def crear_reserva(dto: ReservaCreateDTO, db: Session = Depends(get_db)):
    service = ReservaService(db)
    try:
        return service.crear_reserva(
            propiedad_id=dto.propiedad_id,
            huesped_id=dto.huesped_id,
            fecha_inicio=dto.fecha_inicio,
            fecha_fin=dto.fecha_fin
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{reserva_id}", response_model=ReservaResponseDTO)
def obtener_reserva(reserva_id: int, db: Session = Depends(get_db)):
    service = ReservaService(db)
    try:
        return service.obtener_por_id(reserva_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/huesped/{huesped_id}", response_model=list[ReservaResponseDTO])
def listar_por_huesped(huesped_id: int, db: Session = Depends(get_db)):
    service = ReservaService(db)
    return service.listar_por_huesped(huesped_id)


@router.patch("/{reserva_id}/cancelar", response_model=ReservaResponseDTO)
def cancelar_reserva(reserva_id: int, usuario_id: int, db: Session = Depends(get_db)):
    service = ReservaService(db)
    try:
        return service.cancelar_reserva(reserva_id, usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))