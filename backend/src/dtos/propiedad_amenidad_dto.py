from pydantic import BaseModel


class PropiedadAmenidadCreate(BaseModel):
    propiedad_id: int
    amenidad_id: int