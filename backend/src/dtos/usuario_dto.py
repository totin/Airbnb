from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class UsuarioCreateDTO(BaseModel):
    email: EmailStr
    nombre: str
    es_anfitrion: bool = False


class UsuarioResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    nombre: str
    fecha_registro: datetime
    es_anfitrion: bool