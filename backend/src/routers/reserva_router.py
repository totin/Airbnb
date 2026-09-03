from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from src.db.connection import get_db
from src.dtos.reserva_dto import ReservaCreateDTO, ReservaResponseDTO, ReservaCambioEstadoDTO
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
            fecha_fin=dto.fecha_fin,
            metodo_pago=dto.metodo_pago,
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
def listar_por_huesped(
    huesped_id: int,
    estado: Optional[str] = Query(None, description="Filtro opcional por estado"),
    db: Session = Depends(get_db),
):
    service = ReservaService(db)
    return service.listar_por_huesped(huesped_id, estado=estado)


@router.get("/anfitrion/{anfitrion_id}", response_model=list[ReservaResponseDTO])
def listar_por_anfitrion(anfitrion_id: int, db: Session = Depends(get_db)):
    service = ReservaService(db)
    return service.listar_por_anfitrion(anfitrion_id)


@router.patch("/{reserva_id}/estado", response_model=ReservaResponseDTO)
def cambiar_estado_reserva(
    reserva_id: int,
    dto: ReservaCambioEstadoDTO,
    db: Session = Depends(get_db),
):
    service = ReservaService(db)
    try:
        return service.cambiar_estado_reserva(
            reserva_id=reserva_id,
            nuevo_estado=dto.estado,
            actor_id=dto.actor_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{reserva_id}/cancelar", response_model=ReservaResponseDTO)
def cancelar_reserva(
    reserva_id: int,
    usuario_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    service = ReservaService(db)
    try:
        return service.cancelar_reserva(reserva_id, usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))