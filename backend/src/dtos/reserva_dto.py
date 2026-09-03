from datetime import date
from typing import Optional, Any
from pydantic import BaseModel, ConfigDict
from src.db.models.reserva import MetodoPago
from src.dtos.usuario_dto import UsuarioResponseDTO


class ReservaCreateDTO(BaseModel):
    propiedad_id: int
    huesped_id: int
    fecha_inicio: date
    fecha_fin: date
    metodo_pago: str = MetodoPago.DINERO.value


class ReservaCambioEstadoDTO(BaseModel):
    estado: str
    actor_id: Optional[int] = None


class ReservaResponseDTO(BaseModel):
    id: int
    propiedad_id: int
    huesped_id: int
    fecha_inicio: date
    fecha_fin: date
    estado: str
    total: float
    metodo_pago: str = MetodoPago.DINERO.value
    horas_utilizadas: Optional[int] = None
    horas_ganadas: Optional[int] = None
    propiedad: Optional[Any] = None
    anfitrion: Optional[UsuarioResponseDTO] = None
    huesped: Optional[UsuarioResponseDTO] = None
    tiene_resena: bool = False

    model_config = ConfigDict(from_attributes=True)