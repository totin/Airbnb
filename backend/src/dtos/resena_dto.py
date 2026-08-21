from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ResenaCreateDTO(BaseModel):
    reserva_id: int
    autor_id: int
    puntaje: int = Field(ge=1, le=5)
    comentario: Optional[str] = None


class ResenaResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    reserva_id: int
    autor_id: int
    puntaje: int
    comentario: Optional[str] = None
    fecha: date