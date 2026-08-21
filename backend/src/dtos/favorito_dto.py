from datetime import datetime
from pydantic import BaseModel, ConfigDict


class FavoritoCreateDTO(BaseModel):
    usuario_id: int
    propiedad_id: int


class FavoritoResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    usuario_id: int
    propiedad_id: int
    fecha: datetime