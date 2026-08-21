from pydantic import BaseModel, ConfigDict


class AmenidadCreateDTO(BaseModel):
    nombre: str


class AmenidadResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str