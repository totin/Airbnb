from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from dto.propiedad import PropiedadResponse
from services.propiedad import PropiedadService
from services.reserva import ReservaService


router = APIRouter(
    prefix="/anfitriones",
    tags=["Anfitriones"]
)


@router.get(
    "/{anfitrion_id}/propiedades",
    response_model=list[PropiedadResponse]
)
def obtener_propiedades(
    anfitrion_id: int,
    db: Session = Depends(get_db)
):
    service = PropiedadService(db)

    return service.obtener_propiedades_anfitrion(
        anfitrion_id
    )


@router.patch(
    "/{anfitrion_id}/reservas/{reserva_id}/confirmar"
)
def confirmar_reserva(
    anfitrion_id: int,
    reserva_id: int,
    db: Session = Depends(get_db)
):
    service = ReservaService(db)

    return service.confirmar_reserva(
        reserva_id,
        anfitrion_id
    )


@router.patch(
    "/{anfitrion_id}/reservas/{reserva_id}/rechazar"
)
def rechazar_reserva(
    anfitrion_id: int,
    reserva_id: int,
    db: Session = Depends(get_db)
):
    service = ReservaService(db)

    return service.rechazar_reserva(
        reserva_id,
        anfitrion_id
    )


@router.patch(
    "/{anfitrion_id}/reservas/{reserva_id}/cancelar"
)
def cancelar_reserva(
    anfitrion_id: int,
    reserva_id: int,
    db: Session = Depends(get_db)
):
    service = ReservaService(db)

    return service.cancelar_reserva(
        reserva_id,
        anfitrion_id
    )


@router.get(
    "/{anfitrion_id}/ingresos"
)
def obtener_ingresos(
    anfitrion_id: int,
    desde: date,
    hasta: date,
    db: Session = Depends(get_db)
):
    service = ReservaService(db)

    return service.obtener_ingresos(
        anfitrion_id,
        desde,
        hasta
    )