from pydantic import BaseModel, Field
from datetime import date


class CreateResenaDTO(BaseModel):
    reserva_id: int
    puntaje: int = Field(ge=1, le=5)
    comentario: str


class ResponseResenaDTO(BaseModel):
    id: int
    reserva_id: int
    autor_id: int
    puntaje: int
    comentario: str
    fecha: date

    class Config:
        from_attributes = True