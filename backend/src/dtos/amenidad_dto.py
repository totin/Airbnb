from pydantic import BaseModel


class AmenidadCreate(BaseModel):
    nombre: str


class AmenidadResponse(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True