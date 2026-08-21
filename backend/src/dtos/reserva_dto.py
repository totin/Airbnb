from datetime import date
from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from src.db.models.reserva import EstadoReserva


class ReservaCreateDTO(BaseModel):
    propiedad_id: int
    huesped_id: int
    fecha_inicio: date
    fecha_fin: date


class ReservaResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    propiedad_id: int
    huesped_id: int
    fecha_inicio: date
    fecha_fin: date
    estado: EstadoReserva
    total: Decimal