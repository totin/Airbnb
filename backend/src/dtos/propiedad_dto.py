from pydantic import BaseModel, Field, ConfigDict


class PropiedadCreateDTO(BaseModel):
    titulo: str
    direccion: str
    ciudad: str
    precio_noche: float = Field(gt=0)
    capacidad: int = Field(gt=0)
    anfitrion_id: int


class PropiedadResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    direccion: str
    ciudad: str
    precio_noche: float
    capacidad: int
    anfitrion_id: int


class AsociarAmenidadesDTO(BaseModel):
    amenidades_ids: list[int]