from datetime import date
from typing import Optional
from pydantic import BaseModel
from src.db.models.reserva import MetodoPago


class ReservaCreateDTO(BaseModel):
    propiedad_id: int
    huesped_id: int
    fecha_inicio: date
    fecha_fin: date
    metodo_pago: MetodoPago = MetodoPago.DINERO


class ReservaResponseDTO(BaseModel):
    id: int
    propiedad_id: int
    huesped_id: int
    fecha_inicio: date
    fecha_fin: date
    estado: str
    total: float
    metodo_pago: str
    horas_utilizadas: Optional[int]
    horas_ganadas: Optional[int]

    class Config:
        from_attributes = True