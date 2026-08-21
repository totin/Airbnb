from pydantic import BaseModel, ConfigDict


class PropiedadAmenidadCreateDTO(BaseModel):
    propiedad_id: int
    amenidad_id: int


class PropiedadAmenidadesBulkDTO(BaseModel):
    propiedad_id: int
    amenidades_ids: list[int]


class PropiedadAmenidadResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    propiedad_id: int
    amenidad_id: int