from pydantic import BaseModel, ConfigDict
from typing import Optional, Any


class LugarTuristicoDTO(BaseModel):
    id: str
    nombre: str
    ciudad: str
    descripcion: str
    categoria: str
    lat: float
    lng: float

    model_config = ConfigDict(from_attributes=True)


class LugarCercanoDTO(LugarTuristicoDTO):
    distancia_km: float


class LugarConCercanasDTO(LugarTuristicoDTO):
    cercanas: list[Any] = []
