from typing import Optional, Any
from pydantic import BaseModel, Field, ConfigDict
from src.dtos.usuario_dto import UsuarioResponseDTO


class PropiedadImagenDTO(BaseModel):
    id: int
    url: str
    orden: int
    es_portada: bool

    model_config = ConfigDict(from_attributes=True)


class PropiedadCreateDTO(BaseModel):
    titulo: str
    direccion: str
    ciudad: str
    precio_noche: float
    capacidad: int
    anfitrion_id: int
    amenidades: list[Any] = Field(default_factory=list)  # IDs o nombres de amenidades
    imagenes: list[str] = Field(default_factory=list)  # data URLs o URLs
    lat: Optional[float] = None
    lng: Optional[float] = None


class PropiedadUpdateDTO(BaseModel):
    titulo: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    precio_noche: Optional[float] = None
    capacidad: Optional[int] = None
    amenidades: Optional[list[Any]] = None
    imagenes: Optional[list[str]] = None
    lat: Optional[float] = None
    lng: Optional[float] = None


class AsociarAmenidadesDTO(BaseModel):
    amenidades_ids: list[int]


class AgregarImagenesDTO(BaseModel):
    imagenes: list[str]


class PropiedadResponseDTO(BaseModel):
    id: int
    titulo: str
    direccion: str
    ciudad: str
    precio_noche: float
    capacidad: int
    anfitrion_id: int
    lat: Optional[float] = None
    lng: Optional[float] = None
    imagenes: list[str] = Field(default_factory=list)
    amenidades: list[str] = Field(default_factory=list)
    amenidades_nombres: list[str] = Field(default_factory=list)
    promedio_puntaje: Optional[float] = None
    cantidad_resenas: int = 0
    anfitrion: Optional[UsuarioResponseDTO] = None

    model_config = ConfigDict(from_attributes=True)