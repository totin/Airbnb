from datetime import date
from typing import Literal
from pydantic import BaseModel, Field, model_validator


class ReservaBaseSchema(BaseModel):
    """Atributos compartidos de Reserva"""
    fecha_inicio: date = Field(..., description="Fecha de inicio de la estancia")
    fecha_fin: date = Field(..., description="Fecha de fin de la estancia")

    @model_validator(mode="after")
    def validar_fechas(self):
        """Valida que fecha_fin sea estrictamente posterior a fecha_inicio (chk_fechas_reserva)"""
        if self.fecha_fin <= self.fecha_inicio:
            raise ValueError("La fecha_fin debe ser posterior a la fecha_inicio.")
        return self


class ReservaCreateSchema(ReservaBaseSchema):
    """Schema de Entrada: Datos necesarios para crear una reserva (HU4).
    
    Nota: huesped_id no va aquí porque se extrae del Token de sesión.
    """
    propiedad_id: int = Field(..., description="ID de la propiedad a reservar")


class ReservaResponseSchema(ReservaBaseSchema):
    """Schema de Salida: Formato de respuesta con el detalle completo de la reserva"""
    id: int
    propiedad_id: int
    huesped_id: int
    estado: Literal["pendiente", "confirmada", "cancelada", "finalizada"]
    total: float = Field(..., ge=0, description="Precio total calculado de la reserva")

    class Config:
        from_attributes = True