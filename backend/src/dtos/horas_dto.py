from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SaldoHorasResponseDTO(BaseModel):
    usuario_id: int
    horas: int

    class Config:
        from_attributes = True


class TransaccionHorasResponseDTO(BaseModel):
    id: int
    tipo: str
    cantidad: int
    fecha: datetime
    reserva_id: Optional[int]

    class Config:
        from_attributes = True