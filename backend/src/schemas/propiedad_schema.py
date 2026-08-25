from typing import Optional
from pydantic import BaseModel, Field


class PropiedadBaseSchema(BaseModel):
    """Atributos compartidos de Propiedad"""
    titulo: str = Field(..., max_length=150, description="Título o nombre de la propiedad")
    direccion: str = Field(..., max_length=200, description="Dirección física de la propiedad")
    ciudad: str = Field(..., max_length=100, description="Ciudad donde se ubica")
    precio_noche: float = Field(..., gt=0, description="Precio por noche (debe ser mayor a 0)")
    capacidad: int = Field(..., gt=0, description="Cantidad máxima de huéspedes (debe ser mayor a 0)")
    imagen_url: Optional[str] = Field(None, description="URL de la imagen principal de la propiedad")


class PropiedadCreateSchema(PropiedadBaseSchema):
    """Schema de Entrada: Datos que envía el cliente para publicar una propiedad (HU2).
    
    Nota: anfitrion_id no se incluye aquí porque se obtiene
    directamente del token del usuario autenticado en el Router.
    """
    pass


class PropiedadResponseSchema(PropiedadBaseSchema):
    """Schema de Salida: Formato de respuesta para el Router"""
    id: int
    anfitrion_id: int

    class Config:
        from_attributes = True