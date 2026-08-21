from pydantic import BaseModel


class CreatePropiedadAmenidadDTO(BaseModel):
    propiedad_id: int
    amenidad_id: int