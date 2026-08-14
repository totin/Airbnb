from pydantic import BaseModel
from datetime import datetime


class FavoritoCreate(BaseModel):
    propiedad_id: int


class FavoritoResponse(BaseModel):
    usuario_id: int
    propiedad_id: int
    fecha: datetime

    class Config:
        from_attributes = True