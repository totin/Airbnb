from datetime import date
from pydantic import BaseModel, Field


class UsuarioBaseSchema(BaseModel):
    """Atributos compartidos por los esquemas de Usuario"""
    email: str = Field(..., max_length=150, description="Correo electrónico único del usuario")
    nombre: str = Field(..., max_length=100, description="Nombre completo del usuario")
    es_anfitrion: bool = Field(default=False, description="Indica si el usuario publica propiedades")


class UsuarioCreateSchema(UsuarioBaseSchema):
    """Schema de Entrada: Se usa en el Router para validar los datos al registrarse"""
    pass


class UsuarioResponseSchema(UsuarioBaseSchema):
    """Schema de Salida: Se usa en el response_model del Router para devolver los datos"""
    id: int
    fecha_registro: date

    class Config:
        from_attributes = True