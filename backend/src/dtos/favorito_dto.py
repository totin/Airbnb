from pydantic import BaseModel
from datetime import datetime


class CreateFavoritoDTO(BaseModel):
    usuario_id: int
    propiedad_id: int


class FavoritoResponseDTO(BaseModel):
    usuario_id: int
    propiedad_id: int
    fecha: datetime

    class Config:
        from_attributes = True