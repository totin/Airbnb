from datetime import date
from pydantic import BaseModel


class CreateUsuarioDTO(BaseModel):
    nombre: str
    email: str
    es_anfitrion: bool = False

class UsuarioResponseDTO(BaseModel):
    id: int
    nombre: str
    email: str
    fecha_registro: date
    es_anfitrion: bool

    model_config = {"from_attributes": True}
