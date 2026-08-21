from pydantic import BaseModel, Field


class PropiedadAmenidadBaseSchema(BaseModel):
    """Atributos de la tabla intermedia propiedad_amenidades"""
    propiedad_id: int = Field(..., description="ID de la propiedad")
    amenidad_id: int = Field(..., description="ID de la amenidad")


class PropiedadAmenidadCreateSchema(PropiedadAmenidadBaseSchema):
    """Schema de Entrada: Datos para asociar una amenidad a una propiedad"""
    pass


class PropiedadAmenidadResponseSchema(PropiedadAmenidadBaseSchema):
    """Schema de Salida: Devuelve la relación creada"""

    class Config:
        from_attributes = True