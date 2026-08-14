from datetime import date
from pydantic import BaseModel, Field


class ResenaBaseSchema(BaseModel):
    """Atributos compartidos de Reseña"""
    puntaje: int = Field(
        ..., 
        ge=1, 
        le=5, 
        description="Puntaje de la calificación (debe ser un número entero entre 1 y 5)"
    )
    comentario: str | None = Field(
        default=None, 
        description="Comentario de la reseña (opcional)"
    )


class ResenaCreateSchema(ResenaBaseSchema):
    """Schema de Entrada: Datos necesarios para enviar una reseña (HU6).
    
    Nota: autor_id no va aquí porque se obtiene directamente del Token de sesión del usuario.
    """
    reserva_id: int = Field(..., description="ID de la reserva que se está calificando")


class ResenaResponseSchema(ResenaBaseSchema):
    """Schema de Salida: Formato de respuesta para el Router"""
    id: int
    reserva_id: int
    autor_id: int
    fecha: date

    class Config:
        from_attributes = True