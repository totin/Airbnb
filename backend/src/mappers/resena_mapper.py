from src.db.models.resena_model import Resena
from src.dtos.resena_dto import ResenaResponse


def to_resena_response(resena: Resena) -> ResenaResponse:
    """Convierte un Model SQLAlchemy en un DTO de respuesta."""
    return ResenaResponse.model_validate(resena)