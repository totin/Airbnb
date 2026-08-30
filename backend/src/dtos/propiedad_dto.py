from typing import Optional
from pydantic import BaseModel, Field


class PropiedadImagenDTO(BaseModel):
    id: int
    url: str
    orden: int
    es_portada: bool

    class Config:
        from_attributes = True


class PropiedadCreateDTO(BaseModel):
    titulo: str
    direccion: str
    ciudad: str
    precio_noche: float
    capacidad: int
    anfitrion_id: int
    imagenes: list[str] = Field(default_factory=list)  # base64 data URLs, orden = índice


class PropiedadUpdateDTO(BaseModel):
    titulo: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    precio_noche: Optional[float] = None
    capacidad: Optional[int] = None


class AsociarAmenidadesDTO(BaseModel):
    amenidades_ids: list[int]


class AgregarImagenesDTO(BaseModel):
    imagenes: list[str]  # base64 data URLs a agregar


class PropiedadResponseDTO(BaseModel):
    id: int
    titulo: str
    direccion: str
    ciudad: str
    precio_noche: float
    capacidad: int
    anfitrion_id: int
    imagenes: list[PropiedadImagenDTO] = []

    class Config:
        from_attributes = True