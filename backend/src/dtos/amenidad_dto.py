from pydantic import BaseModel


class CreateAmenidadDTO(BaseModel):
    nombre: str


class ResponseAmenidadDTO(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True