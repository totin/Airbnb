from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.db.connection import get_db
from src.db.models.transaccion_horas import TipoTransaccionHoras
from src.dtos.horas_dto import SaldoHorasResponseDTO, TransaccionHorasResponseDTO
from src.services.horas_service import HorasService

router = APIRouter(prefix="/usuarios", tags=["Horas"])


class OperacionHorasDTO(BaseModel):
    cantidad: int


@router.get("/{usuario_id}/horas", response_model=SaldoHorasResponseDTO)
def obtener_saldo(usuario_id: int, db: Session = Depends(get_db)):
    service = HorasService(db)
    try:
        return service.obtener_saldo(usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{usuario_id}/horas/sumar", response_model=SaldoHorasResponseDTO)
def sumar_horas(usuario_id: int, dto: OperacionHorasDTO, db: Session = Depends(get_db)):
    service = HorasService(db)
    try:
        return service.sumar_horas(
            usuario_id=usuario_id,
            cantidad=dto.cantidad,
            reserva_id=None,
            tipo=TipoTransaccionHoras.GANADA,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{usuario_id}/horas/gastar", response_model=SaldoHorasResponseDTO)
def gastar_horas(usuario_id: int, dto: OperacionHorasDTO, db: Session = Depends(get_db)):
    service = HorasService(db)
    try:
        return service.restar_horas(
            usuario_id=usuario_id,
            cantidad=dto.cantidad,
            reserva_id=None,
            tipo=TipoTransaccionHoras.GASTADA,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{usuario_id}/horas/historial", response_model=list[TransaccionHorasResponseDTO])
def historial(usuario_id: int, db: Session = Depends(get_db)):
    service = HorasService(db)
    return service.listar_historial(usuario_id)