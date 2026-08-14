from pydantic import BaseModel, Field


class CreatePropiedadDTO(BaseModel): 
    titulo: str
    direccion: str
    ciudad: str
    precio_noche: float = Field(..., gt=0, description="El precio debe ser mayor a 0")
    capacidad: int = Field(..., gt=0, description="La capacidad debe ser mayor a 0")
    anfitrion_id: int


class UpdatePropiedadDTO(BaseModel): 
    titulo: str | None = None
    direccion: str | None = None
    ciudad: str | None = None
    precio_noche: float | None = Field(None, gt=0)
    capacidad: int | None = Field(None, gt=0)


class DeletePropiedadDTO(BaseModel):  
    id: int


class GetPropiedadDTO(BaseModel):  
    id: int


class PropiedadResponseDTO(BaseModel):  
    id: int
    titulo: str
    direccion: str
    ciudad: str
    precio_noche: float
    capacidad: int
    anfitrion_id: int

    model_config = {"from_attributes": True}