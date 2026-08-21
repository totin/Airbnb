from pydantic import BaseModel
from datetime import date


class CreateReservaDTO(BaseModel):
    propiedad_id: int
    fecha_inicio: date
    fecha_fin: date


class ResponseReservaDTO(BaseModel):
    id: int
    propiedad_id: int
    huesped_id: int
    fecha_inicio: date
    fecha_fin: date
    estado: str
    total: float

    class Config:
        from_attributes = True