from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import get_db
from dto.propiedad import (
    PropiedadCreate,
    PropiedadResponse
)
from dto.resena import ResenaResponse
from services.propiedad import PropiedadService
from services.resena import ResenaService


router = APIRouter(
    prefix="/propiedades",
    tags=["Propiedades"]
)


@router.post(
    "",
    response_model=PropiedadResponse,
    status_code=201
)
def crear_propiedad(
    propiedad: PropiedadCreate,
    anfitrion_id: int,
    db: Session = Depends(get_db)
):
    service = PropiedadService(db)

    return service.crear_propiedad(
        propiedad,
        anfitrion_id
    )


@router.get(
    "",
    response_model=list[PropiedadResponse]
)
def buscar_propiedades(
    ciudad: str,
    desde: date | None = None,
    hasta: date | None = None,
    huespedes: int | None = None,
    precio_max: float | None = None,
    amenidades: str | None = None,
    db: Session = Depends(get_db)
):
    service = PropiedadService(db)

    lista_amenidades = None

    if amenidades:
        lista_amenidades = [
            a.strip()
            for a in amenidades.split(",")
        ]

    return service.buscar_propiedades(
        ciudad=ciudad,
        desde=desde,
        hasta=hasta,
        huespedes=huespedes,
        precio_max=precio_max,
        amenidades=lista_amenidades
    )


@router.get(
    "/top",
    response_model=list[PropiedadResponse]
)
def obtener_top_propiedades(
    ciudad: str,
    db: Session = Depends(get_db)
):
    service = PropiedadService(db)

    return service.obtener_top_propiedades(ciudad)


@router.get(
    "/{propiedad_id}",
    response_model=PropiedadResponse
)
def obtener_propiedad(
    propiedad_id: int,
    db: Session = Depends(get_db)
):
    service = PropiedadService(db)

    return service.obtener_propiedad(propiedad_id)


@router.get(
    "/{propiedad_id}/resenas",
    response_model=list[ResenaResponse]
)
def obtener_resenas(
    propiedad_id: int,
    db: Session = Depends(get_db)
):
    service = ResenaService(db)

    return service.obtener_resenas_propiedad(
        propiedad_id
    )


@router.get(
    "/{propiedad_id}/disponibilidad"
)
def obtener_disponibilidad(
    propiedad_id: int,
    mes: str,
    db: Session = Depends(get_db)
):
    service = PropiedadService(db)

    return service.obtener_disponibilidad(
        propiedad_id,
        mes
    )