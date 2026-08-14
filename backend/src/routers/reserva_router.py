from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.db.connection import get_db
from src.db.models.usuario import Usuario
from src.dtos.reserva_dto import ReservaCreateDTO, ReservaResponseDTO
from src.middlewares.auth_middleware import get_current_user
from src.services.reserva_service import ReservaService

router = APIRouter(prefix="/reservas", tags=["Reservas"])


@router.post(
    "",
    response_model=ReservaResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva reserva"
)
def crear_reserva(
    reserva_data: ReservaCreateDTO,
    current_user: Usuario = Depends(get_current_user),  # 🛡️ Seguridad
    db: Session = Depends(get_db)
):
    """HU4: Permite a un huésped reservar una propiedad."""
    reserva_service = ReservaService(db)
    return reserva_service.crear_reserva(reserva_data, huesped_id=current_user.id)


@router.get(
    "/mis-reservas",
    response_model=list[ReservaResponseDTO],
    summary="Obtener las reservas del usuario autenticado"
)
def listar_mis_reservas(
    current_user: Usuario = Depends(get_current_user),  # 🛡️ Seguridad
    db: Session = Depends(get_db)
):
    """HU5: Devuelve la lista de reservas hechas por el usuario actual."""
    reserva_service = ReservaService(db)
    return reserva_service.obtener_reservas_de_huesped(huesped_id=current_user.id)