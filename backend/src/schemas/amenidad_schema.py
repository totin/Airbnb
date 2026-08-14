from pydantic import BaseModel, Field


class AmenidadBaseSchema(BaseModel):
    """Atributos compartidos de Amenidad"""
    nombre: str = Field(..., max_length=100, description="Nombre de la amenidad (único)")


class AmenidadCreateSchema(AmenidadBaseSchema):
    """Schema de Entrada: Datos necesarios para crear una nueva amenidad"""
    pass


class AmenidadResponseSchema(AmenidadBaseSchema):
    """Schema de Salida: Formato de respuesta para devolver la amenidad con su ID"""
    id: int

    class Config:
        from_attributes = True