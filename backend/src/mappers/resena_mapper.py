from models.resena import Resena
from dto.resena import ResenaCreate, ResenaResponse


def resena_create_to_model(
    dto: ResenaCreate,
    autor_id: int
) -> Resena:
    return Resena(
        reserva_id=dto.reserva_id,
        autor_id=autor_id,
        puntaje=dto.puntaje,
        comentario=dto.comentario
    )


def resena_to_response(model: Resena) -> ResenaResponse:
    return ResenaResponse(
        id=model.id,
        reserva_id=model.reserva_id,
        autor_id=model.autor_id,
        puntaje=model.puntaje,
        comentario=model.comentario,
        fecha=model.fecha
    )