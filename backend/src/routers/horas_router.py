from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.connection import get_db
from src.dtos.horas_dto import SaldoHorasResponseDTO, TransaccionHorasResponseDTO
from src.services.horas_service import HorasService

router = APIRouter(prefix="/usuarios", tags=["Horas"])


@router.get("/{usuario_id}/horas", response_model=SaldoHorasResponseDTO)
def obtener_saldo(usuario_id: int, db: Session = Depends(get_db)):
    service = HorasService(db)
    try:
        return service.obtener_saldo(usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{usuario_id}/horas/historial", response_model=list[TransaccionHorasResponseDTO])
def historial(usuario_id: int, db: Session = Depends(get_db)):
    service = HorasService(db)
    return service.listar_historial(usuario_id)