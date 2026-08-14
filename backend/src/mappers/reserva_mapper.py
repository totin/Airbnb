from models.reserva import Reserva
from dto.reserva import ReservaCreate, ReservaResponse


def reserva_create_to_model(
    dto: ReservaCreate,
    huesped_id: int,
    total: float
) -> Reserva:
    return Reserva(
        propiedad_id=dto.propiedad_id,
        huesped_id=huesped_id,
        fecha_inicio=dto.fecha_inicio,
        fecha_fin=dto.fecha_fin,
        estado="pendiente",
        total=total
    )


def reserva_to_response(model: Reserva) -> ReservaResponse:
    return ReservaResponse(
        id=model.id,
        propiedad_id=model.propiedad_id,
        huesped_id=model.huesped_id,
        fecha_inicio=model.fecha_inicio,
        fecha_fin=model.fecha_fin,
        estado=model.estado,
        total=model.total
    )