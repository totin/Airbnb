from datetime import date
from pydantic import BaseModel, Field


class FavoritoBaseSchema(BaseModel):
    """Atributos compartidos para Favoritos"""
    propiedad_id: int = Field(..., description="ID de la propiedad guardada como favorita")


class FavoritoCreateSchema(FavoritoBaseSchema):
    """Schema de Entrada: Datos que envía el cliente para agregar a favoritos (HU7).
    
    Nota: usuario_id no se incluye aquí porque se extrae
    directamente del token de autenticación en el Router.
    """
    pass


class FavoritoResponseSchema(FavoritoBaseSchema):
    """Schema de Salida: Formato de respuesta para devolver el favorito creado o guardado"""
    usuario_id: int
    fecha: date

    class Config:
        from_attributes = True