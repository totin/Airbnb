from pydantic import BaseModel, ConfigDict


class IngresoDetalleDTO(BaseModel):
    propiedad_id: int
    titulo: str
    total: float
    reservas: int

    model_config = ConfigDict(from_attributes=True)


class IngresosAnfitrionDTO(BaseModel):
    total: float
    detalle: list[IngresoDetalleDTO]

    model_config = ConfigDict(from_attributes=True)
